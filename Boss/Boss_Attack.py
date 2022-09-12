from math import sin, tan, cos, radians
import random
import pygame
import time
import os


#Boss Defaults
class Boss_Defaults():
    def __init__(self, Game, Window_Locations):
        self.Game = Game
        self.player = self.Game.player
        self.Window = self.Game.Window

        self.Modes = {
            "Show_Hitbox":False
        }
        
        self.Boss_Window_Locations = Window_Locations
        
        self.Moving_To = ()
        self.Move_Rate = ()

    def _Get_Position(self): #return (Top_Border, Bottom_Border, Left_Border, Right_Border, Center_x, Center_y)
        info = ((self.y), (self.y+self.Height), (self.x), (self.x+self.Width), (self.x+(self.Width/2)), (self.y+(self.Height/2)))
        return info

    def _Dead(self):
        self.is_dead = True
        self.Game.Loot_System.Make_Boss_Approval(Spawn_Center=self.Center)

    def _Convert_Center_to_xy(self, Center):
        return (
            Center[0]-(self.Width/2),
            Center[1]-(self.Height/2)
        )

    def _Convert_xy_to_Center(self, x_y):
        return (
            x_y[0]+(self.Width/2),
            x_y[1]+(self.Height/2)
        )







def Make_Bullet_Value_Dict(Bullet_Width, Bullet_Height, Bullet_Img_Name, Bullet_Damage, Angle, Bullet_Degree_Rate, Bullet_vel):
    return {
        "Bullet_Width":Bullet_Width, 
        "Bullet_Height":Bullet_Height, 
        "Bullet_Img_Name":Bullet_Img_Name, 
        "Bullet_Damage":Bullet_Damage, 
        "Bullet_vel":Bullet_vel,
        "Angle":Angle,
        "Bullet_Degree_Rate":Bullet_Degree_Rate
    }



#Boss Attack Use Bullets
class Boss_Bullet_Defaults():
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
                self.Center[0]+(cos(radians(self.Angle))*self.Radius)+(self.Bullet_vel/(((self.Bullet_Slope**2)+1)**(1/2)))-(self.Bullet_Width/2), 
                self.Center[1]+(sin(radians(self.Angle))*self.Radius)+(self.Bullet_Slope*(self.Bullet_vel/(((self.Bullet_Slope**2)+1)**(1/2))))-(self.Bullet_Height/2)
            )
        )
        return self.Center

class Boss_Bullet(Boss_Bullet_Defaults):
    def __init__(self, Bullet_Shooter, window, Bullet_Value_Dict, Bullet_Slope, Radius, Looking_Left):
        super().__init__(
            Bullet_Shooter=Bullet_Shooter,
            Bullet_Width=Bullet_Value_Dict["Bullet_Width"], 
            Bullet_Height=Bullet_Value_Dict["Bullet_Height"], 
            Bullet_Img_Name=Bullet_Value_Dict["Bullet_Img_Name"], 
            Bullet_Damage=Bullet_Value_Dict["Bullet_Damage"], 
            Bullet_vel=Bullet_Value_Dict["Bullet_vel"],
            Angle=Bullet_Value_Dict["Angle"],
            Bullet_Degree_Rate=Bullet_Value_Dict["Bullet_Degree_Rate"]
        )
        self.Update = super()._Update

        self.Window = window
        
        self.Bullet_vel = self.Bullet_vel if not Looking_Left else -self.Bullet_vel
        self.Bullet_Slope = Bullet_Slope

        self.Angle = self.Angle if not Looking_Left else -self.Angle
        self.Bullet_Degree_Rate = self.Bullet_Degree_Rate if not Looking_Left else -self.Bullet_Degree_Rate
        self.Radius = Radius

        self.x, self.y = (
            Bullet_Shooter.x + Bullet_Shooter.Width+(self.Bullet_Width/2) if not Looking_Left else Bullet_Shooter.x - (self.Bullet_Width/2), 
            Bullet_Shooter.Center[1] - (self.Bullet_Height/2)
        )

        self.Center = (
            self.x + (self.Bullet_Width/2),
            self.y + (self.Bullet_Height/2)
        )

        self.clone = self.Window.blit(
            self.Bullet_Img, 
            (self.x, self.y)
        )

    def Special_VFX(self):
        pass





#Boss Attack Types
class Boss_Attack_Defaults():
    def __init__(self, Attacker, Bullet_Type, Attack_Route, Repeat, Continue):
        self.Boss = Attacker     
        self.Attacking = self.Moving = self.Moving_Back = False
        self.Move_Counter = self.Boss.Environment_Counter #reset the Moving Counter and Environment Counter

        self.Follow = True if Attack_Route[0] else False


        
        self.Attack_Spot_Center = [ #(attack position when player on boss's left side , Attack position when player on boss's right side)
            (self.Boss.Boss_Window_Locations[Attack_Spot_Nick_Name[0]], self.Boss.Boss_Window_Locations[Attack_Spot_Nick_Name[1]])
            for Attack_Spot_Nick_Name in Attack_Route[1:]
        ]

        self.Bullet = self.Boss.Bullet_Types[Bullet_Type]

        self.Repeat = Repeat
        self._Repeat = Repeat

        self.Continue = Continue
        self._Continue = Continue

    def _Start_Attack(self):
        if not self.Moving and not self.Attacking and not self.Moving_Back:
            _Attack_Center = self.Attack_Spot_Center[self.Repeat%len(self.Attack_Spot_Center)][0 if self.Boss.Looking_Left else 1]
            self.Boss.Moving_To = self.Boss.Convert_Center_to_xy(Center=(
                    _Attack_Center[0],
                    _Attack_Center[1] if not self.Follow else self.Boss.player.y
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
            if self.Boss.Game.Check_Collided(A=self.Boss.clone, B=self.Boss.player.clone):
                self.Boss.Looking_Left = not self.Boss.Looking_Left
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
            if len(self.Boss.Bullet_Container)==0 or self.Continue <= 0:
                self.Continue = self._Continue
                self.End_Attack()
                self.Moving_Back = self.Boss.Move(Special_Moving_time=None)
                if not self.Moving_Back:
                    return False
            else:
                self.Move_Counter = self.Boss.Environment_Counter #reset the Move_Counter to Environment Counter
        return True



class Attack_1(Boss_Attack_Defaults): #Sector bullet fired Seperatly
    def __init__(self, Attacker, Bullet_Type, Attack_Route, Repeat, Continue):
        super().__init__(Attacker=Attacker, Bullet_Type=Bullet_Type, Attack_Route=Attack_Route, Repeat=Repeat, Continue=Continue)
        self.Start_Attack = super()._Start_Attack
        self.id = 1
    def End_Attack(self):
        pass
    def Attack(self):
        Attack_Stage_Cooldown = 6 # 1/10 seconds
        Slope_Rate = 0.15
        Counter = self.Boss.Environment_Counter-self.Move_Counter
        Judgment = (self.Boss.Self_To_Player_Slope+(Slope_Rate*7))-(((Counter%90)/Attack_Stage_Cooldown)*Slope_Rate) >= (self.Boss.Self_To_Player_Slope-(Slope_Rate*7))
        if Counter%Attack_Stage_Cooldown == 0 and Judgment:
            current_bullet_slope = (self.Boss.Self_To_Player_Slope+(Slope_Rate*7))-(((Counter%90)/Attack_Stage_Cooldown)*Slope_Rate)
            current_bullet_slope = current_bullet_slope if self.Boss.Looking_Left else -current_bullet_slope
            self.Boss.Bullet_Container.append(
                Boss_Bullet(
                    Bullet_Shooter=self.Boss, 
                    window=self.Boss.Window, 
                    Bullet_Value_Dict=self.Bullet, 
                    Bullet_Slope=current_bullet_slope,
                    Radius=0,
                    Looking_Left=self.Boss.Looking_Left
                )
            )
        elif Counter >= 270 and not Judgment:
            return False
        return True


class Attack_2(Boss_Attack_Defaults): #Sector bullet fired at once
    def __init__(self, Attacker, Bullet_Type, Attack_Route, Repeat, Continue):
        super().__init__(Attacker=Attacker, Bullet_Type=Bullet_Type, Attack_Route=Attack_Route, Repeat=Repeat, Continue=Continue)
        self.Start_Attack = super()._Start_Attack
        self.id = 2
    def End_Attack(self):
        pass
    def Attack(self):
        Angle_Rate = 15
        for ang in range(0, 180, Angle_Rate):
            self.Boss.Bullet_Container.append(
                Boss_Bullet(
                    Bullet_Shooter=self.Boss, 
                    window=self.Boss.Window, 
                    Bullet_Value_Dict=self.Bullet, 
                    Bullet_Slope=tan(radians(ang)),
                    Radius=0,
                    Looking_Left=self.Boss.Looking_Left
                )
            )
        return False


class Attack_3(Boss_Attack_Defaults): #Fire a bullet towards the player's position
    def __init__(self, Attacker, Bullet_Type, Attack_Route, Repeat, Continue):
        super().__init__(Attacker=Attacker, Bullet_Type=Bullet_Type, Attack_Route=Attack_Route, Repeat=Repeat, Continue=Continue)
        self.Start_Attack = super()._Start_Attack
        self.id = 3
    def End_Attack(self):
        pass
    def Attack(self):
        Boss_Fire_Position = (
            self.Boss.x if self.Boss.Looking_Left else self.Boss.x+self.Boss.Width, 
            self.Boss.Center[1]
        )
        Bullet_Slope = self.Boss.Game.Get_Slope(A=Boss_Fire_Position, B=self.Boss.player.Center)
        self.Boss.Bullet_Container.append(
            Boss_Bullet(
                Bullet_Shooter=self.Boss, 
                window=self.Boss.Window, 
                Bullet_Value_Dict=self.Bullet, 
                Bullet_Slope=Bullet_Slope,
                Radius=0,
                Looking_Left=self.Boss.Looking_Left
            )
        )
        return False


class Attack_4(Boss_Attack_Defaults): #Ring Around the Rosie
    def __init__(self, Attacker, Bullet_Type, Attack_Route, Repeat, Continue):
        super().__init__(Attacker=Attacker, Bullet_Type=Bullet_Type, Attack_Route=Attack_Route, Repeat=Repeat, Continue=Continue)
        self.Start_Attack = super()._Start_Attack
        self.id = 4
    def End_Attack(self):
        self.Boss.Bullet_Container = []
    def Attack(self):
        Looking_Left = True
        self.Boss.Bullet_Container=[
            Boss_Bullet(
                Bullet_Shooter=self.Boss, 
                window=self.Boss.Window, 
                Bullet_Value_Dict=self.Bullet, 
                Bullet_Slope=self.Boss.Self_To_Player_Slope,
                Radius=-100,
                Looking_Left=Looking_Left
            ),
            Boss_Bullet(
                Bullet_Shooter=self.Boss, 
                window=self.Boss.Window, 
                Bullet_Value_Dict=self.Bullet, 
                Bullet_Slope=self.Boss.Self_To_Player_Slope,
                Radius=-200,
                Looking_Left=Looking_Left
            ),
            Boss_Bullet(
                Bullet_Shooter=self.Boss, 
                window=self.Boss.Window, 
                Bullet_Value_Dict=self.Bullet, 
                Bullet_Slope=self.Boss.Self_To_Player_Slope,
                Radius=-300,
                Looking_Left=Looking_Left
            ),
            Boss_Bullet(
                Bullet_Shooter=self.Boss, 
                window=self.Boss.Window, 
                Bullet_Value_Dict=self.Bullet, 
                Bullet_Slope=self.Boss.Self_To_Player_Slope,
                Radius=-400,
                Looking_Left=Looking_Left
            ),
            Boss_Bullet(
                Bullet_Shooter=self.Boss, 
                window=self.Boss.Window, 
                Bullet_Value_Dict=self.Bullet, 
                Bullet_Slope=self.Boss.Self_To_Player_Slope,
                Radius=-500,
                Looking_Left=Looking_Left
            ),
            Boss_Bullet(
                Bullet_Shooter=self.Boss, 
                window=self.Boss.Window, 
                Bullet_Value_Dict=self.Bullet, 
                Bullet_Slope=self.Boss.Self_To_Player_Slope,
                Radius=-600,
                Looking_Left=Looking_Left
            ),
            Boss_Bullet(
                Bullet_Shooter=self.Boss, 
                window=self.Boss.Window, 
                Bullet_Value_Dict=self.Bullet, 
                Bullet_Slope=self.Boss.Self_To_Player_Slope,
                Radius=-700,
                Looking_Left=Looking_Left
            ),
            Boss_Bullet(
                Bullet_Shooter=self.Boss, 
                window=self.Boss.Window, 
                Bullet_Value_Dict=self.Bullet, 
                Bullet_Slope=self.Boss.Self_To_Player_Slope,
                Radius=100,
                Looking_Left=Looking_Left
            ),
            Boss_Bullet(
                Bullet_Shooter=self.Boss, 
                window=self.Boss.Window, 
                Bullet_Value_Dict=self.Bullet, 
                Bullet_Slope=self.Boss.Self_To_Player_Slope,
                Radius=200,
                Looking_Left=Looking_Left
            ),
            Boss_Bullet(
                Bullet_Shooter=self.Boss, 
                window=self.Boss.Window, 
                Bullet_Value_Dict=self.Bullet, 
                Bullet_Slope=self.Boss.Self_To_Player_Slope,
                Radius=300,
                Looking_Left=Looking_Left
            ),
            Boss_Bullet(
                Bullet_Shooter=self.Boss, 
                window=self.Boss.Window, 
                Bullet_Value_Dict=self.Bullet, 
                Bullet_Slope=self.Boss.Self_To_Player_Slope,
                Radius=400,
                Looking_Left=Looking_Left
            ),
            Boss_Bullet(
                Bullet_Shooter=self.Boss, 
                window=self.Boss.Window, 
                Bullet_Value_Dict=self.Bullet, 
                Bullet_Slope=self.Boss.Self_To_Player_Slope,
                Radius=500,
                Looking_Left=Looking_Left
            ),
            Boss_Bullet(
                Bullet_Shooter=self.Boss, 
                window=self.Boss.Window, 
                Bullet_Value_Dict=self.Bullet, 
                Bullet_Slope=self.Boss.Self_To_Player_Slope,
                Radius=600,
                Looking_Left=Looking_Left
            ),
            Boss_Bullet(
                Bullet_Shooter=self.Boss, 
                window=self.Boss.Window, 
                Bullet_Value_Dict=self.Bullet, 
                Bullet_Slope=self.Boss.Self_To_Player_Slope,
                Radius=700,
                Looking_Left=Looking_Left
            )
        ]
        return False



































