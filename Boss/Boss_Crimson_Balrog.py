from .Boss_Attack import *
import pygame
import random
import os

class Crimson_Balrog(Boss_Defaults):
    def __init__(self, Game, scale, Window_Locations, Health_Bar_Type, x_y=None, Center=None):
        if x_y or Center:
            #Boss Image Init
            super().__init__(Game=Game, Window_Locations=Window_Locations)
            self.Dead = super()._Dead
            self.Get_Position = super()._Get_Position
            self.Convert_Center_to_xy = super()._Convert_Center_to_xy
            self.Convert_xy_to_Center = super()._Convert_xy_to_Center

            self.Init_Images(x_y=None, Center=Window_Locations["Center"], scale=scale)

            #Boss Values
            self.Health = 1000
            self.Health_Bar = Health_Bar_Type(Enemy=self)
            self.is_dead = False
            self.Looking_Left = True

            self.Environment_Counter = self.Game.Environment.Current_Scene.Event_Counter

            self.Moving_time = 60 #1 seconds
            self.Move_Counter = self.Environment_Counter #reset the Moving Counter and Environment Counter

            self.Attacking = False
            self.Attack_idx = None
            self.Bullet_Types = {
                "FireBall":Make_Bullet_Value_Dict(Bullet_Width=20, Bullet_Height=20, Bullet_Img_Name="FireBall", Bullet_Damage=100, Angle=0, Bullet_Degree_Rate=0, Bullet_vel=5),
                "LargeFireBall":Make_Bullet_Value_Dict(Bullet_Width=72, Bullet_Height=72, Bullet_Img_Name="FireBall", Bullet_Damage=100, Angle=0, Bullet_Degree_Rate=0, Bullet_vel=7),
                "CircularFireBall":Make_Bullet_Value_Dict(Bullet_Width=28, Bullet_Height=28, Bullet_Img_Name="FireBall", Bullet_Damage=100, Angle=0, Bullet_Degree_Rate=3, Bullet_vel=0)
            }
            self.Attack_Types = [
                Attack_1(Attacker=self, Bullet_Type="FireBall", Attack_Route=[False, ("Right_Right", "Left_Left")], Repeat=1, Continue=0),
                Attack_2(Attacker=self, Bullet_Type="FireBall", Attack_Route=[False, ("Right_Center", "Left_Center")], Repeat=1, Continue=0),
                Attack_3(Attacker=self, Bullet_Type="LargeFireBall", Attack_Route=[False, ("Top_Right_Center", "Top_Left_Center"), ("Bottom_Right_Center", "Bottom_Left_Center")], Repeat=8, Continue=0),
                Attack_4(Attacker=self, Bullet_Type="CircularFireBall", Attack_Route=[False, ("Mid_Right", "Mid_Left")], Repeat=1, Continue=240),
            ]
            self.Bullet_Container = []
        else:
            raise BaseException("Spawning a Boss required one argument either x_y or Center")

    def Init_Images(self, x_y, Center, scale):
        self.Imgs = [
            pygame.image.load(os.path.join("assets", "Enemy", "Boss", "Crimson_Balrog", "1.png")),
            pygame.image.load(os.path.join("assets", "Enemy", "Boss", "Crimson_Balrog", "2.png"))
        ]
        self.Imgs[0] = pygame.transform.scale(
            self.Imgs[0], (int(self.Imgs[0].get_size()[0]*scale), int(self.Imgs[0].get_size()[1]*scale))
        )
        
        self.Width, self.Height = self.Imgs[0].get_size()
        self.Change_Img_Frame_Counter, self.Change_Img_Frame_Num, self.idx = 0, 18, 0

        self.Set_Position(x_y=x_y, Center=Center)

        self.Imgs_position = [
            (self.x, self.y),
            (self.x, self.y+(self.Imgs[0].get_size()[1]/10*4))
        ]
        self.Center = self.Convert_xy_to_Center(x_y=(self.x, self.y))

        for idx, img in enumerate(self.Imgs[1:]):
            img_size = img.get_size()
            rate = self.Width/img_size[0]
            self.Imgs[idx+1] = pygame.transform.scale(
                img, (int(img_size[0]*rate), int(img_size[1]*rate))
            )
        self.clone = self.Window.blit(
            self.Imgs[self.idx], self.Imgs_position[self.idx]
        )

    def Update_Image_id(self):
        self.Change_Img_Frame_Counter += 1
        if self.Change_Img_Frame_Counter%self.Change_Img_Frame_Num == 0:
            self.idx += 1
            if self.idx >= len(self.Imgs):
                self.idx = 0

    def Get_Position(self): #return (Top_Border, Bottom_Border, Left_Border, Right_Border, Center_x, Center_y)
        info = ((self.y), (self.y+self.Height), (self.x), (self.x+self.Width), (self.x+(self.Width/2)), (self.y+(self.Height/2)))
        return info

    def Dead(self):
        self.is_dead = True
        self.Game.Loot_System.Make_Boss_Approval(Spawn_Center=self.Center)

    def Draw(self):
        self.clone = self.Window.blit(
            self.Imgs[self.idx], self.Imgs_position[self.idx]
        )
        self.Health_Bar.Update()

    def Set_Position(self, x_y=None, Center=None):
        if x_y:
            self.x, self.y = x_y
        elif Center:
            self.x, self.y = self.Convert_Center_to_xy(Center=Center)
        self.Imgs_position = [
            (self.x, self.y),
            (self.x, self.y+(self.Imgs[0].get_size()[1]/10*4))
        ]

    def Convert_Center_to_xy(self, Center):
        return (
            Center[0]-(self.Width/2),
            Center[1]-(self.Height/2)
        )

    def Convert_xy_to_Center(self, x_y):
        return (
            x_y[0]+(self.Width/2),
            x_y[1]+(self.Height/2)
        )

    def Move(self, Special_Moving_time=None):
        if ( any(Attack_Type.Moving for Attack_Type in self.Attack_Types) or any(Attack_Type.Moving_Back for Attack_Type in self.Attack_Types) ) and self.Moving_To:
            if not self.Move_Rate:
                self.Move_Counter = self.Environment_Counter #reset the Moving Counter and Environment Counter
                if Special_Moving_time:
                    self.Move_Rate = (
                        (self.Moving_To[0]-self.x) / Special_Moving_time,
                        (self.Moving_To[1]-self.y) / Special_Moving_time,
                    )
                else:
                    self.Move_Rate = (
                        (self.Moving_To[0]-self.x) / self.Moving_time,
                        (self.Moving_To[1]-self.y) / self.Moving_time,
                    )
            self.Set_Position(x_y=(self.x+self.Move_Rate[0], self.y+self.Move_Rate[1]))
            if self.Environment_Counter-self.Move_Counter >= (Special_Moving_time if Special_Moving_time else self.Moving_time):
                self.Set_Position(x_y=self.Moving_To)
                self.Moving_To = self.Move_Rate = ()
                self.Move_Counter = self.Environment_Counter #reset the Moving Counter and Environment Counter
                self.Self_To_Player_Slope = self.Game.Get_Slope(A=self.Get_Position()[4:], B=self.player.Get_Position()[4:])
                return False
        return True

    def Control_Attack(self):
        if self.Environment_Counter%500==0 and not self.Attacking:
            self.Attack_idx = random.randrange(0, len(self.Attack_Types))
            self.Attacking = True
        elif self.Attacking:
            self.Attacking = self.Attack_Types[self.Attack_idx].Start_Attack()

    def Update(self):
        self.Environment_Counter = self.Game.Environment.Current_Scene.Event_Counter
        self.Update_Image_id()
        self.Control_Attack()

        self.Center = self.Convert_xy_to_Center(x_y=self.Imgs_position[0])
        
        self.Draw()

        for idx, bullet in enumerate(self.Bullet_Container):
            New_Bullet_x, New_Bullet_y = bullet.Update()
            if self.Game.Check_Collided(A=self.player.clone, B=bullet.clone):
                self.player.Health -= 100
            if New_Bullet_x > self.Game.Width or New_Bullet_x < 0 or New_Bullet_y > self.Game.Height or New_Bullet_y < 0:
                self.Bullet_Container.pop(idx)

        if self.Game.Check_Collided(A=self.player.clone, B=self.clone):
                self.player.Health -= 100
        
    
