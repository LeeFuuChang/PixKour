from math import sin, cos, radians
from .Boss_Attack import *
import pygame
import random
import os

class Angtrisent(Boss_Defaults):
    def __init__(self, Game, scale, Window_Locations, Health_Bar_Type, x_y=None, Center=None):
        #Boss Image Init
        super().__init__(Game=Game, Window_Locations=Window_Locations)
        self.Dead = super()._Dead
        self.Get_Position = super()._Get_Position
        self.Convert_Center_to_xy = super()._Convert_Center_to_xy
        self.Convert_xy_to_Center = super()._Convert_xy_to_Center
        
        #Timers
        self.Game.Event_Timer.Make_Event(Event_Name="Angtrisent_Attack", Time=10)
        
        #Initialize Images
        self.Init_Images(x_y=x_y, Center=Center, scale=scale)

        #Boss Values
        self.Health = 1000
        self.Health_Bar = Health_Bar_Type(Enemy=self)
        self.is_dead = False

        self.Environment_Counter = self.Game.Environment.Current_Scene.Event_Counter

        self.Moving_time = 60 #1 seconds
        self.Move_Counter = self.Environment_Counter #reset the Moving Counter and Environment Counter

        #Attack Properties
        self.Attacking = False
        self.Attack_idx = 0
        self.Attack_Types = [
            Sword_Wall_Attack(Game=self.Game)
        ]
        self.Bullet_Container = []
        self.Modes["Show_Hitbox"] = True

    def Init_Images(self, x_y, Center, scale):
        first_Imgs_size = pygame.image.load(os.path.join("assets", "Enemy", "Boss", "Angtrisent", f"Idle1.png")).get_size()
        
        #Rescaling the Image
        self.Width, self.Height = int(first_Imgs_size[0]*scale), int(first_Imgs_size[1]*scale)

        self.Change_Img_Frame_Counter, self.Change_Img_Frame_Num, self.idx = 0, 6, 2

        #Set Position / Update x,y and center coordnate 
        self.Set_Position(x_y=x_y, Center=Center)
        self.Center = self.Convert_xy_to_Center(x_y=(self.x, self.y))

        #Defining all Image and Hitboxes
        pixel_w, pixel_h = self.Width/96, self.Height/113
        self.Idle_Imgs = [ #[Img, [(hitbox_x, hitbox_y, hitbox_w, hitbox_h)]] // hitbox_xy = self.xy + img_xy_drift + hitbox_xy_drift
            [
                pygame.transform.scale(
                    pygame.image.load(os.path.join("assets", "Enemy", "Boss", "Angtrisent", "Idle1.png")), (self.Width, self.Height)
                ), [
                    (self.x +(pixel_w*8)               , self.y +(pixel_h*27)              , int(pixel_w*9) , int(pixel_h*19)),
                    (self.x +(pixel_w*8)  +(pixel_w*72), self.y +(pixel_h*27)              , int(pixel_w*9) , int(pixel_h*19)),
                    (self.x +(pixel_w*8)  +(pixel_w*9) , self.y +(pixel_h*27) +(pixel_h*13), int(pixel_w*10), int(pixel_h*7) ),
                    (self.x +(pixel_w*8)  +(pixel_w*62), self.y +(pixel_h*27) +(pixel_h*13), int(pixel_w*10), int(pixel_h*7) ),
                    (self.x +(pixel_w*8)  +(pixel_w*2) , self.y +(pixel_h*27) +(pixel_h*19), int(pixel_w*77), int(pixel_h*9) ),
                    (self.x +(pixel_w*8)  +(pixel_w*9) , self.y +(pixel_h*27) +(pixel_h*28), int(pixel_w*63), int(pixel_h*8) ),
                    (self.x +(pixel_w*8)  +(pixel_w*35), self.y +(pixel_h*27) +(pixel_h*36), int(pixel_w*10), int(pixel_h*22))
                ]
            ], [
                pygame.transform.scale(
                    pygame.image.load(os.path.join("assets", "Enemy", "Boss", "Angtrisent", "Idle2.png")), (self.Width, self.Height)
                ), [
                    (self.x                            , self.y +(pixel_h*40)              , int(pixel_w*15), int(pixel_h*33)),
                    (self.x              +(pixel_w*44) , self.y +(pixel_h*40) +(pixel_h*7) , int(pixel_w*7) , int(pixel_h*6) ),
                    (self.x              +(pixel_w*15) , self.y +(pixel_h*40) +(pixel_h*13), int(pixel_w*66), int(pixel_h*19)),
                    (self.x              +(pixel_w*81) , self.y +(pixel_h*40)              , int(pixel_w*15), int(pixel_h*33)),
                    (self.x              +(pixel_w*45) , self.y +(pixel_h*40) +(pixel_h*32), int(pixel_w*8) , int(pixel_h*11))
                ]
            ], [
                pygame.transform.scale(
                    pygame.image.load(os.path.join("assets", "Enemy", "Boss", "Angtrisent", "Idle3.png")), (self.Width, self.Height)
                ), [
                    (self.x +(pixel_w*29) +(pixel_w*15), self.y +(pixel_h*46)              , int(pixel_w*7) , int(pixel_h*7) ),
                    (self.x +(pixel_w*29) +(pixel_w*8) , self.y +(pixel_h*46) +(pixel_h*7) , int(pixel_w*22), int(pixel_h*7) ),
                    (self.x +(pixel_w*29) +(pixel_w*5) , self.y +(pixel_h*46) +(pixel_h*14), int(pixel_w*27), int(pixel_h*15)),
                    (self.x +(pixel_w*29)              , self.y +(pixel_h*46) +(pixel_h*29), int(pixel_w*37), int(pixel_h*12)),
                    (self.x +(pixel_w*29) +(pixel_w*3) , self.y +(pixel_h*46) +(pixel_h*41), int(pixel_w*11), int(pixel_h*11)),
                    (self.x +(pixel_w*29) +(pixel_w*23), self.y +(pixel_h*46) +(pixel_h*41), int(pixel_w*11), int(pixel_h*11))
                ]
            ], [
                pygame.transform.scale(
                    pygame.image.load(os.path.join("assets", "Enemy", "Boss", "Angtrisent", "Idle4.png")), (self.Width, self.Height)
                ), [
                    (self.x +(pixel_w*25)              , self.y +(pixel_h*46) +(pixel_h*6) , int(pixel_w*8) , int(pixel_h*39)),
                    (self.x +(pixel_w*25) +(pixel_w*8) , self.y +(pixel_h*46)              , int(pixel_w*30), int(pixel_h*47)),
                    (self.x +(pixel_w*25) +(pixel_w*38), self.y +(pixel_h*46) +(pixel_h*6) , int(pixel_w*8) , int(pixel_h*39))
                ]
            ], [
                pygame.transform.scale(
                    pygame.image.load(os.path.join("assets", "Enemy", "Boss", "Angtrisent", "Idle5.png")), (self.Width, self.Height)
                ), [
                    (self.x +(pixel_w*5)  +(pixel_w*9) , self.y +(pixel_h*45)              , int(pixel_w*68), int(pixel_h*15)),
                    (self.x +(pixel_w*5)  +(pixel_w*2) , self.y +(pixel_h*45) +(pixel_h*15), int(pixel_w*82), int(pixel_h*12)),
                    (self.x +(pixel_w*5)               , self.y +(pixel_h*45) +(pixel_h*27), int(pixel_w*22), int(pixel_h*9) ),
                    (self.x +(pixel_w*5)  +(pixel_w*39), self.y +(pixel_h*45) +(pixel_h*27), int(pixel_w*9) , int(pixel_h*12)),
                    (self.x +(pixel_w*5)  +(pixel_w*64), self.y +(pixel_h*45) +(pixel_h*27), int(pixel_w*22), int(pixel_h*9) ),
                    (self.x +(pixel_w*5)  +(pixel_w*4) , self.y +(pixel_h*45) +(pixel_h*36), int(pixel_w*3) , int(pixel_h*4) ),
                    (self.x +(pixel_w*5)  +(pixel_w*10), self.y +(pixel_h*45) +(pixel_h*36), int(pixel_w*6) , int(pixel_h*9) ),
                    (self.x +(pixel_w*5)  +(pixel_w*70), self.y +(pixel_h*45) +(pixel_h*36), int(pixel_w*6) , int(pixel_h*9) ),
                    (self.x +(pixel_w*5)  +(pixel_w*79), self.y +(pixel_h*45) +(pixel_h*36), int(pixel_w*3) , int(pixel_h*4) )
                ]
            ], [
                pygame.transform.scale(
                    pygame.image.load(os.path.join("assets", "Enemy", "Boss", "Angtrisent", "Idle6.png")), (self.Width, self.Height)
                ), [
                    (self.x +(pixel_w*6)               , self.y +(pixel_h*35)              , int(pixel_w*84), int(pixel_h*34)),
                    (self.x +(pixel_w*6)  +(pixel_w*38), self.y +(pixel_h*35) +(pixel_h*34), int(pixel_w*8) , int(pixel_h*22))
                ]
            ], [
                pygame.transform.scale(
                    pygame.image.load(os.path.join("assets", "Enemy", "Boss", "Angtrisent", "Idle7.png")), (self.Width, self.Height)
                ), [
                    (self.x +(pixel_w*12)              , self.y +(pixel_h*1)               , int(pixel_w*18), int(pixel_h*42)),
                    (self.x +(pixel_w*12) +(pixel_w*54), self.y +(pixel_h*1)               , int(pixel_w*18), int(pixel_h*42)),
                    (self.x +(pixel_w*12) +(pixel_w*18), self.y +(pixel_h*1)  +(pixel_h*23), int(pixel_w*13), int(pixel_h*19)),
                    (self.x +(pixel_w*12) +(pixel_w*41), self.y +(pixel_h*1)  +(pixel_h*23), int(pixel_w*13), int(pixel_h*19)),
                    (self.x +(pixel_w*12) +(pixel_w*7) , self.y +(pixel_h*1)  +(pixel_h*42), int(pixel_w*24), int(pixel_h*10)),
                    (self.x +(pixel_w*12) +(pixel_w*41), self.y +(pixel_h*1)  +(pixel_h*42), int(pixel_w*24), int(pixel_h*10)),
                    (self.x +(pixel_w*12) +(pixel_w*15), self.y +(pixel_h*1)  +(pixel_h*52), int(pixel_w*17), int(pixel_h*11)),
                    (self.x +(pixel_w*12) +(pixel_w*40), self.y +(pixel_h*1)  +(pixel_h*52), int(pixel_w*17), int(pixel_h*11)),
                    (self.x +(pixel_w*12) +(pixel_w*32), self.y +(pixel_h*1)  +(pixel_h*56), int(pixel_w*8) , int(pixel_h*39))
                ]
            ], [
                pygame.transform.scale(
                    pygame.image.load(os.path.join("assets", "Enemy", "Boss", "Angtrisent", "Idle8.png")), (self.Width, self.Height)
                ), [
                    (self.x +(pixel_w*14)              , self.y                            , int(pixel_w*26), int(pixel_h*48)),
                    (self.x +(pixel_w*14) +(pixel_w*43), self.y                            , int(pixel_w*26), int(pixel_h*48)),
                    (self.x +(pixel_w*14) +(pixel_w*26), self.y               +(pixel_h*32), int(pixel_w*17), int(pixel_h*16)),
                    (self.x +(pixel_w*14) +(pixel_w*7) , self.y               +(pixel_h*48), int(pixel_w*25), int(pixel_h*10)),
                    (self.x +(pixel_w*14) +(pixel_w*37), self.y               +(pixel_h*48), int(pixel_w*25), int(pixel_h*10)),
                    (self.x +(pixel_w*14) +(pixel_w*18), self.y               +(pixel_h*58), int(pixel_w*12), int(pixel_h*17)),
                    (self.x +(pixel_w*14) +(pixel_w*38), self.y               +(pixel_h*58), int(pixel_w*13), int(pixel_h*19)),
                    (self.x +(pixel_w*14) +(pixel_w*30), self.y               +(pixel_h*59), int(pixel_w*8) , int(pixel_h*37))
                ]
            ]
        ]
        self.Attack_Imgs = [ #[Img, [(hitbox_x, hitbox_y, hitbox_w, hitbox_h)]] // hitbox_xy = self.xy + img_xy_drift + hitbox_xy_drift
            [
                pygame.transform.scale(
                    pygame.image.load(os.path.join("assets", "Enemy", "Boss", "Angtrisent", "Attack1.png")), (self.Width, self.Height)
                ), [
                    (self.x +(pixel_w*7)               , self.y +(pixel_h*20)              , int(pixel_w*26), int(pixel_h*32)),
                    (self.x +(pixel_w*7)  +(pixel_w*56), self.y +(pixel_h*20)              , int(pixel_w*26), int(pixel_h*32)),
                    (self.x +(pixel_w*7)  +(pixel_w*26), self.y +(pixel_h*20) +(pixel_h*22), int(pixel_w*30), int(pixel_h*10)),
                    (self.x +(pixel_w*7)  +(pixel_w*5) , self.y +(pixel_h*20) +(pixel_h*32), int(pixel_w*72), int(pixel_h*7) ),
                    (self.x +(pixel_w*7)  +(pixel_w*16), self.y +(pixel_h*20) +(pixel_h*39), int(pixel_w*50), int(pixel_h*5) ),
                    (self.x +(pixel_w*7)  +(pixel_w*29), self.y +(pixel_h*20) +(pixel_h*44), int(pixel_w*24), int(pixel_h*7) ),
                    (self.x +(pixel_w*7)  +(pixel_w*37), self.y +(pixel_h*20) +(pixel_h*51), int(pixel_w*8) , int(pixel_h*23))
                ]
            ], [
                pygame.transform.scale(
                    pygame.image.load(os.path.join("assets", "Enemy", "Boss", "Angtrisent", "Attack2.png")), (self.Width, self.Height)
                ), [
                    (self.x +(pixel_w*7)               , self.y +(pixel_h*20)              , int(pixel_w*26), int(pixel_h*32)),
                    (self.x +(pixel_w*7)  +(pixel_w*56), self.y +(pixel_h*20)              , int(pixel_w*26), int(pixel_h*32)),
                    (self.x +(pixel_w*7)  +(pixel_w*26), self.y +(pixel_h*20) +(pixel_h*22), int(pixel_w*30), int(pixel_h*10)),
                    (self.x +(pixel_w*7)  +(pixel_w*4) , self.y +(pixel_h*20) +(pixel_h*32), int(pixel_w*74), int(pixel_h*7) ),
                    (self.x +(pixel_w*7)  +(pixel_w*16), self.y +(pixel_h*20) +(pixel_h*39), int(pixel_w*50), int(pixel_h*5) ),
                    (self.x +(pixel_w*7)  +(pixel_w*29), self.y +(pixel_h*20) +(pixel_h*44), int(pixel_w*24), int(pixel_h*4) ),
                    (self.x +(pixel_w*7)  +(pixel_w*38), self.y +(pixel_h*20) +(pixel_h*48), int(pixel_w*6) , int(pixel_h*26))
                ]
            ], [
                pygame.transform.scale(
                    pygame.image.load(os.path.join("assets", "Enemy", "Boss", "Angtrisent", "Attack3.png")), (self.Width, self.Height)
                ), [
                    (self.x +(pixel_w*7)               , self.y +(pixel_h*20)              , int(pixel_w*26), int(pixel_h*32)),
                    (self.x +(pixel_w*7)  +(pixel_w*56), self.y +(pixel_h*20)              , int(pixel_w*26), int(pixel_h*32)),
                    (self.x +(pixel_w*7)  +(pixel_w*26), self.y +(pixel_h*20) +(pixel_h*22), int(pixel_w*30), int(pixel_h*10)),
                    (self.x +(pixel_w*7)  +(pixel_w*4) , self.y +(pixel_h*20) +(pixel_h*32), int(pixel_w*74), int(pixel_h*7) ),
                    (self.x +(pixel_w*7)  +(pixel_w*16), self.y +(pixel_h*20) +(pixel_h*39), int(pixel_w*50), int(pixel_h*5) ),
                    (self.x +(pixel_w*7)  +(pixel_w*29), self.y +(pixel_h*20) +(pixel_h*44), int(pixel_w*24), int(pixel_h*7) ),
                    (self.x +(pixel_w*7)  +(pixel_w*38), self.y +(pixel_h*20) +(pixel_h*51), int(pixel_w*6) , int(pixel_h*23))
                ]
            ]
        ]

        #set Idle images as default images
        self.Imgs = self.Idle_Imgs

        #Draw Image onto the screen
        self.clone = self.Window.blit(
            self.Imgs[self.idx][0], (self.x, self.y)
        )
    
    def Set_Position(self, x_y=None, Center=None):
        if x_y:
            self.x, self.y = x_y[0]*self.Game.Win_Scale, x_y[1]*self.Game.Win_Scale
        elif Center:
            CenterToXY = self.Convert_Center_to_xy(Center=Center)
            self.x, self.y = CenterToXY[0]*self.Game.Win_Scale, CenterToXY[1]*self.Game.Win_Scale

    def Detect_Hitboxes(self, bullet):
        for hitbox in self.Imgs[self.idx][1]:
            A_x, A_y, A_w, A_h = hitbox
            B_x, B_y, B_w, B_h = (bullet.x, bullet.y)+bullet.size
            Judgement = (
                (A_x <= B_x <= A_x+A_w or A_x <= B_x+B_w <= A_x+A_w) or (B_x <= A_x <= B_x+B_w or B_x <= A_x+A_w <= B_x+B_w)
                ) and (
                (A_y <= B_y <= A_y+A_h or A_y <= B_y+B_h <= A_y+A_h) or (B_y <= A_y <= B_y+B_h or B_y <= A_y+A_h <= B_y+B_h)
            )
            if Judgement:
                print("damaged")
                return True
        return False

    def Draw(self):
        self.Window.blit(
            self.Imgs[self.idx][0], (self.x, self.y)
        )
        self.Health_Bar.Update()
        if self.Modes["Show_Hitbox"]:
            for hitbox in self.Imgs[self.idx][1]:
                pygame.draw.rect(self.Window, (255, 0, 0), hitbox, 2)

    def Update_Img(self):
        if self.Attacking:
            self.Imgs = self.Attack_Imgs
        else:
            self.Imgs = self.Idle_Imgs

        self.Change_Img_Frame_Counter += 1
        if self.Change_Img_Frame_Counter%self.Change_Img_Frame_Num==0:
            self.idx += 1
        if self.idx >= len(self.Imgs):
            self.idx = 0

        self.Draw()

    def Update(self):
        self.Update_Img()

        if self.Game.Event_Timer.Get_Events()["Angtrisent_Attack"]:
            if not self.Attacking:
                self.Attacking = True
                self.Bullet_Container.extend(
                    self.Attack_Types[self.Attack_idx].Start_Attack()
                )
        elif all(not bullet.Animating for bullet in self.Bullet_Container) and all(bullet.Wait_Frame <= 0 for bullet in self.Bullet_Container):
            self.Attacking = False

        for idx, bullet in enumerate(self.Bullet_Container):
            Remove = bullet.Update(player=self.Game.player)
            if Remove:
                self.Bullet_Container.pop(idx)















class Angtrisent_Bullet_Defaults():
    def __init__(self, Bullet_Shooter, Bullet_Width, Bullet_Height, Bullet_Img_Name, Bullet_Damage, Angle, Bullet_Degree_Rate, Bullet_vel):
        self.Bullet_Width, self.Bullet_Height = Bullet_Width, Bullet_Height

        self.Bullet_Shooter = Bullet_Shooter

        self.Bullet_Img = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "Enemy", "Bullet", Bullet_Img_Name+(".png" if ".png" not in Bullet_Img_Name else ""))), (self.Bullet_Width, self.Bullet_Height)
        )
        self.Bullet_Img_Copy = self.Bullet_Img.copy()
        
        self.Bullet_vel = Bullet_vel

        self.Bullet_Damage = Bullet_Damage

        self.Angle = Angle
        self.Bullet_Degree_Rate = Bullet_Degree_Rate

    def _Update(self):
        self.Special_VFX()
        if self.Radius:
            self.Center = self.Bullet_Shooter.Center
            self.Angle += self.Bullet_Degree_Rate
        else:
            self.Center = (
                self.Center[0]+(cos(radians(self.Angle))*self.Radius)+(self.Bullet_vel/(((self.Bullet_Slope**2)+1)**(1/2))), 
                self.Center[1]+(sin(radians(self.Angle))*self.Radius)+(self.Bullet_Slope*(self.Bullet_vel/(((self.Bullet_Slope**2)+1)**(1/2))))
            )
        self.clone = self.Window.blit(  
            self.Bullet_Img, 
            (
                self.Center[0]+(cos(radians(self.Angle))*self.Radius)+(self.Bullet_vel/(((self.Bullet_Slope**2)+1)**(1/2)))-self.Bullet_Width, 
                self.Center[1]+(sin(radians(self.Angle))*self.Radius)+(self.Bullet_Slope*(self.Bullet_vel/(((self.Bullet_Slope**2)+1)**(1/2))))-self.Bullet_Height
            )
        )
        return self.Center




class Orb_Attack_Orb():
    def __init__(self, Center, player):
        self.target = player
        self.Window = player.Window

        self.Bullet_Width, self.Bullet_Height = 100, 100

        self.Center = Center
        
        self.x, self.y = self.Center[0]-(self.Bullet_Width/2), self.Center[1]-(self.Bullet_Height/2)

        self.Bullet_Slope = (self.Center[1]-self.target.Center[1]) / (self.Center[0]-self.target.Center[0])

        self.Bullet_vel = 7
        self.Bullet_Damage = 0

        self.Going = (self.Center[0] >= self.target.Center[0], self.Center[0] < self.target.Center[0])
        if self.Going[1]:
            self.Bullet_Slope = -self.Bullet_Slope

        self.Imgs = [
            pygame.transform.scale(
                pygame.image.load(
                    os.path.join("assets", "Enemy", "Boss", "Angtrisent", "Orb_Attack", f"{i}.png")
                ), (self.Bullet_Width, self.Bullet_Height)
            ) for i in range(1, 15)
        ]

        self.Change_Img_Frame_Counter, self.Change_Img_Frame_Num, self.idx = 0, 6, 0
        self.GO = False

    def Update_Image_id(self):
        self.Change_Img_Frame_Counter += 1
        if self.Change_Img_Frame_Counter%self.Change_Img_Frame_Num == 0 and not self.GO:
            self.idx += 1
            if self.idx >= len(self.Imgs)-1:
                self.GO = True
    
    def Update(self):
        self.Update_Image_id()
        if self.GO:
            if (self.Going[1] and self.Center[0]<self.target.Center[0]+(self.target.Charactor_Width*3)) or (self.Going[0] and self.Center[0]>=self.target.Center[0]+(self.target.Charactor_Width*3)):
                self.Bullet_Slope = ((self.Center[1]-self.target.Center[1]) / (self.Center[0]-self.target.Center[0]))
            if (self.Center[0] < self.target.Center[0] and self.Bullet_vel<0) or (self.Center[0] > self.target.Center[0] and self.Bullet_vel>0):
                self.Bullet_vel = -self.Bullet_vel
            self.Center = (
                self.Center[0]+(self.Bullet_vel/(((self.Bullet_Slope**2)+1)**(1/2))), 
                self.Center[1]+(self.Bullet_Slope*(self.Bullet_vel/(((self.Bullet_Slope**2)+1)**(1/2))))
            )
        self.clone = self.Window.blit(  
            self.Imgs[self.idx], 
            (
                self.Center[0]-(self.Bullet_Width/2), 
                self.Center[1]-(self.Bullet_Height/2)
            )
        )
        return self.Center

class Orb_Attack():
    def __init__(self, Game):
        #Base Values
        self.Game = Game
        self.Window = self.Game.Window
        self.player = self.Game.player






class Sword_Rain_Attack_Sword():
    def __init__(self, Game, Sword_Center_Positions, Wait_Frame):
        #Base Values
        self.Game = Game
        self.Window = self.Game.Window
        self.player = self.Game.player

        #Image Values
        self.Scaling = self.Game.Width/64/15
        self.Sword_Center_Positions = Sword_Center_Positions
        self.Sword_Width, self.Sword_Height = int(15*self.Scaling), int(122*self.Scaling)
        self.imgs = [
            pygame.transform.scale(
                pygame.image.load(
                    os.path.join("assets", "Enemy", "Boss", "Angtrisent", "Sword_Rain_Attack", f"{i}.png")
                ), (self.Sword_Width, self.Sword_Height)
            ) for i in range(1, 8)
        ]

        #Bullet Values
        self.Remove_After_Hit = False
        self.Sword_vel = 8*self.Game.Win_Scale
        self.Bullet_Damage = 100
        self.Change_Img_Frame_Counter, self.Change_Img_Frame_Num, self.idx = 0, 4, 0
        self.Wait_Frame = Wait_Frame
        self.Animating = True

    def Update_Image_id(self):
        self.Change_Img_Frame_Counter += 1
        if self.Change_Img_Frame_Counter%self.Change_Img_Frame_Num == 0:
            self.idx += 1
            if self.idx >= len(self.imgs)-1:
                self.Animating = False

    def Update(self, player):
        #If Animation Ended and also Wait time finished then start to move the bullet
        if self.Animating:
            self.Update_Image_id()
        elif self.Wait_Frame > 0:
            self.Wait_Frame -= 1
        else:
            for center_id, center in enumerate(self.Sword_Center_Positions):
                self.Sword_Center_Positions[center_id] = (center[0], center[1]+self.Sword_vel)

        #Draw / Update Swords and Check if any sword hit the player
        for Center in self.Sword_Center_Positions:
            sword = self.Window.blit(
                self.imgs[self.idx], 
                (Center[0]-(self.Sword_Width/2), Center[1]-(self.Sword_Height/2)) 
            )
            if self.Game.Check_Collided(A=sword, B=player.clone) and not self.Animating:
                player.Health -= self.Bullet_Damage

        #Return True to delete bullet if the bullet is out of the screen
        if self.Sword_Center_Positions[0][1] >= self.Game.Width: 
            return True
        return False


class Sword_Rain_Attack():
    def __init__(self, Game):
        #Base Values
        self.Game = Game
        self.Window = self.Game.Window
        self.player = self.Game.player

    def Start_Attack(self): #Return Bullets as a List
        Swords = []
        Sword_Gap = (self.Game.Width/10)
        for Wave in range(5): #Create 5 Waves/Groups of Swords
            Center = ((self.Game.Width/20)*random.randint(0, 1), self.Game.Height/4)
            Swords.append(
                Sword_Rain_Attack_Sword(
                    Game=self.Game, 
                    Sword_Center_Positions=[(Center[0]+(Sword_Gap*Shift_amount), Center[1]) for Shift_amount in range(12)], 
                    Wait_Frame=40*(Wave+1)
                )
            )
        return Swords





class Sword_Wall_Attack_Sword():
    def __init__(self, Game, Sword_Center_Positions, Wait_Frame, ToLeft):
        #Base Values
        self.Game = Game
        self.Window = self.Game.Window
        self.player = self.Game.player

        #Image Values
        self.Scaling = self.Game.Height/48/15
        self.Sword_Center_Positions = Sword_Center_Positions
        self.Sword_Width, self.Sword_Height = int(122*self.Scaling), int(15*self.Scaling)
        self.imgs = [
            pygame.transform.scale(
                pygame.image.load(
                    os.path.join("assets", "Enemy", "Boss", "Angtrisent", "Sword_Wall_Attack", ("Left" if ToLeft else "Right")+f"-{i}.png")
                ), (self.Sword_Width, self.Sword_Height)
            ) for i in range(1, 8)
        ]

        #Bullet Values
        self.Remove_After_Hit = False
        self.Sword_vel = 12*self.Game.Win_Scale
        self.Sword_vel = -self.Sword_vel if ToLeft else self.Sword_vel
        self.Bullet_Damage = 100
        self.Change_Img_Frame_Counter, self.Change_Img_Frame_Num, self.idx = 0, 4, 0
        self.Wait_Frame = Wait_Frame
        self.Animating = True

    def Update_Image_id(self):
        self.Change_Img_Frame_Counter += 1
        if self.Change_Img_Frame_Counter%self.Change_Img_Frame_Num == 0:
            self.idx += 1
            if self.idx >= len(self.imgs)-1:
                self.Animating = False

    def Update(self, player):
        #If Animation Ended and also Wait time finished then start to move the bullet
        if self.Animating:
            self.Update_Image_id()
        elif self.Wait_Frame > 0:
            self.Wait_Frame -= 1
        else:
            for center_id, center in enumerate(self.Sword_Center_Positions):
                self.Sword_Center_Positions[center_id] = (center[0]+self.Sword_vel, center[1])

        #Draw / Update Swords and Check if any sword hit the player
        for Center in self.Sword_Center_Positions:
            sword = self.Window.blit(
                self.imgs[self.idx], 
                (Center[0]-(self.Sword_Width/2), Center[1]-(self.Sword_Height/2)) 
            )
            # if self.Game.Check_Collided(A=sword, B=player.clone) and not self.Animating:
            #     player.Health -= self.Bullet_Damage

        #Return True to delete bullet if the bullet is out of the screen
        if self.Sword_Center_Positions[0][1] >= self.Game.Width: 
            return True
        return False


class Sword_Wall_Attack():
    def __init__(self, Game):
        #Base Values
        self.Game = Game
        self.Window = self.Game.Window
        self.player = self.Game.player

    def Start_Attack(self): #Return Bullets as a List
        ToLeft = random.randint(0, 1)
        Swords = []
        Sword_Gap = (self.Game.Height/7.5)
        for Wave in range(3): #Create 3 Waves/Groups of Swords
            Center = (self.Game.Width-(self.Game.Width/16) if ToLeft else self.Game.Width/16, (self.Game.Height/30))
            Sword_Center_Positions = []
            for Shift_amount in range(12):
                Sword_Center_Positions.append((Center[0], Center[1]+(Sword_Gap*Shift_amount)))
                if Shift_amount%2:
                    Sword_Center_Positions.append((Center[0], Center[1]+(Sword_Gap*Shift_amount)+(Sword_Gap/2)))
            Swords.append(
                Sword_Wall_Attack_Sword(
                    Game=self.Game, 
                    Sword_Center_Positions=Sword_Center_Positions, 
                    Wait_Frame=60*(Wave+1),
                    ToLeft=ToLeft
                )
            )
        return Swords




