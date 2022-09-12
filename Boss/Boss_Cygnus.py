from .Boss_Attack import *
import pygame
import random
import os

# Suggest scale = 0.3
class Cygnus(Boss_Defaults):
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
            self.Health = 3000
            self.Health_Bar = Health_Bar_Type(Enemy=self)
            self.is_dead = False
            self.Looking_Left = True

            self.Environment_Counter = self.Game.Environment.Current_Scene.Event_Counter

            self.Moving_time = 60 #1 seconds
            self.Move_Counter = self.Environment_Counter #reset the Moving Counter and Environment Counter

            self.Attacking = False
            self.Attack_idx = None
            self.Bullet_Types = {
                "FireBall":Make_Bullet_Value_Dict(Bullet_Width=20, Bullet_Height=20, Bullet_Img_Name="MegaBall1", Bullet_Damage=100, Angle=0, Bullet_Degree_Rate=0, Bullet_vel=8),
                "LargeFireBall":Make_Bullet_Value_Dict(Bullet_Width=72, Bullet_Height=72, Bullet_Img_Name="MegaBall2", Bullet_Damage=100, Angle=0, Bullet_Degree_Rate=0, Bullet_vel=12),
                "CircularFireBall":Make_Bullet_Value_Dict(Bullet_Width=28, Bullet_Height=28, Bullet_Img_Name="MegaBall3", Bullet_Damage=100, Angle=0, Bullet_Degree_Rate=3, Bullet_vel=0),
            }
            self.Attack_Types = [
                Attack_2(Attacker=self, Bullet_Type="FireBall", Attack_Route=[False, ("Right_Center", "Left_Center")], Repeat=6, Continue=120),
                Attack_3(Attacker=self, Bullet_Type="LargeFireBall", Attack_Route=[False, ("Top_Right_Center", "Top_Left_Center"), ("Bottom_Right_Center", "Bottom_Left_Center")], Repeat=8, Continue=0),
                Attack_4(Attacker=self, Bullet_Type="CircularFireBall", Attack_Route=[False, ("Mid_Right", "Mid_Left")], Repeat=2, Continue=360),
                Cygnus_Exclusive_Attack_1(Attacker=self, Attack_Route=[False, ("Top_Center", "Top_Center"), ("Top_Left_Center", "Top_Left_Center"), ("Top_Right_Center", "Top_Left_Center")], Repeat=1, Continue=240),
            ]
            self.Bullet_Container = []
        else:
            raise BaseException("Spawning a Boss required one argument either x_y or Center")

    def Init_Images(self, x_y, Center, scale):
        self.Imgs = [
            pygame.image.load(os.path.join("assets", "Enemy", "Boss", "Cygnus", "Cygnus.png"))
        ]
        self.Imgs[0] = pygame.transform.scale(
            self.Imgs[0], (int(self.Imgs[0].get_size()[0]*scale), int(self.Imgs[0].get_size()[1]*scale))
        )
        
        self.Width, self.Height = self.Imgs[0].get_size()
        self.Change_Img_Frame_Counter, self.Change_Img_Frame_Num, self.idx = 0, 18, 0

        self.Set_Position(x_y=x_y, Center=Center)

        self.Imgs_position = [(self.x, self.y)]*len(self.Imgs)
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
            print(f"\r{self.idx}", end="")

    def Get_Position(self): #return (Top_Border, Bottom_Border, Left_Border, Right_Border, Center_x, Center_y)
        info = ((self.y), (self.y+self.Height), (self.x), (self.x+self.Width), (self.x+(self.Width/2)), (self.y+(self.Height/2)))
        return info

    def Dead(self):
        self.is_dead = True
        self.Game.Loot_System.Make_Boss_Approval(Spawn_Center=self.Center)

    def Draw(self):
        self.Looking_Left = True if self.Center[0] > self.player.Center[0] else False

        self.clone = self.Window.blit(
            pygame.transform.flip(
                self.Imgs[self.idx], not self.Looking_Left, False
            ), self.Imgs_position[self.idx]
        )
        self.Health_Bar.Update()

    def Set_Position(self, x_y=None, Center=None):
        if x_y:
            self.x, self.y = x_y
        elif Center:
            self.x, self.y = self.Convert_Center_to_xy(Center=Center)
        self.Imgs_position = [(self.x, self.y)]*len(self.Imgs)

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
                self.Self_To_Player_Slope = self.Game.Get_Slope(A=self.Center, B=self.player.Center)
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
            if self.Game.Check_Collided(A=self.Game.player.clone, B=bullet.clone):
                self.player.Health -= bullet.Bullet_Damage
            if New_Bullet_x > self.Game.Width or New_Bullet_x < 0 or New_Bullet_y > self.Game.Height or New_Bullet_y < 0:
                self.Bullet_Container.pop(idx)






# Boss Exclusive Attack pattern
class Cygnus_Exclusive_Attack_1_Bullet():
    def __init__(self, Attacker, x, y, s):
        #Image init
        self.x, self.y = x, y
        self.Window = Attacker.Window
        self.Pre_Attack_img = pygame.image.load(
            os.path.join("assets", "Enemy", "Bullet", "Cygnus_Exclusive", "Blast1.png")
        )
        self.Attack_img = pygame.image.load(
            os.path.join("assets", "Enemy", "Bullet", "Cygnus_Exclusive", "Blast2.png")
        )
        self.Counter = 0

        self.Random_Scale = random.randint(2, 5)/10

        self.Pre_Attack_img = self.Rescale_Img(img=self.Pre_Attack_img, scale=self.Random_Scale)
        self.Attack_img = self.Rescale_Img(img=self.Attack_img, scale=self.Random_Scale)

        #Bullet value
        self.Bullet_Damage = 100

    def Rescale_Img(self, img, scale):
        original_scale = img.get_size()
        return pygame.transform.scale(
            img, (int(original_scale[0]*scale), int(original_scale[1]*scale))
        )

    def Update(self):
        if self.Counter >= 120:
            self.clone = self.Window.blit(  
                self.Attack_img, (self.x-(self.Attack_img.get_size()[0]/2), self.y-self.Attack_img.get_size()[1])
            )
            self.Base = self.Window.blit(
                self.Pre_Attack_img, (self.x-(self.Pre_Attack_img.get_size()[0]/2), self.y-self.Pre_Attack_img.get_size()[1])
            )
        elif self.Counter >= 300:
            return -1, -1, True
        else:
            self.clone = self.Window.blit(  
                self.Pre_Attack_img, (self.x-(self.Pre_Attack_img.get_size()[0]/2), self.y-self.Pre_Attack_img.get_size()[1])
            )
        self.Counter += 1
        return 1, 1


# Cygnus Exculsive Attacks
class Cygnus_Exclusive_Attack_1():
    def __init__(self, Attacker, Attack_Route, Repeat, Continue):
        self.Boss = Attacker     
        self.Attacking = self.Moving = self.Moving_Back = False
        self.Move_Counter = self.Boss.Environment_Counter #reset the Moving Counter and Environment Counter

        self.Follow = True if Attack_Route[0] else False
        
        self.Attack_Spot_Center = [ #(attack position when player on boss's left side , Attack position when player on boss's right side)
            (self.Boss.Boss_Window_Locations[Attack_Spot_Nick_Name[0]], self.Boss.Boss_Window_Locations[Attack_Spot_Nick_Name[1]])
            for Attack_Spot_Nick_Name in Attack_Route[1:]
        ] * Repeat

        self.Repeat = Repeat
        self._Repeat = Repeat

        self.Continue = Continue
        self._Continue = Continue

    def Start_Attack(self):
        if not self.Moving and not self.Attacking and not self.Moving_Back:
            _Attack_Center = self.Attack_Spot_Center[1 if (self.Repeat%2)==0 else 0][0 if self.Boss.Looking_Left else 1]
            self.Boss.Moving_To = self.Boss.Convert_Center_to_xy(Center=(
                    _Attack_Center[0],
                    _Attack_Center[1] if not self.Follow else self.Boss.Game.player.y
                )
            )
            self.Moving = True
            self.Attacking = False

            self.Move_Counter = self.Boss.Environment_Counter #reset the Move_Counter to Environment Counter

        if self.Moving and not self.Attacking and not self.Moving_Back:
            self.Moving = self.Boss.Move(Special_Moving_time=None)
            if not self.Moving:
                self.Attacking = True
                
                self.Move_Counter = self.Boss.Environment_Counter #reset the Move_Counter to Environment Counter

        if not self.Moving and self.Attacking and not self.Moving_Back:
            self.Attacking = self.Attack()

            if not self.Attacking:
                self.Repeat -= 1
                if self.Repeat == 0:
                    self.Repeat = self._Repeat #reset the Repeat Counter
                    self.Moving_Back = not self.Attacking
                    self.Boss.Moving_To = self.Boss.Convert_Center_to_xy(Center=self.Boss.Boss_Window_Locations["Center"])
                    
                    self.Move_Counter = self.Boss.Environment_Counter #reset the Move_Counter to Environment Counter

        if not self.Moving and not self.Attacking and self.Moving_Back:
            self.Continue -= 1
            if len(self.Boss.Bullet_Container)==0 or self.Continue == 0:
                self.Continue = self._Continue
                self.Boss.Bullet_Container = []
                self.Moving_Back = self.Boss.Move(Special_Moving_time=None)
                if not self.Moving_Back:
                    return False
            else:
                self.Move_Counter = self.Boss.Environment_Counter #reset the Move_Counter to Environment Counter
        return True
    def Attack(self):
        self.Boss.Bullet_Container.append(
            Cygnus_Exclusive_Attack_1_Bullet(Attacker=self.Boss, x=100, y=self.Boss.Game.Height, s=0.1),
        )
        self.Boss.Bullet_Container.append(
            Cygnus_Exclusive_Attack_1_Bullet(Attacker=self.Boss, x=200, y=self.Boss.Game.Height, s=0.1),
        )
        self.Boss.Bullet_Container.append(
            Cygnus_Exclusive_Attack_1_Bullet(Attacker=self.Boss, x=300, y=self.Boss.Game.Height, s=0.6),
        )
        self.Boss.Bullet_Container.append(
            Cygnus_Exclusive_Attack_1_Bullet(Attacker=self.Boss, x=400, y=self.Boss.Game.Height, s=0.5),
        )
        self.Boss.Bullet_Container.append(
            Cygnus_Exclusive_Attack_1_Bullet(Attacker=self.Boss, x=500, y=self.Boss.Game.Height, s=0.4),
        )
        self.Boss.Bullet_Container.append(
            Cygnus_Exclusive_Attack_1_Bullet(Attacker=self.Boss, x=600, y=self.Boss.Game.Height, s=0.3),
        )
        self.Boss.Bullet_Container.append(
            Cygnus_Exclusive_Attack_1_Bullet(Attacker=self.Boss, x=700, y=self.Boss.Game.Height, s=0.2),
        )
        self.Boss.Bullet_Container.append(
            Cygnus_Exclusive_Attack_1_Bullet(Attacker=self.Boss, x=800, y=self.Boss.Game.Height, s=0.1),
        )
        self.Boss.Bullet_Container.append(
            Cygnus_Exclusive_Attack_1_Bullet(Attacker=self.Boss, x=900, y=self.Boss.Game.Height, s=0.1),
        )
        return False

