import pygame
import os


class Loot():
    pointer_image = pygame.image.load(os.path.join("assets", "pointer.png"))
    def __init__(self, Game, Represent, Spawn_Center):
        self.Game = Game
        self.player = self.Game.player
        self.Window = self.Game.Window
        self.Environment = self.Game.Environment
        self.Win_Width, self.Win_Height = self.Window.get_size() 

        self.Falling_Gravity = 0
        self.Gravity = 14
        self.Falling_vel = 2

        self.ID = Represent.ID
        self.Represent = Represent
        self.Img_Width, self.Img_Height = self.player.Charactor_Width, self.player.Charactor_Height
        self.Img = pygame.transform.scale(
            self.Represent.Loot_Img, (self.Img_Width, self.Img_Height)
        )

        self.x, self.y =  (Spawn_Center[0]-(self.Img_Width/2), Spawn_Center[1]-(self.Img_Height/2))

        self.clone = self.Window.blit(self.Img, (self.x, self.y))

    def Get_Position(self): #return (Top_Border, Bottom_Border, Left_Border, Right_Border, Center_x, Center_y)
        info = ((self.y), (self.y+self.Img_Height), (self.x), (self.x+self.Img_Width), (self.x+self.Img_Width//2), (self.y+self.Img_Height//2))
        return info

    def Draw_Loot_Img(self):
        self.clone = self.Window.blit(
            self.Img, (self.x, self.y)
        )

    def Check_Landed(self, next_move_val=0):
        Top_Border, Bottom_Border, Left_Border, Right_Border, Center_x, Center_y = self.Get_Position() #Get Player Position info

        for Block in sorted(self.Environment.Blocks, key=lambda Block:Block.y):
            if Block.x < Right_Border and Left_Border < Block.x+Block.Block_Width: #Check if the Loot's x position is in between the Land border
                if Bottom_Border <= Block.y and (Bottom_Border - next_move_val) >= Block.y: #Check if the Loot will fall onto/into the Land after next fall
                    self.y = Block.y-self.Img_Height #if so, keep the Loot on top of the Land
                    return True
        return False

    def Control_Fall(self):
        if not self.Check_Landed():
            self.y -= self.Falling_Gravity
            if self.Falling_Gravity > -self.Gravity:
                self.Falling_Gravity -= self.Falling_vel
            else:
                self.Falling_Gravity = -self.Gravity
            if self.Check_Landed(next_move_val=self.Falling_Gravity):
                self.Falling_Gravity = 0

    def Update(self):
        self.Control_Fall()
        self.Draw_Loot_Img()
        if self.Game.Check_Collided(A=self.player.clone, B=self.clone):
            if self.player.Interact(Object=self):
                if self.Represent.Loot_Type == "Weapon":
                    self.player.Equip_Weapon(Weapon=self.Represent)
                return True
            self.Window.blit(
                self.pointer_image, (self.x, self.y)
            )
            self.Window.blit(
                self.Represent.NameTag_Img, (self.x+24, self.y-24)
            )
        return False




class Coin_Defaults():
    Imgs = []
    for img_id in range(9):
        Imgs.append(
            pygame.image.load(
                os.path.join(
                    "assets", "Textures", "Coin", f"Coin{img_id+1}.png"
                )
            )
        )
    def __init__(self, Game):
        for idx, Coin_Img in enumerate(self.Imgs):
            self.Imgs[idx] = pygame.transform.scale(
                Coin_Img, (Game.Block_Width, Game.Block_Height)
            )

class Coin(Coin_Defaults):
    ID = "Coin"
    def __init__(self, Game, Spawn_Center):
        super().__init__(Game=Game)

        self.Game = Game
        self.player = self.Game.player
        self.Window = self.Game.Window
        self.Environment = self.Game.Environment

        self.Falling_Gravity = 0
        self.Gravity = 14
        self.Falling_vel = 2

        self.Img_Width, self.Img_Height = self.Game.Block_Width, self.Game.Block_Height

        self.x, self.y = Spawn_Center[0]-(self.Img_Width/2), Spawn_Center[1]-(self.Img_Height/2)

        self.Counter = 0
        self.Img_id = 0
        
        self.clone = self.Window.blit(
            self.Imgs[self.Img_id], (self.x, self.y)
        )

    def Get_Position(self): #return (Top_Border, Bottom_Border, Left_Border, Right_Border, Center_x, Center_y)
        info = ((self.y), (self.y+self.Img_Height), (self.x), (self.x+self.Img_Width), (self.x+self.Img_Width//2), (self.y+self.Img_Height//2))
        return info

    def Check_Landed(self, next_move_val=0):
        Top_Border, Bottom_Border, Left_Border, Right_Border, Center_x, Center_y = self.Get_Position() #Get Player Position info

        for Block in sorted(self.Environment.Blocks, key=lambda Block:Block.y):
            if Block.x < Right_Border and Left_Border < Block.x+Block.Block_Width: #Check if the Loot's x position is in between the Land border
                if Bottom_Border <= Block.y and (Bottom_Border - next_move_val) >= Block.y: #Check if the Loot will fall onto/into the Land after next fall
                    self.y = Block.y-self.Img_Height #if so, keep the Loot on top of the Land
                    return True
        return False

    def Control_Fall(self):
        if not self.Check_Landed():
            self.y -= self.Falling_Gravity
            if self.Falling_Gravity > -self.Gravity:
                self.Falling_Gravity -= self.Falling_vel
            else:
                self.Falling_Gravity = -self.Gravity
            if self.Check_Landed(next_move_val=self.Falling_Gravity):
                self.Falling_Gravity = 0
        else:
            self.Animation()

    def Animation(self):
        if self.Counter%12 == 0:
            self.Img_id += 1
            if self.Img_id >= len(self.Imgs):
                self.Img_id = self.Counter = 0
        self.Counter += 1

        self.clone = self.Window.blit(
            self.Imgs[self.Img_id], (self.x, self.y)
        )
    
    def Draw_Coin(self):
        self.clone = self.Window.blit(
            self.Imgs[self.Img_id], (self.x, self.y)
        )

    def Update(self):
        self.Control_Fall()
        self.Draw_Coin()
        if self.Game.Check_Collided(A=self.clone, B=self.player.clone):
            self.player.Coins += 1
            return True
        return False



class Boss_Approval_Defaults():
    Imgs = []
    for img_id in range(9):
        Imgs.append(
            pygame.image.load(
                os.path.join(
                    "assets", "Textures", "Coin", f"BA{img_id+1}.png"
                )
            )
        )
    def __init__(self, Game):
        for idx, BA_Img in enumerate(self.Imgs):
            self.Imgs[idx] = pygame.transform.scale(
                BA_Img, (int(Game.Block_Width/12*13), int(Game.Block_Height/2*3))
            )

class Boss_Approval(Boss_Approval_Defaults):
    ID = "Boss_Approval"
    def __init__(self, Game, Spawn_Center):
        super().__init__(Game=Game)

        self.Game = Game
        self.player = self.Game.player
        self.Window = self.Game.Window
        self.Environment = self.Game.Environment

        self.Falling_Gravity = 0
        self.Gravity = 14
        self.Falling_vel = 2

        self.Img_Width, self.Img_Height = self.Imgs[0].get_size()
        
        self.x, self.y = Spawn_Center[0]-(self.Img_Width/2), Spawn_Center[1]-(self.Img_Height/2)

        self.Counter = 0
        self.Img_id = 0
        
        self.clone = self.Window.blit(
            self.Imgs[self.Img_id], (self.x, self.y)
        )

    def Get_Position(self): #return (Top_Border, Bottom_Border, Left_Border, Right_Border, Center_x, Center_y)
        info = ((self.y), (self.y+self.Img_Height), (self.x), (self.x+self.Img_Width), (self.x+self.Img_Width//2), (self.y+self.Img_Height//2))
        return info

    def Check_Landed(self, next_move_val=0):
        Top_Border, Bottom_Border, Left_Border, Right_Border, Center_x, Center_y = self.Get_Position() #Get Player Position info

        for Block in sorted(self.Environment.Blocks, key=lambda Block:Block.y):
            if Block.x < Right_Border and Left_Border < Block.x+Block.Block_Width: #Check if the Loot's x position is in between the Land border
                if Bottom_Border <= Block.y and (Bottom_Border - next_move_val) >= Block.y: #Check if the Loot will fall onto/into the Land after next fall
                    self.y = Block.y-self.Img_Height #if so, keep the Loot on top of the Land
                    return True
        return False

    def Control_Fall(self):
        if not self.Check_Landed():
            self.y -= self.Falling_Gravity
            if self.Falling_Gravity > -self.Gravity:
                self.Falling_Gravity -= self.Falling_vel
            else:
                self.Falling_Gravity = -self.Gravity
            if self.Check_Landed(next_move_val=self.Falling_Gravity):
                self.Falling_Gravity = 0
        else:
            self.Animation()

    def Animation(self):
        if self.Counter%12 == 0:
            self.Img_id += 1
            if self.Img_id >= len(self.Imgs):
                self.Img_id = self.Counter = 0
        self.Counter += 1

    def Draw_Boss_Approval(self):
        self.clone = self.Window.blit(
            self.Imgs[self.Img_id], (self.x, self.y)
        )

    def Update(self):
        self.Control_Fall()
        self.Draw_Boss_Approval()
        if self.Game.Check_Collided(A=self.clone, B=self.player.clone):
            self.player.Boss_Approvals += 1
            return True
        return False
  



#-----------------------------------------------------------------------------------------------------------------------------------------------------
""" Ground Loots """
#Loots
class Loot_System():
    Loot = Loot
    def __init__(self, Game):
        self.Game = Game

        self.Loot_Container = []
    
    def Make_Loot(self, Loot_Item, Spawn_Center):
        self.Loot_Container.append(
            Loot(Game=self.Game, Represent=Loot_Item, Spawn_Center=Spawn_Center)
        )

    def Make_Coin(self, Spawn_Center):
        self.Loot_Container.append(
            Coin(Game=self.Game, Spawn_Center=Spawn_Center)
        )

    def Make_Boss_Approval(self, Spawn_Center):
        self.Loot_Container.append(
            Boss_Approval(Game=self.Game, Spawn_Center=Spawn_Center)
        )

    def Clear_All_Loot(self):
        for _ in self.Loot_Container:
            del _
        self.Loot_Container = []

    def Update_All_Loot(self):
        for idx, _Loot in enumerate(self.Loot_Container):
            Result = _Loot.Update()
            if Result:
                self.Loot_Container.pop(idx)
        return self.Loot_Container