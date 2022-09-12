import pygame
import json
import os

class Block():
    def __init__(self, Game, x, y, Land_Block_Img, Land_Block_Width, Land_Block_Height):
        self.Game = Game
        self.player = self.Game.player
        self.Window = self.Game.Window

        self.x, self.y = x, y
        
        self.Block_Width, self.Block_Height = Land_Block_Width, Land_Block_Height

        self.Land_Block_Img = pygame.transform.scale(
            Land_Block_Img, (self.Block_Width, self.Block_Height)
        )

    def Update(self):
        self.clone = self.Window.blit(
            self.Land_Block_Img, (self.x, self.y)
        )
        for bullet in self.player.Weapon.Bullet_Container:
            if self.Game.Check_Collided(A=self.clone, B=bullet.clone):
                bullet.Hit["Environment"] = True



class Spike():
    def __init__(self, Game, x, y, Spike_Img, Facing, Spike_Width, Spike_Height):
        self.Game = Game
        self.player = self.Game.player
        self.Window = self.Game.Window

        self.x, self.y = x, y

        self.Facing = Facing # ( Facing up , Facing down , Facing left , Facing right)
        
        self.Spike_Width, self.Spike_Height = Spike_Width, Spike_Height

        rotate_rate = [0, 180, 90, 270]
        self.Spike_Img = pygame.transform.scale(
            pygame.transform.rotate(
                Spike_Img, rotate_rate[self.Facing.index(True)]
            ), (self.Spike_Width, self.Spike_Height)
        )

        self.Spike_Vertex = self.Get_Spike_Vertex()
        self.Spike_Slopes = self.Get_Spike_Slope()

    def Get_Spike_Vertex(self): #Get Spike Vertex, return as [Bottom vertex, Bottom vertex, Tip vertex]
        if self.Facing[0]:
            self.Bottom = self.y+self.Spike_Height
            return [
                (self.x, self.y+self.Spike_Height),
                (self.x+self.Spike_Width, self.y+self.Spike_Height),
                (self.x+(self.Spike_Width/2), self.y)
            ]
        elif self.Facing[1]:
            self.Bottom = self.y
            return [
                (self.x, self.y),
                (self.x+self.Spike_Width, self.y),
                (self.x+(self.Spike_Width/2), self.y+self.Spike_Height)
            ]
        elif self.Facing[2]:
            self.Bottom = self.x+self.Spike_Width
            return [
                (self.x+self.Spike_Width, self.y),
                (self.x+self.Spike_Width, self.y+self.Spike_Height),
                (self.x, self.y+(self.Spike_Height/2))
            ]
        elif self.Facing[3]:
            self.Bottom = self.x
            return [
                (self.x, self.y),
                (self.x, self.y+self.Spike_Height),
                (self.x+self.Spike_Width, self.y+(self.Spike_Height/2))
            ]

    def Get_Spike_Slope(self):
        # return a&b refering to y=ax+b
        a_1 = (self.Spike_Vertex[0][1] - self.Spike_Vertex[2][1]) / (self.Spike_Vertex[0][0] - self.Spike_Vertex[2][0])
        b_1 = self.Spike_Vertex[0][1] - (a_1*self.Spike_Vertex[0][0])
        a_2 = (self.Spike_Vertex[1][1] - self.Spike_Vertex[2][1]) / (self.Spike_Vertex[1][0] - self.Spike_Vertex[2][0])
        b_2 = self.Spike_Vertex[1][1] - (a_2*self.Spike_Vertex[1][0])
        return [
            (a_1, b_1),
            (a_2, b_2)
        ]

    def Check_Spike_Collided(self, B):
        B_x, B_y, B_w, B_h = (B.x, B.y)+B.size
        self.Spike_Vertex = self.Get_Spike_Vertex()
        self.Spike_Slopes = self.Get_Spike_Slope()

        B_x, B_y, B_w, B_h = (B.x, B.y)+B.size
        Judgement = (
            (self.x <= B_x <= self.x+self.Spike_Width or self.x <= B_x+B_w <= self.x+self.Spike_Width) or (B_x <= self.x <= B_x+B_w or B_x <= self.x+self.Spike_Width <= B_x+B_w)
            ) and (
            (self.y <= B_y <= self.y+self.Spike_Height or self.y <= B_y+B_h <= self.y+self.Spike_Height) or (B_y <= self.y <= B_y+B_h or B_y <= self.y+self.Spike_Height <= B_y+B_h)
        )
        if not Judgement:
            return False

        for vertex in self.Spike_Vertex:
            if (B_x < vertex[0] < B_x+B_w) and (B_y < vertex[1] < B_y+B_h):
                return True
        
        if self.Facing[0] or self.Facing[1]:
            if (self.Bottom == B_y) or (self.Bottom == B_y+B_h):
                if (B_x < self.x < B_x+B_w) or (B_x < self.x+self.Spike_Width < B_x+B_w):
                    return True
            if self.y <= B_y <= self.y+self.Spike_Height:
                Checking_value = B_y
            elif self.y <= B_y+B_h <= self.y+self.Spike_Height:
                Checking_value = B_y+B_h
            else:
                return False
            x_points = [
                (Checking_value-self.Spike_Slopes[0][1])/self.Spike_Slopes[0][0], 
                (Checking_value-self.Spike_Slopes[1][1])/self.Spike_Slopes[1][0]
            ]
            if (min(x_points) <= B_x <= max(x_points)) or (min(x_points) <= B_x+B_w <= max(x_points)) or (B_x <= min(x_points) and B_x+B_w >= max(x_points)):
                if self.Facing[0]:
                    if (self.y == B_y+B_h):
                        return False
                elif self.Facing[1]:
                    if (self.y+self.Spike_Height == B_y) or ((self.x == B_x+B_w) and not (self.x+self.Spike_Width == B_x)) or (not (self.x == B_x+B_w) and (self.x+self.Spike_Width == B_x)):
                        return False
                return True

        elif self.Facing[2] or self.Facing[3]:
            if (self.Bottom == B_x) or (self.Bottom == B_x+B_w):
                if (B_y < self.y < B_y+B_h) or (B_y < self.y+self.Spike_Height < B_y+B_h):
                    return True
            if self.x <= B_x <= self.x+self.Spike_Width:
                Checking_value = B_x
            elif self.x <= B_x+B_w <= self.x+self.Spike_Width:
                Checking_value = B_x+B_w
            else:
                return False
            y_points = [
                (self.Spike_Slopes[0][0]*Checking_value)+self.Spike_Slopes[0][1],
                (self.Spike_Slopes[1][0]*Checking_value)+self.Spike_Slopes[1][1]
            ]
            if (min(y_points) <= B_y <= max(y_points)) or (min(y_points) <= B_y+B_h <= max(y_points)) or (B_y <= min(y_points) and B_y+B_h >= max(y_points)):
                if self.Facing[2]:
                    if (self.x == B_x+B_w) or ((self.y == B_y+B_h) and not (self.y+self.Spike_Height == B_y)) or (not (self.y == B_y+B_h) and (self.y+self.Spike_Height == B_y)):
                        return False
                elif self.Facing[3]:
                    if (self.x+self.Spike_Width == B_x) or ((self.y == B_y+B_h) and not (self.y+self.Spike_Height == B_y)) or (not (self.y == B_y+B_h) and (self.y+self.Spike_Height == B_y)):
                        return False
                return True
        return False
            
    def Draw(self):
        self.clone = self.Window.blit(
            self.Spike_Img, (self.x, self.y)
        )
    
    def Update(self):
        self.Draw()
        if self.Check_Spike_Collided(B=self.player.clone):
            self.player.Health -= 100
        for bullet in self.player.Weapon.Bullet_Container:
            if self.Check_Spike_Collided(B=bullet.clone):
                bullet.Hit["Environment"] = True



class Jump_Stone():
    _Jump_Stone_Img = pygame.image.load(
        os.path.join(
            "assets", "Textures", "Jump_Stone", "Jump_Stone.png"
        )
    )
    def __init__(self, Game, x, y, Jump_Stone_Width, Jump_Stone_Height):
        self.Game = Game
        self.player = self.Game.player
        self.Window = self.Game.Window

        self.x, self.y = x, y

        self.Jump_Stone_Width, self.Jump_Stone_Height = Jump_Stone_Width, Jump_Stone_Height

        self.Jump_Stone_Img = pygame.transform.scale(
            self._Jump_Stone_Img, (self.Jump_Stone_Width, self.Jump_Stone_Height)
        )

        self.Cooldown = 0

    def Check_Jump_Stone_Collided(self, B):
        A_x, A_y, A_w, A_h = self.x, self.y, self.Jump_Stone_Width, self.Jump_Stone_Height
        B_x, B_y, B_w, B_h = (B.x, B.y)+B.size
        Judgement = (
            (A_x <= B_x <= A_x+A_w or A_x <= B_x+B_w <= A_x+A_w) or (B_x <= A_x <= B_x+B_w or B_x <= A_x+A_w <= B_x+B_w)
            ) and (
            (A_y <= B_y <= A_y+A_h or A_y <= B_y+B_h <= A_y+A_h) or (B_y <= A_y <= B_y+B_h or B_y <= A_y+A_h <= B_y+B_h)
        )
        if Judgement:
            return True
        return False
            
    def Draw(self):
        self.clone = self.Window.blit(
            self.Jump_Stone_Img, (self.x, self.y)
        )
    
    def Update(self):
        if self.Cooldown <= 0:
            self.Draw()
            if self.Check_Jump_Stone_Collided(B=self.player.clone):
                self.player.Jumping_Gravity = self.player.Gravity
                self.player.Jump_sound.play()
                self.Cooldown = 120
        else:
            self.Cooldown -= 1



class Spawn_Point():
    _Activate_img = pygame.image.load(
        os.path.join("assets", "Textures", "SpawnPoint", "Activate.png")
    )
    _InActivate_img = pygame.image.load(
        os.path.join("assets", "Textures", "SpawnPoint", "Inactivate.png")
    )
    def __init__(self, Game, Scene, x, y, Spawn_Point_Block_Width, Spawn_Point_Block_Height):
        self.Game = Game
        self.Scene = Scene
        self.Map_x, self.Map_y = self.Scene.Map_x, self.Scene.Map_y
        self.player = self.Game.player
        self.Window = self.Game.Window

        self.x, self.y = x, y

        self.Block_Width, self.Block_Height = Spawn_Point_Block_Width, Spawn_Point_Block_Height
        
        self.Activate_img = pygame.transform.scale(
            self._Activate_img, (self.Block_Width, self.Block_Height)
        )
        self.InActivate_img = pygame.transform.scale(
            self._InActivate_img, (self.Block_Width, self.Block_Height)
        )

        self.img = self.InActivate_img

        #Spawn point value
        self.Activated = False

    def Check_Bullet_Collided(self, B):
        A_x, A_y, A_w, A_h = self.x, self.y, self.Block_Width, self.Block_Height
        B_x, B_y, B_w, B_h = (B.x, B.y)+B.size
        Judgement = (
            (A_x <= B_x <= A_x+A_w or A_x <= B_x+B_w <= A_x+A_w) or (B_x <= A_x <= B_x+B_w or B_x <= A_x+A_w <= B_x+B_w)
            ) and (
            (A_y <= B_y <= A_y+A_h or A_y <= B_y+B_h <= A_y+A_h) or (B_y <= A_y <= B_y+B_h or B_y <= A_y+A_h <= B_y+B_h)
        )
        if Judgement:
            return True
        return False

    def Activate_Spawn_Point(self):
        if not self.Activated:
            self.Activated = True
            self.img = self.Activate_img

            self.player.Set_Respawn(Scene=self.Scene, Map_x=self.Map_x, Map_y=self.Map_y, x=self.x, y=self.y-self.player.Charactor_Height)

    def Draw(self):
        self.Window.blit(
            self.img, (self.x, self.y)
        )

    def Control_Save(self):
        for idx, bullet in enumerate(self.player.Weapon.Bullet_Container):
            if self.Check_Bullet_Collided(B=bullet.clone):
                self.Activate_Spawn_Point()
                self.player.Weapon.Bullet_Container.pop(idx)

    def Update(self):
        self.Control_Save()
        self.Draw()



class Portal(): #A to B
    Portal_Types = {
        "S":(
            pygame.image.load(os.path.join("assets", "Textures", "Portal", "Shop_Icon.png")), 
            pygame.image.load(os.path.join("assets", "Textures", "Portal", "Yellow.png"))
        ), #Shop
        "B":(
            pygame.image.load(os.path.join("assets", "Textures", "Portal", "Boss_Icon.png")), 
            pygame.image.load(os.path.join("assets", "Textures", "Portal", "Red.png"))
        ), #Boss
        "P":(
            pygame.image.load(os.path.join("assets", "Textures", "Portal", "Teleport_Icon.png")), 
            pygame.image.load(os.path.join("assets", "Textures", "Portal", "Blue.png"))
        ) #Teleport
    } 
    def __init__(self, Info, Game, A_Scene, A_x, A_y, Block_Width, Block_Height):
        self.Game = Game
        self.player = self.Game.player
        self.Window = self.Game.Window

        #A ( Start )
        self.A_Scene = A_Scene
        self.A_Map_x, self.A_Map_y = self.A_Scene.Map_x, self.A_Scene.Map_y
        self.A_x, self.A_y = A_x, A_y

        #B ( Destination)
        self.B_Map_x, self.B_Map_y = int(Info[1:3]), int(Info[3:5])
        self.B_x, self.B_y = int(Info[5:7])*Block_Width, int(Info[7:9])*Block_Height
        self.B_Scene = self.Game.Environment.Map[self.B_Map_y][self.B_Map_x]

        #Info[0] = Portal type, Info[1:3] = Portal Destination Map_x, Info[3:5] = Portal Destination Map_y, Info[5:7] = Portal Destination x, Info[7:9] = Portal Destination y
        self.Portal_Interact_Icon, self.Portal_Img = self.Portal_Types[Info[0]]

        #Portal Image and Width Height
        self.Portal_Width, self.Portal_Height = int(Block_Width), int(Block_Height*2)
        self.Portal_Img = pygame.transform.scale(
            self.Portal_Img, (self.Portal_Width, self.Portal_Height)
        )

        #Portal Interact Image and Width Height
        self.Img_Width, self.Img_Height = self.player.Charactor_Width, self.player.Charactor_Height
        self.Img = pygame.transform.scale(
            self.Portal_Interact_Icon, (self.Img_Width, self.Img_Height)
        )

    def Check_Portal_Collided(self, B):
        A_x, A_y, A_w, A_h = self.A_x, self.A_y, self.Portal_Width, self.Portal_Height
        B_x, B_y, B_w, B_h = (B.x, B.y)+B.size
        Judgement = (
            (A_x <= B_x <= A_x+A_w or A_x <= B_x+B_w <= A_x+A_w) or (B_x <= A_x <= B_x+B_w or B_x <= A_x+A_w <= B_x+B_w)
            ) and (
            (A_y <= B_y <= A_y+A_h or A_y <= B_y+B_h <= A_y+A_h) or (B_y <= A_y <= B_y+B_h or B_y <= A_y+A_h <= B_y+B_h)
        )
        if Judgement:
            return True
        return False
            
    def Draw(self):
        self.clone = self.Window.blit(
            self.Portal_Img, (self.A_x, self.A_y)
        )
    
    def Update(self):
        self.Draw()
        if self.Check_Portal_Collided(B=self.player.clone):
            if self.player.Interact(Object=self):
                self.Game.Environment.Set_Scene(Scene=self.B_Scene, Map_x=self.B_Map_x, Map_y=self.B_Map_y)
                self.player.x, self.player.y = self.B_x, self.B_y



class Scene_Defaults():
    def __init__(self, Game, Block_Width, Block_Height):
        #Game values
        self.Game = Game
        self.Window = self.Game.Window
        self.Win_Width, self.Win_Height = self.Window.get_size()

        #Scene related
        self.Map = None
        self.Boss_Map = None
        self.Original_Map = None
        self.Block_Width, self.Block_Height = Block_Width, Block_Height
        self.Loot_Container = []
        self.Blocks = []
        self.Spikes = []
        self.Spawns = []
        self.Coins = []

        #Boss related
        self.Boss = None
        self.Boss_Name = None
        self.Boss_Cleared = True

    def _init_Img(self, Block_Img_Name, Spike_Img_Name, Background_Img_Name):
        self.Block_Img_Name = Block_Img_Name
        self.Block_Img = pygame.image.load(
            os.path.join(
                "assets", "Textures", "Blocks", Block_Img_Name+".png" if ".png" not in Block_Img_Name else Block_Img_Name
            )
        )

        self.Spike_Img_Name = Spike_Img_Name
        self.Spike_Img = pygame.image.load(
            os.path.join(
                "assets", "Textures", "Spikes", Spike_Img_Name+".png" if ".png" not in Spike_Img_Name else Spike_Img_Name
            )
        )

        self.Background_Img_Name = Background_Img_Name
        self.Background_Img = pygame.image.load(os.path.join("assets", "Backgrounds", f"{self.Background_Img_Name}.png"))

    def _Bind_Map(self, Map_x, Map_y):
        self.Map_x, self.Map_y = Map_x, Map_y

    def _Build_Map(self, Map):
        self.Blocks = []
        self.Spikes = []
        self.Spawns = []
        self.Jump_Stones = []
        self.Portals = []
        for row_idx, row in enumerate(Map):
            for col_idx, block in enumerate(row):
                if block == "Block":
                    self.Blocks.append(
                        Block(
                            Game=self.Game, 
                            x=col_idx*self.Block_Width, 
                            y=row_idx*self.Block_Height, 
                            Land_Block_Img=self.Block_Img, 
                            Land_Block_Width=self.Block_Width, 
                            Land_Block_Height=self.Block_Height
                        )
                    )
                elif block == "Spik1":
                    self.Spikes.append(
                        Spike(
                            Game=self.Game, 
                            x=col_idx*self.Block_Width, 
                            y=row_idx*self.Block_Height,
                            Spike_Img=self.Spike_Img, 
                            Facing=(1, 0, 0, 0), 
                            Spike_Width=self.Block_Width,
                            Spike_Height=self.Block_Height
                        )
                    )
                elif block == "Spik2":
                    self.Spikes.append(
                        Spike(
                            Game=self.Game, 
                            x=col_idx*self.Block_Width, 
                            y=row_idx*self.Block_Height,
                            Spike_Img=self.Spike_Img, 
                            Facing=(0, 1, 0, 0), 
                            Spike_Width=self.Block_Width,
                            Spike_Height=self.Block_Height
                        )
                    )
                elif block == "Spik3":
                    self.Spikes.append(
                        Spike(
                            Game=self.Game, 
                            x=col_idx*self.Block_Width, 
                            y=row_idx*self.Block_Height,
                            Spike_Img=self.Spike_Img, 
                            Facing=(0, 0, 1, 0), 
                            Spike_Width=self.Block_Width,
                            Spike_Height=self.Block_Height
                        )
                    )
                elif block == "Spik4":
                    self.Spikes.append(
                        Spike(
                            Game=self.Game, 
                            x=col_idx*self.Block_Width, 
                            y=row_idx*self.Block_Height,
                            Spike_Img=self.Spike_Img, 
                            Facing=(0, 0, 0, 1), 
                            Spike_Width=self.Block_Width,
                            Spike_Height=self.Block_Height
                        )
                    )
                elif block == "JumpS":
                    self.Jump_Stones.append(
                        Jump_Stone(
                            Game=self.Game,
                            x=(col_idx*self.Block_Width)+(self.Block_Width/4), 
                            y=(row_idx*self.Block_Height)+(self.Block_Height/4),
                            Jump_Stone_Width=int(self.Block_Width/2), 
                            Jump_Stone_Height=int(self.Block_Height/2)
                        )
                    )
                elif block == "Spawn":
                    self.Spawns.append(
                        Spawn_Point(
                            Game=self.Game, 
                            Scene=self,  
                            x=col_idx*self.Block_Width, 
                            y=row_idx*self.Block_Height,
                            Spawn_Point_Block_Width=self.Block_Width, 
                            Spawn_Point_Block_Height=self.Block_Height
                        )
                    )
                elif block[0] in ["P", "S", "B"]:
                    self.Portals.append(
                        Portal(
                            Info=block,
                            Game=self.Game,
                            A_Scene=self,
                            A_x=col_idx*self.Block_Width, 
                            A_y=row_idx*self.Block_Height,
                            Block_Width=self.Block_Width, 
                            Block_Height=self.Block_Height
                        )
                    )

    def _Update(self):
        self.Game.Enemy.Update_All_Enemy()

        self.Event_Counter += 1
        return self.Blocks+self.Spawns, self.Spikes, self.Background_Layers

    def _Draw(self):
        for Spawn in self.Spawns:
            Spawn.Update()
        for Block in self.Blocks:
            Block.Update()
        for Spike in self.Spikes:
            Spike.Update()
        for Jump_Stone in self.Jump_Stones:
            Jump_Stone.Update()
        for Portal in self.Portals:
            Portal.Update()




#-------------------------------------------------------------------------------------------------------------------------
"""
    ！！！！Tutorial Scenes！！！！
"""
class Tutorial_1(Scene_Defaults):
    def __init__(self, Env_System):
        super().__init__(Game=Env_System.Game, Block_Width=Env_System.Block_Width, Block_Height=Env_System.Block_Height)
        self.init_Img = super()._init_Img
        self.Draw = super()._Draw
        self.Update = super()._Update
        self.Bind_Map = super()._Bind_Map
        self.Build_Map = super()._Build_Map

    def set(self):
        self.Event_Counter = -1

        self.Build_Map(Map=self.Original_Map)

        self.Background_Layers = [
            pygame.transform.scale(
                self.Background_Img, (self.Win_Width, self.Win_Height)
            )
        ]

        return self.Blocks+self.Spawns, self.Spikes, self.Background_Layers


class Tutorial_2(Scene_Defaults):
    def __init__(self, Env_System):
        super().__init__(Game=Env_System.Game, Block_Width=Env_System.Block_Width, Block_Height=Env_System.Block_Height)
        self.init_Img = super()._init_Img
        self.Draw = super()._Draw
        self.Bind_Map = super()._Bind_Map
        self.Build_Map = super()._Build_Map

    def set(self):
        self.Event_Counter = -1

        self.Build_Map(Map=self.Original_Map)

        self.Background_Layers = [
            pygame.transform.scale(
                self.Background_Img, (self.Win_Width, self.Win_Height)
            )
        ]

        return self.Blocks+self.Spawns, self.Spikes, self.Background_Layers

    def Update(self):
        if self.Event_Counter==-1:
            self.Game.Loot_System.Make_Loot(Loot_Item=self.Game.Weapons.SnowBall_Gun, Spawn_Center=(30, 30))
            self.Update = super()._Update
        self.Event_Counter += 1
        return self.Blocks+self.Spawns, self.Spikes, self.Background_Layers


class Tutorial_3(Scene_Defaults):
    def __init__(self, Env_System):
        super().__init__(Game=Env_System.Game, Block_Width=Env_System.Block_Width, Block_Height=Env_System.Block_Height)
        self.init_Img = super()._init_Img
        self.Draw = super()._Draw
        self.Update = super()._Update
        self.Bind_Map = super()._Bind_Map
        self.Build_Map = super()._Build_Map

    def set(self):
        self.Event_Counter = -1

        self.Build_Map(Map=self.Original_Map)

        self.Background_Layers = [
            pygame.transform.scale(
                self.Background_Img, (self.Win_Width, self.Win_Height)
            )
        ]

        return self.Blocks+self.Spawns, self.Spikes, self.Background_Layers


class Tutorial_4(Scene_Defaults):
    def __init__(self, Env_System):
        super().__init__(Game=Env_System.Game, Block_Width=Env_System.Block_Width, Block_Height=Env_System.Block_Height)
        self.init_Img = super()._init_Img
        self.Draw = super()._Draw
        self.Update = super()._Update
        self.Bind_Map = super()._Bind_Map
        self.Build_Map = super()._Build_Map

    def set(self):
        self.Event_Counter = -1

        self.Build_Map(Map=self.Original_Map)

        self.Background_Layers = [
            pygame.transform.scale(
                self.Background_Img, (self.Win_Width, self.Win_Height)
            )
        ]

        return self.Blocks+self.Spawns, self.Spikes, self.Background_Layers


class Tutorial_5(Scene_Defaults):
    def __init__(self, Env_System):
        super().__init__(Game=Env_System.Game, Block_Width=Env_System.Block_Width, Block_Height=Env_System.Block_Height)
        self.init_Img = super()._init_Img
        self.Draw = super()._Draw
        self.Update = super()._Update
        self.Bind_Map = super()._Bind_Map
        self.Build_Map = super()._Build_Map

    def set(self):
        self.Event_Counter = -1

        self.Build_Map(Map=self.Original_Map)

        self.Background_Layers = [
            pygame.transform.scale(
                self.Background_Img, (self.Win_Width, self.Win_Height)
            )
        ]

        return self.Blocks+self.Spawns, self.Spikes, self.Background_Layers


class Tutorial_6(Scene_Defaults):
    def __init__(self, Env_System):
        super().__init__(Game=Env_System.Game, Block_Width=Env_System.Block_Width, Block_Height=Env_System.Block_Height)
        self.init_Img = super()._init_Img
        self.Draw = super()._Draw
        self.Update = super()._Update
        self.Bind_Map = super()._Bind_Map
        self.Build_Map = super()._Build_Map

    def set(self):
        self.Event_Counter = -1

        self.Build_Map(Map=self.Original_Map)

        self.Background_Layers = [
            pygame.transform.scale(
                self.Background_Img, (self.Win_Width, self.Win_Height)
            )
        ]

        return self.Blocks+self.Spawns, self.Spikes, self.Background_Layers


class Tutorial_7(Scene_Defaults):
    def __init__(self, Env_System):
        super().__init__(Game=Env_System.Game, Block_Width=Env_System.Block_Width, Block_Height=Env_System.Block_Height)
        self.init_Img = super()._init_Img
        self.Draw = super()._Draw
        self.Update = super()._Update
        self.Bind_Map = super()._Bind_Map
        self.Build_Map = super()._Build_Map

    def set(self):
        self.Event_Counter = -1

        self.Build_Map(Map=self.Original_Map)

        self.Background_Layers = [
            pygame.transform.scale(
                self.Background_Img, (self.Win_Width, self.Win_Height)
            )
        ]

        return self.Blocks+self.Spawns, self.Spikes, self.Background_Layers




#-------------------------------------------------------------------------------------------------------------------------
"""
    ！！！！Plateau Scenes！！！！
"""
class Plateau(Scene_Defaults):
    def __init__(self, Env_System):
        super().__init__(Game=Env_System.Game, Block_Width=Env_System.Block_Width, Block_Height=Env_System.Block_Height)
        self.init_Img = super()._init_Img
        self.Draw = super()._Draw
        self.Bind_Map = super()._Bind_Map
        self.Build_Map = super()._Build_Map

        if self.Boss_Name:
            self.Map = self.Boss_Map
        else:
            self.Map = self.Original_Map

    def set(self):
        if self.Boss_Cleared:
            self.Update = super()._Update
            self.Map = self.Original_Map
        else:
            self.Map = self.Boss_Map

        self.Event_Counter = -1

        self.Build_Map(Map=self.Map)

        self.Background_Layers = [
            pygame.transform.scale(
                self.Background_Img, (self.Win_Width, self.Win_Height)
            )
        ]

        return self.Blocks+self.Spawns, self.Spikes, self.Background_Layers

    def Boss_Cleared_Event(self):
        self.Boss_Cleared = True
        self.Map = self.Original_Map
        self.Build_Map(Map=self.Map)
        self.Update = super()._Update

    def Update(self):
        if self.Event_Counter == -1 and self.Boss_Name and not self.Boss_Cleared:
            self.Boss = self.Game.Enemy.Make_Boss(Boss_Name=self.Boss_Name, Center=(480, 400))
            print("spawn boss: ", self.Boss_Name)
        
        if self.Boss.is_dead:
            self.Boss_Cleared_Event()
        self.Game.Enemy.Update_All_Enemy()

        self.Event_Counter += 1
        return self.Blocks+self.Spawns, self.Spikes, self.Background_Layers












#-------------------------------------------------------------------------------------------------------------------------
"""
    ！！！！Scenes！！！！
"""
class General(Scene_Defaults):
    def __init__(self, Env_System):
        super().__init__(Game=Env_System.Game, Block_Width=Env_System.Block_Width, Block_Height=Env_System.Block_Height)
        self.init_Img = super()._init_Img
        self.Draw = super()._Draw
        self.Bind_Map = super()._Bind_Map
        self.Build_Map = super()._Build_Map

        if self.Boss_Name:
            self.Map = self.Boss_Map
        else:
            self.Map = self.Original_Map

    def set(self):
        if self.Boss_Cleared:
            self.Update = super()._Update
            self.Map = self.Original_Map
        else:
            self.Map = self.Boss_Map

        self.Event_Counter = -1

        self.Build_Map(Map=self.Map)

        self.Background_Layers = [
            pygame.transform.scale(
                self.Background_Img, (self.Win_Width, self.Win_Height)
            )
        ]

        return self.Blocks+self.Spawns, self.Spikes, self.Background_Layers

    def Boss_Cleared_Event(self):
        self.Boss_Cleared = True
        self.Map = self.Original_Map
        self.Build_Map(Map=self.Map)
        self.Update = super()._Update

    def Update(self):
        if self.Event_Counter == -1 and self.Boss_Name and not self.Boss_Cleared:
            self.Boss = self.Game.Enemy.Make_Boss(Boss_Name=self.Boss_Name, Center=(480, 400))
        
        if self.Boss.is_dead:
            self.Boss_Cleared_Event()
        self.Game.Enemy.Update_All_Enemy()

        self.Event_Counter += 1
        return self.Blocks+self.Spawns, self.Spikes, self.Background





class Test_Scene(Scene_Defaults):
    Boss_Name = "Angtrisent"
    def __init__(self, Env_System):
        super().__init__(Game=Env_System.Game, Block_Width=Env_System.Block_Width, Block_Height=Env_System.Block_Height, Block_Img_Name="Grass", Spike_Img_Name="Spike")
        self.Draw = super()._Draw
        self.Bind_Map = super()._Bind_Map
        self.Build_Map = super()._Build_Map

    def set(self):
        self.Event_Counter = -1

        self.Build_Map(Map=self.Map)

        self.Background = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "Backgrounds", "4.png")), (self.Win_Width, self.Win_Height)
        )

        return self.Blocks+self.Spawns, self.Spikes, self.Background

    def Boss_Cleared_Event(self):
        self.Boss_Cleared = True
        self.Update = super()._Update

    def Update(self):
        if self.Event_Counter == -1:
            self.Boss = self.Game.Enemy.Make_Boss(Boss_Name=self.Boss_Name, Center=(480, 400))
        
        if self.Boss.is_dead:
            self.Boss_Cleared_Event()
        self.Game.Enemy.Update_All_Enemy()

        self.Event_Counter += 1
        return self.Blocks+self.Spawns, self.Spikes, self.Background









#-------------------------------------------------------------------------------------------------------------------------
class Boss_Scene(Scene_Defaults):
    def __init__(self, Env_System):
        super().__init__(Game=Env_System.Game, Block_Width=Env_System.Block_Width, Block_Height=Env_System.Block_Height, Block_Img_Name="Purple_Brick", Spike_Img_Name="Spike")
        self.Draw = super()._Draw
        self.Bind_Map = super()._Bind_Map
        self.Build_Map = super()._Build_Map

    def set(self):
        self.Event_Counter = -1

        if self.Boss_Cleared:
            self.Update = super()._Update
            self.Build_Map(Map=self.Original_Map)
        else:
            self.Build_Map(Map=self.Boss_Map)

        self.Background = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "Enemy", "Boss", "Cygnus", "BackGround.png")), (self.Win_Width, self.Win_Height)
        )

        return self.Blocks+self.Spawns, self.Spikes, self.Background

    def Boss_Cleared_Event(self):
        self.Boss_Cleared = True
        self.Build_Map(Map=self.Original_Map)
        self.Update = super()._Update

    def Update(self):
        if self.Event_Counter == -1:
            self.Boss = self.Game.Enemy.Make_Boss(Boss_Name=self.Boss_Name, x_y=(480, 100))

        if self.Boss.is_dead:
            self.Boss_Cleared_Event()
        
        self.Game.Enemy.Update_All_Enemy()

        self.Event_Counter += 1
        return self.Blocks+self.Spawns, self.Spikes, self.Background















#-----------------------------------------------------------------------------------------------------------------------------------------------------
""" Environment & Scene Main System """
#Environment & Scene Control
class Environment():
    def __init__(self, Game, Block_Width, Block_Height):
        self.Game = Game
        self.Window = Game.Window
        self.player = Game.player

        self.Win_Width, self.Win_Height, self.Block_Width, self.Block_Height = self.Game.Width, self.Game.Height, Block_Width, Block_Height

        self.Map = [
            [Tutorial_1(Env_System=self), Tutorial_2(Env_System=self), Tutorial_3(Env_System=self), Tutorial_4(Env_System=self), Tutorial_5(Env_System=self), Tutorial_6(Env_System=self), Tutorial_7(Env_System=self), None                       , Plateau(Env_System=self)   , Plateau(Env_System=self)   , Plateau(Env_System=self)   , Plateau(Env_System=self)   ],
            [None                       , None                       , None                       , None                       , None                       , None                       , None                       , None                       , Plateau(Env_System=self)   , Plateau(Env_System=self)   , Plateau(Env_System=self)   , Plateau(Env_System=self)   ],
            [General(Env_System=self)   , None                       , None                       , None                       , None                       , None                       , Plateau(Env_System=self)   , None                       , Plateau(Env_System=self)   , Plateau(Env_System=self)   , Plateau(Env_System=self)   , Plateau(Env_System=self)   ],
            [None                       , None                       , None                       , None                       , None                       , None                       , None                       , None                       , Plateau(Env_System=self)   , Plateau(Env_System=self)   , Plateau(Env_System=self)   , Plateau(Env_System=self)   ],
        ]

        self.Load_Default_Map()

        self.Map_x, self.Map_y = 0, 0
        self.Current_Scene = self.Map[self.Map_y][self.Map_x]
        self.Last_Scene = (self.Current_Scene, self.Map_x, self.Map_y)
        self.Blocks, self.Spikes, self.Background_Layers = self.Current_Scene.set()

        self.player.Bind_Env(Env=self)



    #Functions
    def Get_Available_Directions(self): #Returns if there's a available scene on each direction
        if self.Current_Scene.Boss_Cleared:
            Can_Go_Up = self.Map_y != 0 and self.Map[self.Map_y-1][self.Map_x] != None
            Can_Go_Down = self.Map_y != len(self.Map)-1 and self.Map[self.Map_y+1][self.Map_x] != None
            Can_Go_Left = self.Map_x != 0 and self.Map[self.Map_y][self.Map_x-1] != None
            Can_Go_Right = self.Map_x != len(self.Map[self.Map_y])-1 and self.Map[self.Map_y][self.Map_x+1] != None
        else:
            Can_Go_Up = Can_Go_Down = Can_Go_Left = Can_Go_Right = False
        return Can_Go_Up, Can_Go_Down, Can_Go_Left, Can_Go_Right

    def Set_Scene(self, Scene, Map_x, Map_y):
        self.Game.Enemy.Clear_All_Enemy()
        self.Game.Loot_System.Clear_All_Loot()

        self.Map_x, self.Map_y = Map_x, Map_y
        self.Current_Scene = Scene
        self.Last_Scene = (self.Current_Scene, self.Map_x, self.Map_y)
        self.Blocks, self.Spikes, self.Background = self.Current_Scene.set()



    #Update Environment
    def Update(self, state):
        Available_Next_Scene_Directions = self.Get_Available_Directions()
        Updated = False
        if state[0]:
            if Available_Next_Scene_Directions[0]:
                self.Last_Scene = (self.Current_Scene, self.Map_x, self.Map_y)
                self.player.y = self.Win_Height-self.player.Charactor_Height

                self.Map_y -= 1
                self.Current_Scene = self.Map[self.Map_y][self.Map_x]
                self.Blocks, self.Spikes, self.Background = self.Current_Scene.set()
                Updated = True

        if state[1]:
            if Available_Next_Scene_Directions[1]:
                self.Last_Scene = (self.Current_Scene, self.Map_x, self.Map_y)
                self.player.y = 0

                self.Map_y += 1
                self.Current_Scene = self.Map[self.Map_y][self.Map_x]
                self.Blocks, self.Spikes, self.Background = self.Current_Scene.set()
                
                Updated = True

        if state[2]:
            if Available_Next_Scene_Directions[2]:
                self.Last_Scene = (self.Current_Scene, self.Map_x, self.Map_y)
                self.player.x = self.Win_Width-self.player.Charactor_Width

                self.Map_x -= 1
                self.Current_Scene = self.Map[self.Map_y][self.Map_x]
                self.Blocks, self.Spikes, self.Background = self.Current_Scene.set()
                
                Updated = True

        if state[3]:
            if Available_Next_Scene_Directions[3]:
                self.Last_Scene = (self.Current_Scene, self.Map_x, self.Map_y)
                self.player.x = 0

                self.Map_x += 1
                self.Current_Scene = self.Map[self.Map_y][self.Map_x]
                self.Blocks, self.Spikes, self.Background = self.Current_Scene.set()
                
                Updated = True

        if Updated:
            self.Game.Clear_All_Entity()
            self.Game.Loot_System.Loot_Container = self.Current_Scene.Loot_Container

        self.Current_Scene.Loot_Container = self.Game.Loot_System.Update_All_Loot()
        self.Blocks, self.Spikes, self.Background_Layers = self.Current_Scene.Update()

    def Draw_Environment(self):
        for Background in self.Background_Layers:
            self.Window.blit(Background, (0, 0))

        self.Current_Scene.Draw()



    #Saving and Loading
    def Load_Default_Map(self):
        with open(os.path.join("Config", "Default_MapData.json")) as MapData:
            Default_MapData = json.load(MapData)

        for y_idx, row in enumerate(self.Map):
            for x_idx, scene in enumerate(row):
                if scene:
                    cord_id = "{:0>2}{:0>2}".format(x_idx, y_idx)
                    scene.init_Img(
                        Block_Img_Name=Default_MapData[cord_id]["Block_Img_Name"], 
                        Spike_Img_Name=Default_MapData[cord_id]["Spike_Img_Name"],
                        Background_Img_Name=Default_MapData[cord_id]["Background_Img_Name"]
                    )
                    scene.Bind_Map(Map_x=x_idx, Map_y=y_idx)
                    scene.Boss_Map = Default_MapData[cord_id]["Boss_Map"]
                    scene.Boss_Name = Default_MapData[cord_id]["Boss_Name"]
                    scene.Boss_Cleared = Default_MapData[cord_id]["Boss_Cleared"]
                    scene.Original_Map = Default_MapData[cord_id]["Original_Map"]

    def Load_Saving(self, Environment_data):
        for y_idx, row in enumerate(self.Map):
            for x_idx, scene in enumerate(row):
                if scene:
                    cord_id = "{:0>2}{:0>2}".format(x_idx, y_idx)
                    scene.init_Img(
                        Block_Img_Name=Environment_data[cord_id]["Block_Img_Name"], 
                        Spike_Img_Name=Environment_data[cord_id]["Spike_Img_Name"],
                        Background_Img_Name=Environment_data[cord_id]["Background_Img_Name"]
                    )
                    scene.Bind_Map(Map_x=x_idx, Map_y=y_idx)
                    scene.Boss_Map = Environment_data[cord_id]["Boss_Map"]
                    scene.Boss_Name = Environment_data[cord_id]["Boss_Name"]
                    scene.Boss_Cleared = Environment_data[cord_id]["Boss_Cleared"]
                    scene.Original_Map = Environment_data[cord_id]["Original_Map"]

    def Get_Saving_Data(self):
        Environment_data = {}
        for y_idx, row in enumerate(self.Map):
            for x_idx, scene in enumerate(row):
                if scene:
                    cord_id = "{:0>2}{:0>2}".format(x_idx, y_idx)
                    Environment_data[cord_id] = {
                        "Boss_Map":scene.Boss_Map,
                        "Boss_Name":scene.Boss_Name,
                        "Boss_Cleared":scene.Boss_Cleared,
                        "Original_Map":scene.Original_Map,
                        "Block_Img_Name":scene.Block_Img_Name,
                        "Spike_Img_Name":scene.Spike_Img_Name,
                        "Background_Img_Name":scene.Background_Img_Name
                    }
        return Environment_data
