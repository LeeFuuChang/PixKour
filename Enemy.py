from Boss.Boss_Angtrisent import Angtrisent
from Boss import *
import pygame
import os

class Enemy_Bullet():
    def __init__(self, Bullet_Shooter_Center_x, Bullet_Shooter_Center_y):
        pass



#-----------------------------------------------------------------------------------------------------------------------------------------------------
#Enemy Health Bar
class Enemy_Health_Bar():
    def __init__(self, Enemy):
        self.Enemy = Enemy
        self.Frame_Width, self.Frame_Height = self.Enemy.clone.size[0], 30
        self.Bar_Width, self.Bar_Height = self.Frame_Width-(self.Frame_Height//3), self.Frame_Height-(self.Frame_Height//3)
        self.Frame_x, self.Frame_y = self.Enemy.x, self.Enemy.y-self.Frame_Height
        self.Bar_x, self.Bar_y = self.Frame_x+self.Frame_Height//6, self.Frame_y+self.Frame_Height//6
        self.Width_Per_Health = self.Bar_Width/self.Enemy.Health
        self.Frame = pygame.draw.rect(
            self.Enemy.Window, (255, 255, 255), 
            pygame.Rect(self.Frame_x, self.Frame_y, self.Frame_Width, self.Frame_Height)
        )
        self.Bar = pygame.draw.rect(
            self.Enemy.Window, (255, 0, 0), 
            pygame.Rect(self.Bar_x, self.Bar_y, self.Bar_Width, self.Bar_Height)
        )
    def Update(self):
        self.Frame_x, self.Frame_y = self.Enemy.x, self.Enemy.y-self.Frame_Height
        self.Bar_x, self.Bar_y = self.Frame_x+self.Frame_Height//6, self.Frame_y+self.Frame_Height//6
        self.Frame = pygame.draw.rect(
            self.Enemy.Window, (255, 255, 255), 
            pygame.Rect(self.Frame_x, self.Frame_y, self.Frame_Width, self.Frame_Height)
        )
        self.Bar = pygame.draw.rect(
            self.Enemy.Window, (255, 0, 0), 
            pygame.Rect(self.Bar_x, self.Bar_y, self.Enemy.Health*self.Width_Per_Health, self.Bar_Height)
        )

class Boss_Health_Bar():
    def __init__(self, Enemy):
        self.Enemy = Enemy
        self.Frame_Width, self.Frame_Height = self.Enemy.Window.get_size()[0], 30
        self.Bar_Width, self.Bar_Height = self.Frame_Width-(self.Frame_Height//3), self.Frame_Height-(self.Frame_Height//3)
        self.Frame_x, self.Frame_y = 0, 0
        self.Bar_x, self.Bar_y = self.Frame_x+self.Frame_Height//6, self.Frame_y+self.Frame_Height//6
        self.Width_Per_Health = self.Bar_Width/self.Enemy.Health
        self.Frame = pygame.draw.rect(
            self.Enemy.Window, (255, 255, 255), 
            pygame.Rect(self.Frame_x, self.Frame_y, self.Frame_Width, self.Frame_Height)
        )
        self.Bar = pygame.draw.rect(
            self.Enemy.Window, (255, 0, 0), 
            pygame.Rect(self.Bar_x, self.Bar_y, self.Bar_Width, self.Bar_Height)
        )
    def Update(self):
        self.Frame_x, self.Frame_y = 0, 0
        self.Bar_x, self.Bar_y = self.Frame_x+self.Frame_Height//6, self.Frame_y+self.Frame_Height//6
        self.Frame = pygame.draw.rect(
            self.Enemy.Window, (255, 255, 255), 
            pygame.Rect(self.Frame_x, self.Frame_y, self.Frame_Width, self.Frame_Height)
        )
        self.Bar = pygame.draw.rect(
            self.Enemy.Window, (255, 0, 0), 
            pygame.Rect(self.Bar_x, self.Bar_y, self.Enemy.Health*self.Width_Per_Health, self.Bar_Height)
        )


#-----------------------------------------------------------------------------------------------------------------------------------------------------
#Enemy Main Control
class Enemy():
    Boss_Kinds = {
        "Angtrisent":(Angtrisent, 0.6),
        "Crimson_Balrog":(Crimson_Balrog, 0.9),
        "Cygnus":(Cygnus, 0.4),
    }
    Boss_Container = []
    def __init__(self, Game):
        self.Game = Game
        self.player = self.Game.player
        self.Window = self.player.Window

        self.Boss_Window_Locations = {
            "Center":              ( (Game.Width/2)                             , (Game.Height/2)             ),
            "Mid_Right":           ( (Game.Width-(Game.Width/4)-(Game.Width/8)) , (Game.Height/2)             ),
            "Right_Center":        ( (Game.Width-(Game.Width/4))                , (Game.Height/2)             ),
            "Right_Right":         ( (Game.Width-(Game.Width/8))                , (Game.Height/2)             ),
            "Mid_Left":            ( (Game.Width/4)+(Game.Width/8)              , (Game.Height/2)             ),
            "Left_Center":         ( (Game.Width/4)                             , (Game.Height/2)             ),
            "Left_Left":           ( (Game.Width/8)                             , (Game.Height/2)             ),

            "Top_Center":          ( (Game.Width/2)                             , (Game.Height/4)             ),
            "Top_Mid_Right":       ( (Game.Width-(Game.Width/4)-(Game.Width/8)) , (Game.Height/4)             ),
            "Top_Right_Center":    ( (Game.Width-(Game.Width/4))                , (Game.Height/4)             ),
            "Top_Right_Right":     ( (Game.Width-(Game.Width/8))                , (Game.Height/4)             ),
            "Top_Mid_Left":        ( (Game.Width/4)+(Game.Width/8)              , (Game.Height/4)             ),
            "Top_Left_Center":     ( (Game.Width/4)                             , (Game.Height/4)             ),
            "Top_Left_Left":       ( (Game.Width/8)                             , (Game.Height/4)             ),

            "Bottom_Center":       ( (Game.Width/2)                             , Game.Height-(Game.Height/4) ),
            "Bottom_Mid_Right":    ( (Game.Width-(Game.Width/4)-(Game.Width/8)) , Game.Height-(Game.Height/4) ),
            "Bottom_Right_Center": ( (Game.Width-(Game.Width/4))                , Game.Height-(Game.Height/4) ),
            "Bottom_Right_Right":  ( (Game.Width-(Game.Width/8))                , Game.Height-(Game.Height/4) ),
            "Bottom_Mid_Left":     ( (Game.Width/4)+(Game.Width/8)              , Game.Height-(Game.Height/4) ),
            "Bottom_Left_Center":  ( (Game.Width/4)                             , Game.Height-(Game.Height/4) ),
            "Bottom_Left_Left":    ( (Game.Width/8)                             , Game.Height-(Game.Height/4) ),
        }
    def Make_Boss(self, Boss_Name, x_y=None, Center=None):
        _Boss = self.Boss_Kinds[Boss_Name]
        if x_y:
            Boss = _Boss[0](
                Game=self.Game, x_y=x_y, scale=_Boss[1]*self.Game.Win_Scale, Window_Locations=self.Boss_Window_Locations, Health_Bar_Type=Boss_Health_Bar
            )
            self.Boss_Container.append(Boss)
        elif Center:
            Boss = _Boss[0](
                Game=self.Game, Center=Center, scale=_Boss[1]*self.Game.Win_Scale, Window_Locations=self.Boss_Window_Locations, Health_Bar_Type=Boss_Health_Bar
            )
            self.Boss_Container.append(Boss)
        return Boss
    def Clear_All_Enemy(self):
        self.Boss_Container = []
    def Update_All_Enemy(self):
        for Boss_idx, Boss in enumerate(self.Boss_Container):
            Boss.Update()
            for Bullet in self.player.Weapon.Bullet_Container:
                if not any(hit for hit in Bullet.Hit.values()):
                    if Boss.Detect_Hitboxes(bullet=Bullet.clone):
                        Boss.Health -= Bullet.Bullet_Damage
                        if Boss.Health <= 0:
                            Boss.Dead()
                            if self.Boss_Container:
                                self.Boss_Container.pop(Boss_idx)
                        Bullet.Hit["Enemy"] = True


