import pygame
import os


class Player_Double_Jump():
    Player_Double_Jump_imgs = [
        pygame.image.load(
            os.path.join("assets", "VFX", "DoubleJump", f"{i}.png")
        ) for i in range(1, 8)
    ]
    def __init__(self, Game):
        self.Game = Game
        self.Window = self.Game.Window
        self.player = self.Game.player

        self.Width, self.Height = int(self.player.Charactor_Width*1.5), int(self.player.Charactor_Height*1.5)

        self.imgs = [
            pygame.transform.flip(
                pygame.transform.scale(
                    img, (self.Width, self.Height)
                ), self.player.state["Looking_Left"], False
            ) for img in self.Player_Double_Jump_imgs
        ]

        self.x = self.player.x-(self.Width/2) if not self.player.state["Looking_Left"] else self.player.x+self.player.Charactor_Width-(self.Width/2)
        self.y = self.player.y+self.player.Charactor_Height-(self.Height/2)

        self.idx = 0
        self.counter = 0

    def Update(self):
        self.counter += 1
        if self.counter%4==0:
            self.idx += 1
            if self.idx >= len(self.imgs):
                return True
        self.Window.blit(
            self.imgs[self.idx], (self.x, self.y)
        )
        return False


class Player_Dash():
    Player_Dash_imgs = [
        pygame.image.load(
            os.path.join("assets", "VFX", "Dash", f"{i}.png")
        ) for i in range(1, 9)
    ]
    def __init__(self, Game):
        self.Game = Game
        self.Window = self.Game.Window
        self.player = self.Game.player

        self.Width, self.Height = int(self.player.Charactor_Width*3), int(self.player.Charactor_Height*3)

        self.imgs = [
            pygame.transform.flip(
                pygame.transform.scale(
                    img, (self.Width, self.Height)
                ), self.player.state["Looking_Left"], False
            ) for img in self.Player_Dash_imgs
        ]

        self.x = self.player.x-(self.Width/2) if not self.player.state["Looking_Left"] else self.player.x+self.player.Charactor_Width-(self.Width/2)
        self.y = self.player.y+(self.player.Charactor_Height/2)-(self.Height/2)

        self.idx = 0
        self.counter = 0

    def Update(self):
        self.x = self.player.x-(self.Width/2) if not self.player.state["Looking_Left"] else self.player.x+self.player.Charactor_Width-(self.Width/2)
        self.y = self.player.y+(self.player.Charactor_Height/2)-(self.Height/2)
        self.counter += 1
        if self.counter%3==0:
            self.idx += 1
            if self.idx >= len(self.imgs):
                return True
        self.Window.blit(
            self.imgs[self.idx], (self.x, self.y)
        )
        return False


class Player_Land():
    Player_Land_imgs = [
        pygame.image.load(
            os.path.join("assets", "VFX", "Land", f"{i}.png")
        ) for i in range(1, 11)
    ]
    def __init__(self, Game):
        self.Game = Game
        self.Window = self.Game.Window
        self.player = self.Game.player

        self.Width, self.Height = int(self.player.Charactor_Width*3), int(self.player.Charactor_Height)
    
        self.imgs = [
            pygame.transform.flip(
                pygame.transform.scale(
                    img, (self.Width, self.Height)
                ), self.player.state["Looking_Left"], False
            ) for img in self.Player_Land_imgs
        ]

        self.x = self.player.x+(self.player.Charactor_Width/2)-(self.Width/2)
        self.y = self.player.y+self.player.Charactor_Height-self.Height

        self.idx = 0
        self.counter = 0

    def Update(self):
        self.counter += 1
        if self.counter%3==0:
            self.idx += 1
            if self.idx >= len(self.imgs):
                return True
        self.Window.blit(
            self.imgs[self.idx], (self.x, self.y)
        )
        return False


class Player_Dead():
    Player_Dead_imgs = [
        pygame.image.load(
            os.path.join("assets", "VFX", "Dead", f"{i}.png")
        ) for i in range(1, 31)
    ]
    def __init__(self, Game):
        self.Game = Game
        self.Window = self.Game.Window
        self.player = self.Game.player

        self.Width, self.Height = self.player.Charactor_Width*5, self.player.Charactor_Height*5

        self.imgs = [
            pygame.transform.scale(
                img,(self.Width, self.Height) 
            ) for img in self.Player_Dead_imgs
        ]

        self.x = self.player.x+(self.player.Charactor_Width/2)-(self.Width/2)
        self.y = self.player.y+(self.player.Charactor_Height/2)-(self.Height/2)

        self.idx = 0
        self.counter = 0

    def Update(self):
        self.counter += 1
        if self.counter%2==0:
            self.idx += 1
            if self.idx >= len(self.imgs):
                return True
        self.Window.blit(
            self.imgs[self.idx], (self.x, self.y)
        )
        return False


class Particles():
    Player_Double_Jump = Player_Double_Jump
    Player_Dash = Player_Dash
    Player_Land = Player_Land
    Player_Dead = Player_Dead
    def __init__(self, Game):
        self.Game = Game
        self.Window = self.Game.Window
        self.player = self.Game.player
        self.Particle_Container = []
    def Add_Particle(self, particle):
        self.Particle_Container.append(particle(Game=self.Game))
    def Update(self):
        for particle in self.Particle_Container:
            Remove = particle.Update()
            if Remove:
                self.Particle_Container.remove(particle)