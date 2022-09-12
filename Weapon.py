from math import sin, cos, radians
import pygame
import os


class Bullet_Defaults():
    def __init__(self, Bullet_Width, Bullet_Height, Bullet_Img_Name, Bullet_Damage, Angle, Radius, Bullet_Degree_Rate, Bullet_vel, Bullet_Slope):
        self.Bullet_Width, self.Bullet_Height = Bullet_Width, Bullet_Height

        self.Bullet_Img = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "Bullet", Bullet_Img_Name+(".png" if ".png" not in Bullet_Img_Name else ""))), (self.Bullet_Width, self.Bullet_Height)
        )
        self.Bullet_Img_Copy = self.Bullet_Img.copy()
        
        self.Bullet_vel = Bullet_vel
        self.Bullet_Slope = Bullet_Slope

        self.Bullet_Damage = Bullet_Damage

        self.Angle = Angle
        self.Radius = Radius
        self.Bullet_Degree_Rate = Bullet_Degree_Rate

        self.Hit = {"Enemy":False, "Environment":False}

    def _Update(self):
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
        self.Special_VFX()
        return self.Center[0], self.Center[1], self.Hit

class Weapon_Defaults():
    """
    Max_Bullet_Per_Shot =>  Max Bullets Every fire, 0=No Limit
    Shotfire_Cooldown =>    Cooldown between Bullets
    Shoot_Cooldown =>       Cooldown between every fire
    """
    def __init__(self, Game, Max_Bullet_On_Screen, Max_Bullet_Per_Shot, Shotfire_Cooldown, Shoot_Cooldown, Bullet, Weapon_Name):
        self.Game = Game
        
        self.player = Game.player

        self.Window = Game.Window
        self.Win_Width, self.Win_Height = self.Window.get_size()

        self.Bullet_Container = []

        self.Shooting = False

        self.Max_Bullet_Per_Shot = Max_Bullet_Per_Shot
        self.Bullet_Counter = 0 

        self.Max_Bullet_On_Screen = Max_Bullet_On_Screen
        self._Max_Bullet_On_Screen = Max_Bullet_On_Screen

        self.Shotfire_Cooldown = Shotfire_Cooldown
        self._Shotfire_Cooldown = 0
        
        self.Shoot_Cooldown = Shoot_Cooldown
        self._Shoot_Cooldown = 0

        self.Bullet = Bullet

        self.Holding_Img_Width, self.Holding_Img_Height = self.player.Charactor_Width//6*5, self.player.Charactor_Height//6*5
        self.Holding_Img = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "Weapon", Weapon_Name, f"{Weapon_Name}-Holding.png")), (self.Holding_Img_Width, self.Holding_Img_Height)
        )

    def _Draw_Holding(self):
        self.Weapon_VFX()
        self.Window.blit(
            pygame.transform.flip(self.Holding_Img, self.player.state["Looking_Left"],  False), (
                self.player.x+self.player.Charactor_Width-(self.Holding_Img_Width/2) if not self.player.state["Looking_Left"] else self.player.x-(self.Holding_Img_Width/2), 
                self.player.y+(self.Holding_Img_Width/6)
            )
        )

    def _Shoot(self):
        if (self.Max_Bullet_On_Screen > 0 and len(self.Bullet_Container) < self._Max_Bullet_On_Screen) or self.Max_Bullet_On_Screen<0:
            if self._Shoot_Cooldown > 0:
                self._Shoot_Cooldown -= 1

            if self.Shooting and self._Shotfire_Cooldown <= 0 and self.Bullet_Counter < self.Max_Bullet_Per_Shot:
                self.Spawn_Bullet()
                self._Shotfire_Cooldown = self.Shotfire_Cooldown
                if self.Max_Bullet_Per_Shot:
                    self.Bullet_Counter += 1
                    if self.Bullet_Counter >= self.Max_Bullet_Per_Shot:
                        self.Shooting = False
                        self.Bullet_Counter = 0
                        self._Shoot_Cooldown = self.Shoot_Cooldown
            elif self._Shotfire_Cooldown > 0:
                self._Shotfire_Cooldown -= 1

    def _Update(self):
        self.Handle_Bullets()

#-----------------------------------------------------------------------------------------------------------------------------------------------------
""" Weapon & Bullet Stuffs """
# Default Weapon
class SnowBall_Bullet(Bullet_Defaults):
    def __init__(self, Game, Slope, Looking_Left):
        super().__init__(
            Bullet_Width=int(12*Game.Win_Scale), 
            Bullet_Height=int(12*Game.Win_Scale), 
            Bullet_Damage=2,
            Angle=0, 
            Radius=0, 
            Bullet_Degree_Rate=0,
            Bullet_Img_Name="SnowBall", 
            Bullet_vel=10*Game.Win_Scale, 
            Bullet_Slope=Slope
        )
        self.Update = super()._Update

        self.Window = Game.Window
        self.player = Game.player

        self.Bullet_vel = self.Bullet_vel if not Looking_Left else -self.Bullet_vel
        
        self.Bullet_Img = pygame.transform.flip(self.Bullet_Img, Looking_Left, False)

        self.x, self.y = (
            self.player.x + self.player.Charactor_Width if not Looking_Left else self.player.x, 
            self.player.y + (self.player.Charactor_Height//2) - (self.Bullet_Height//2)
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

class SnowBall_Gun(Weapon_Defaults): 
    ID = "SnowBall_Gun"
    Loot_Type = "Weapon"
    Loot_Img=pygame.image.load(os.path.join("assets", "Weapon", "SnowBall_Gun", "SnowBall_Gun.png"))
    NameTag_Img = pygame.image.load(os.path.join("assets", "Weapon", "SnowBall_Gun", "SnowBall_Gun-NameTag.png"))
    def __init__(self, Game):
        super().__init__(
            Game=Game,
            Max_Bullet_On_Screen=-1,
            Max_Bullet_Per_Shot=5, 
            Shotfire_Cooldown=1, 
            Shoot_Cooldown=36, 
            Bullet=SnowBall_Bullet,
            Weapon_Name="SnowBall_Gun"
        )
        self.Shoot = super()._Shoot
        self.Update = super()._Update
        self.Draw_Holding = super()._Draw_Holding

    def Spawn_Bullet(self):
        self.Bullet_Container.append(
            self.Bullet(Game=self.Game, Slope=0, Looking_Left=self.player.state["Looking_Left"])
        )

    def Weapon_VFX(self):
        pass

    def Handle_Bullets(self):
        for idx, bullet in enumerate(self.Bullet_Container):
            New_Bullet_x, New_Bullet_y, Remove = bullet.Update()
            if New_Bullet_x > self.Win_Width or New_Bullet_x < 0 or New_Bullet_y > self.Win_Height or New_Bullet_y < 0 or any(hit for hit in bullet.Hit.values()):
                self.Bullet_Container.pop(idx)



#Shuriken
class Shuriken_Bullet(Bullet_Defaults):
    def __init__(self, Game, Slope, Looking_Left):
        super().__init__(
            Bullet_Width=int(20*Game.Win_Scale), 
            Bullet_Height=int(20*Game.Win_Scale), 
            Bullet_Damage=1,
            Angle=0, 
            Radius=0, 
            Bullet_Degree_Rate=0,
            Bullet_Img_Name="Shuriken", 
            Bullet_vel=8*Game.Win_Scale, 
            Bullet_Slope=Slope
        )
        self.Update = super()._Update

        self.Window = Game.Window
        self.player = Game.player

        self.Bullet_vel = self.Bullet_vel if not Looking_Left else -self.Bullet_vel
        
        self.Bullet_Img = pygame.transform.flip(self.Bullet_Img, Looking_Left, False)

        self.x, self.y = (
            self.player.x + self.player.Charactor_Width if not Looking_Left else self.player.x, 
            self.player.y + (self.player.Charactor_Height//2) - (self.Bullet_Height//2)
        )

        self.Center = (
            self.x + (self.Bullet_Width/2),
            self.y + (self.Bullet_Height/2)
        )

        self.clone = self.Window.blit(
            self.Bullet_Img, 
            (self.x, self.y)
        )

        #Special arguments
        self.rotate_angle = 0

    def Special_VFX(self):
        self.rotate_angle += 12
        if self.rotate_angle >= 360:
            self.rotate_angle -= 360
        self.Bullet_Img = pygame.transform.rotate(self.Bullet_Img_Copy, -self.rotate_angle)

class Shuriken(Weapon_Defaults):
    ID = "Shuriken"
    Loot_Type = "Weapon"
    Loot_Img = pygame.image.load(os.path.join("assets", "Weapon", "Shuriken", "Shuriken.png"))
    NameTag_Img = pygame.image.load(os.path.join("assets", "Weapon", "Shuriken", "Shuriken-NameTag.png"))
    def __init__(self, Game):
        super().__init__(
            Game=Game,
            Max_Bullet_On_Screen=-1,
            Max_Bullet_Per_Shot=1, 
            Shotfire_Cooldown=5, 
            Shoot_Cooldown=5, 
            Bullet=Shuriken_Bullet,
            Weapon_Name="Shuriken"
        )
        self.Shoot = super()._Shoot
        self.Update = super()._Update
        self.Draw_Holding = super()._Draw_Holding

    def Spawn_Bullet(self):
        self.Bullet_Container.append(
            self.Bullet(Game=self.Game, Slope=0, Looking_Left=self.player.state["Looking_Left"])
        )

    def Weapon_VFX(self):
        pass

    def Handle_Bullets(self):
        for idx, bullet in enumerate(self.Bullet_Container):
            New_Bullet_x, New_Bullet_y, Remove = bullet.Update()
            if New_Bullet_x > self.Win_Width or New_Bullet_x < 0 or New_Bullet_y > self.Win_Height or New_Bullet_y < 0 or any(hit for hit in bullet.Hit.values()):
                self.Bullet_Container.pop(idx)



#Xueshang
class Xueshang_Bullet(Bullet_Defaults):
    def __init__(self, Game, Slope, Looking_Left):
        super().__init__(
            Bullet_Width=int(25*Game.Win_Scale), 
            Bullet_Height=int(40*Game.Win_Scale), 
            Bullet_Damage=1,
            Angle=0, 
            Radius=0, 
            Bullet_Degree_Rate=0, 
            Bullet_Img_Name="Xueshang", 
            Bullet_vel=8*Game.Win_Scale, 
            Bullet_Slope=Slope
        )
        self.Update = super()._Update

        self.Window = Game.Window
        self.player = Game.player

        self.Bullet_vel = self.Bullet_vel if not Looking_Left else -self.Bullet_vel
        
        self.Bullet_Img = pygame.transform.flip(self.Bullet_Img, Looking_Left, False)

        self.x, self.y = (
            self.player.x + self.player.Charactor_Width if not Looking_Left else self.player.x, 
            self.player.y + (self.player.Charactor_Height//2) - (self.Bullet_Height//2)
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

class Xueshang(Weapon_Defaults):
    ID = "Xueshang"
    Loot_Type = "Weapon"
    Loot_Img = pygame.image.load(os.path.join("assets", "Weapon", "Xueshang", "Xueshang.png"))
    NameTag_Img = pygame.image.load(os.path.join("assets", "Weapon", "Xueshang", "Xueshang-NameTag.png"))
    def __init__(self, Game):
        super().__init__(
            Game=Game,
            Max_Bullet_On_Screen=-1,
            Max_Bullet_Per_Shot=5, 
            Shotfire_Cooldown=3, 
            Shoot_Cooldown=36, 
            Bullet=Xueshang_Bullet,
            Weapon_Name="Xueshang"
        )
        self.Shoot = super()._Shoot
        self.Update = super()._Update
        self.Draw_Holding = super()._Draw_Holding

    def Spawn_Bullet(self):
        self.Bullet_Container.extend(
            [
                self.Bullet(Game=self.Game, Slope=+(1/16), Looking_Left=self.player.state["Looking_Left"]),
                self.Bullet(Game=self.Game, Slope=-(1/16), Looking_Left=self.player.state["Looking_Left"]),
                self.Bullet(Game=self.Game, Slope=0, Looking_Left=self.player.state["Looking_Left"])
            ]
        )

    def Weapon_VFX(self):
        pass

    def Handle_Bullets(self):
        for idx, bullet in enumerate(self.Bullet_Container):
            New_Bullet_x, New_Bullet_y, Remove = bullet.Update()
            if New_Bullet_x > self.Win_Width or New_Bullet_x < 0 or New_Bullet_y > self.Win_Height or New_Bullet_y < 0 or any(hit for hit in bullet.Hit.values()):
                self.Bullet_Container.pop(idx)



#SwallowingBow
class SwallowingBow_Bullet(Bullet_Defaults):
    def __init__(self, Game, Slope, Looking_Left):
        super().__init__(
            Bullet_Width=int(60*Game.Win_Scale), 
            Bullet_Height=int(10*Game.Win_Scale), 
            Bullet_Damage=8,
            Angle=0, 
            Radius=0, 
            Bullet_Degree_Rate=0, 
            Bullet_Img_Name="SwallowingBow", 
            Bullet_vel=12*Game.Win_Scale, 
            Bullet_Slope=Slope
        )
        self.Update = super()._Update

        self.Window = Game.Window
        self.player = Game.player

        self.Bullet_vel = self.Bullet_vel if not Looking_Left else -self.Bullet_vel
        
        self.Bullet_Img = pygame.transform.flip(self.Bullet_Img, Looking_Left, False)

        self.x, self.y = (
            self.player.x + self.player.Charactor_Width if not Looking_Left else self.player.x, 
            self.player.y + (self.player.Charactor_Height//2) - (self.Bullet_Height//2)
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

class SwallowingBow(Weapon_Defaults):
    ID = "SwallowingBow"
    Loot_Type = "Weapon"
    Loot_Img = pygame.image.load(os.path.join("assets", "Weapon", "SwallowingBow", "SwallowingBow.png"))
    NameTag_Img = pygame.image.load(os.path.join("assets", "Weapon", "SwallowingBow", "SwallowingBow-NameTag.png"))
    def __init__(self, Game):
        super().__init__(
            Game=Game,
            Max_Bullet_On_Screen=-1,
            Max_Bullet_Per_Shot=1, 
            Shotfire_Cooldown=60, 
            Shoot_Cooldown=60, 
            Bullet=SwallowingBow_Bullet,
            Weapon_Name="SwallowingBow"
        )
        self.Shoot = super()._Shoot
        self.Update = super()._Update
        self.Draw_Holding = super()._Draw_Holding

    def Spawn_Bullet(self):
        self.Bullet_Container.append(
            self.Bullet(Game=self.Game, Slope=0, Looking_Left=self.player.state["Looking_Left"])
        )

    def Weapon_VFX(self):
        pass

    def Handle_Bullets(self):
        for idx, bullet in enumerate(self.Bullet_Container):
            New_Bullet_x, New_Bullet_y, Remove = bullet.Update()
            if New_Bullet_x > self.Win_Width or New_Bullet_x < 0 or New_Bullet_y > self.Win_Height or New_Bullet_y < 0 or any(hit for hit in bullet.Hit.values()):
                self.Bullet_Container.pop(idx)



#DeadStarLaserGun
'''
Need to solve wall stop laser problem
'''
class DeadStarLaserGun_Bullet(Bullet_Defaults):
    def __init__(self, player, window, Slope, Looking_Left):
        super().__init__(
            Bullet_Width=10000, 
            Bullet_Height=12, 
            Bullet_Damage=100,
            Angle=0, 
            Radius=0, 
            Bullet_Degree_Rate=0, 
            Bullet_Img_Name="DeadStarLaser", 
            Bullet_vel=0, 
            Bullet_Slope=Slope
        )

        self.Window = window
        self.player = player

        self.Bullet_vel = self.Bullet_vel if not Looking_Left else -self.Bullet_vel
        
        self.Bullet_Img = pygame.transform.flip(self.Bullet_Img, Looking_Left, False)

        self.x, self.y = (
            self.player.x + self.player.Charactor_Width if not Looking_Left else self.player.x, 
            self.player.y + (self.player.Charactor_Height//2) - (self.Bullet_Height//2)
        )

        self.Center = (
            self.x + (self.Bullet_Width/2),
            self.y + (self.Bullet_Height/2)
        )

        self.clone = self.Window.blit(
            self.Bullet_Img, 
            (self.x, self.y)
        )

        #Special arguments
        self.k = 3

    def Update(self):
        if self.k > 0:
            self.k -= 1
            self.clone = self.Window.blit(
                self.Bullet_Img, 
                (self.x, self.y)
            )
            return 1, 0, False
        else:
            return 0, 0, True

    def Special_VFX(self):
        pass

class DeadStarLaserGun(Weapon_Defaults):
    ID = "DeadStarLaserGun"
    Loot_Type = "Weapon"
    Loot_Img = pygame.image.load(os.path.join("assets", "Weapon", "DeadStarLaserGun", "DeadStarLaserGun.png"))
    NameTag_Img = pygame.image.load(os.path.join("assets", "Weapon", "DeadStarLaserGun", "DeadStarLaserGun-NameTag.png"))
    def __init__(self, player):
        super().__init__(
            player=player,
            Max_Bullet_On_Screen=1,
            Max_Bullet_Per_Shot=1, 
            Shotfire_Cooldown=60, 
            Shoot_Cooldown=60, 
            Bullet=DeadStarLaserGun_Bullet,
            Weapon_Name="DeadStarLaserGun"
        )
        self.Shoot = super()._Shoot
        self.Update = super()._Update
        self.Draw_Holding = super()._Draw_Holding

    def Spawn_Bullet(self):
        self.Bullet_Container.append(
            self.Bullet(player=self.player, window=self.Window, Slope=0, Looking_Left=self.player.state["Looking_Left"])
        )

    def Weapon_VFX(self):
        pass

    def Handle_Bullets(self):
        for idx, bullet in enumerate(self.Bullet_Container):
            New_Bullet_x, New_Bullet_y, Remove = bullet.Update()
            if New_Bullet_x > self.Win_Width or New_Bullet_x < 0 or New_Bullet_y > self.Win_Height or New_Bullet_y < 0 or Remove:
                self.Bullet_Container.pop(idx)



#XLoad
class XLoad_Bullet(Bullet_Defaults):
    def __init__(self, Game, Slope, Looking_Left):
        super().__init__(
            Bullet_Width=int(20*Game.Win_Scale), 
            Bullet_Height=int(20*Game.Win_Scale), 
            Bullet_Damage=12,
            Angle=0, 
            Radius=0, 
            Bullet_Degree_Rate=0, 
            Bullet_Img_Name="XLoad", 
            Bullet_vel=10*Game.Win_Scale, 
            Bullet_Slope=Slope
        )

        self.Window = Game.Window
        self.player = Game.player

        self.Bullet_vel = self.Bullet_vel if not Looking_Left else -self.Bullet_vel
        
        self.Bullet_Img = pygame.transform.flip(self.Bullet_Img, Looking_Left, False)

        self.x, self.y = (
            self.player.x + self.player.Charactor_Width if not Looking_Left else self.player.x, 
            self.player.y + (self.player.Charactor_Height//2) - (self.Bullet_Height//2)
        )

        self.Center = (
            self.x + (self.Bullet_Width/2),
            self.y + (self.Bullet_Height/2)
        )

        self.clone = self.Window.blit(
            self.Bullet_Img, 
            (self.x, self.y)
        )

        #Special arguments
        self.rotate_angle = 0
        self.Returning = False

    def Update(self):
        if self.Returning:
            player_Center = self.player.Get_Position()[4:]
            self.Bullet_Slope = self.player.Game.Get_Slope(A=self.Center, B=player_Center)
            if (self.Center[0] < player_Center[0] and self.Bullet_vel<0) or (self.Center[0] > player_Center[0] and self.Bullet_vel>0):
                self.Bullet_vel = -self.Bullet_vel

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
        self.Special_VFX()
        if self.player.Game.Check_Collided(A=self.clone, B=self.player.clone):
            return self.Center[0], self.Center[1], True
        return self.Center[0], self.Center[1], False

    def Special_VFX(self):
        self.rotate_angle += 12
        if self.rotate_angle >= 360:
            self.rotate_angle -= 360
        self.Bullet_Img = pygame.transform.rotate(self.Bullet_Img_Copy, -self.rotate_angle)

class XLoad(Weapon_Defaults):
    ID = "XLoad"
    Loot_Type = "Weapon"
    Loot_Img = pygame.image.load(os.path.join("assets", "Weapon", "XLoad", "XLoad.png"))
    NameTag_Img = pygame.image.load(os.path.join("assets", "Weapon", "XLoad", "XLoad-NameTag.png"))
    def __init__(self, Game):
        super().__init__(
            Game=Game,
            Max_Bullet_On_Screen=-1,
            Max_Bullet_Per_Shot=1, 
            Shotfire_Cooldown=18, 
            Shoot_Cooldown=18, 
            Bullet=XLoad_Bullet,
            Weapon_Name="XLoad"
        )
        self.Shoot = super()._Shoot
        self.Update = super()._Update
        self.Draw_Holding = super()._Draw_Holding

    def Spawn_Bullet(self):
        self.Bullet_Container.extend(
            [
                self.Bullet(Game=self.Game, Slope=+(1/16), Looking_Left=self.player.state["Looking_Left"]),
                self.Bullet(Game=self.Game, Slope=-(1/16), Looking_Left=self.player.state["Looking_Left"]),
            ]
        )

    def Weapon_VFX(self):
        pass

    def Handle_Bullets(self):
        for idx, bullet in enumerate(self.Bullet_Container):
            New_Bullet_x, New_Bullet_y, Remove = bullet.Update()
            if Remove:
                self.Bullet_Container.pop(idx)
            elif New_Bullet_x > self.Win_Width or New_Bullet_x < 0 or New_Bullet_y > self.Win_Height or New_Bullet_y < 0 or any(hit for hit in bullet.Hit.values()):
                bullet.Returning = True



#Crescendum
class Crescendum_Bullet(Bullet_Defaults):
    def __init__(self, Game, Slope, Looking_Left):
        super().__init__(
            Bullet_Width=int(20*Game.Win_Scale), 
            Bullet_Height=int(20*Game.Win_Scale), 
            Bullet_Damage=12,
            Angle=0, 
            Radius=0, 
            Bullet_Degree_Rate=0, 
            Bullet_Img_Name="Crescendum", 
            Bullet_vel=10*Game.Win_Scale, 
            Bullet_Slope=Slope
        )

        self.Window = Game.Window
        self.player = Game.player

        self.Bullet_vel = self.Bullet_vel if not Looking_Left else -self.Bullet_vel
        
        self.Bullet_Img = pygame.transform.flip(self.Bullet_Img, Looking_Left, False)

        self.x, self.y = (
            self.player.x + self.player.Charactor_Width if not Looking_Left else self.player.x, 
            self.player.y + (self.player.Charactor_Height//2) - (self.Bullet_Height//2)
        )

        self.Center = (
            self.x + (self.Bullet_Width/2),
            self.y + (self.Bullet_Height/2)
        )

        self.clone = self.Window.blit(
            self.Bullet_Img, 
            (self.x, self.y)
        )

        #Special arguments
        self.rotate_angle = 0
        self.Returning = False

    def Update(self):
        if self.Returning:
            player_Center = self.player.Get_Position()[4:]
            self.Bullet_Slope = self.player.Game.Get_Slope(A=self.Center, B=player_Center)
            if (self.Center[0] < player_Center[0] and self.Bullet_vel<0) or (self.Center[0] > player_Center[0] and self.Bullet_vel>0):
                self.Bullet_vel = -self.Bullet_vel

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
        self.Special_VFX()
        if self.player.Game.Check_Collided(A=self.clone, B=self.player.clone):
            return self.Center[0], self.Center[1], True
        return self.Center[0], self.Center[1], False

    def Special_VFX(self):
        self.rotate_angle += 12
        if self.rotate_angle >= 360:
            self.rotate_angle -= 360
        self.Bullet_Img = pygame.transform.rotate(self.Bullet_Img_Copy, -self.rotate_angle)

class Crescendum(Weapon_Defaults):
    ID = "Crescendum"
    Loot_Type = "Weapon"
    Loot_Img = pygame.image.load(os.path.join("assets", "Weapon", "Crescendum", "Crescendum.png"))
    NameTag_Img = pygame.image.load(os.path.join("assets", "Weapon", "Crescendum", "Crescendum-NameTag.png"))
    def __init__(self, Game):
        super().__init__(
            Game=Game,
            Max_Bullet_On_Screen=1,
            Max_Bullet_Per_Shot=1, 
            Shotfire_Cooldown=5, 
            Shoot_Cooldown=5, 
            Bullet=Crescendum_Bullet,
            Weapon_Name="Crescendum"
        )
        self.Shoot = super()._Shoot
        self.Update = super()._Update
        self.Draw_Holding = super()._Draw_Holding

        #Weapone VFX
        self.Max = 8
        self.Reset_Cooldown = 720 #12 seconds
        self._Reset_Cooldown = 720 #12 seconds
        self.Angle = 0
        self.Weapon_VFX_Img = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "Weapon", "Crescendum", "Crescendum.png")), (int(20*Game.Win_Scale), int(20*Game.Win_Scale))
        )
        self.Weapon_VFX_Img_Copy = self.Weapon_VFX_Img.copy()

    def Spawn_Bullet(self):
        make_bullet = [
                self.Bullet(Game=self.Game, Slope=0, Looking_Left=self.player.state["Looking_Left"]),
                # self.Bullet(player=self.player, window=self.Window, Slope=+(1/2), Looking_Left=not self.player.state["Looking_Left"]),
                # self.Bullet(player=self.player, window=self.Window, Slope=-(1/2), Looking_Left=not self.player.state["Looking_Left"]),
                # self.Bullet(player=self.player, window=self.Window, Slope=+(1/4), Looking_Left=not self.player.state["Looking_Left"]),
                # self.Bullet(player=self.player, window=self.Window, Slope=-(1/4), Looking_Left=not self.player.state["Looking_Left"]),
                # self.Bullet(player=self.player, window=self.Window, Slope=0, Looking_Left=not self.player.state["Looking_Left"]),
                # self.Bullet(player=self.player, window=self.Window, Slope=+(1/2), Looking_Left=self.player.state["Looking_Left"]),
                # self.Bullet(player=self.player, window=self.Window, Slope=-(1/2), Looking_Left=self.player.state["Looking_Left"]),
                # self.Bullet(player=self.player, window=self.Window, Slope=+(1/4), Looking_Left=self.player.state["Looking_Left"]),
                # self.Bullet(player=self.player, window=self.Window, Slope=-(1/4), Looking_Left=self.player.state["Looking_Left"])
            ]
        self.Bullet_Container.extend(
            make_bullet
        )
        self.Max_Bullet_On_Screen -= len(make_bullet)

    def Weapon_VFX(self):
        player_Center = self.player.Get_Position()[4:]
        Weapon_VFX_Img_size = self.Weapon_VFX_Img.get_size()
        for i in range(self.Max_Bullet_On_Screen):
            angle = i*(360//self.Max)+self.Angle
            angle = -angle if self.player.state["Looking_Left"] else angle
            self.Weapon_VFX_clone = self.Window.blit(  
                pygame.transform.rotate(self.Weapon_VFX_Img_Copy, self.Angle), 
                (
                    player_Center[0]+(cos(radians(-angle))*50)-(Weapon_VFX_Img_size[0]/2), 
                    player_Center[1]+(sin(radians(-angle))*50)-(Weapon_VFX_Img_size[1]/2)
                )
            )
        self.Angle += 5

    def Handle_Bullets(self):
        if self.Max_Bullet_On_Screen+len(self.Bullet_Container) <= 0:
            self.Max_Bullet_On_Screen = self._Max_Bullet_On_Screen = 1
        for idx, bullet in enumerate(self.Bullet_Container):
            New_Bullet_x, New_Bullet_y, Remove = bullet.Update()
            if Remove:
                self.Bullet_Container.pop(idx)
                self.Max_Bullet_On_Screen += 1
                if bullet.Hit["Enemy"] and self.Max_Bullet_On_Screen+len(self.Bullet_Container) < self.Max:
                    self.Max_Bullet_On_Screen += 1
                if self.Max_Bullet_On_Screen+len(self.Bullet_Container) > self._Max_Bullet_On_Screen:
                    self._Max_Bullet_On_Screen = self.Max_Bullet_On_Screen+len(self.Bullet_Container)
            elif New_Bullet_x > self.Win_Width or New_Bullet_x < 0 or New_Bullet_y > self.Win_Height or New_Bullet_y < 0 or any(hit for hit in bullet.Hit.values()):
                bullet.Returning = True



#Compassionate
class Compassionate_Bullet(Bullet_Defaults):
    def __init__(self, Game, Slope, Looking_Left):
        super().__init__(
            Bullet_Width=int(20*Game.Win_Scale), 
            Bullet_Height=int(20*Game.Win_Scale), 
            Bullet_Damage=12,
            Angle=0, 
            Radius=0, 
            Bullet_Degree_Rate=0, 
            Bullet_Img_Name="Compassionate", 
            Bullet_vel=10*Game.Win_Scale, 
            Bullet_Slope=Slope
        )

        self.Window = Game.Window
        self.player = Game.player

        self.Bullet_vel = self.Bullet_vel if not Looking_Left else -self.Bullet_vel
        
        self.Bullet_Img = pygame.transform.flip(self.Bullet_Img, Looking_Left, False)

        self.x, self.y = (
            self.player.x + self.player.Charactor_Width if not Looking_Left else self.player.x, 
            self.player.y + (self.player.Charactor_Height//2) - (self.Bullet_Height//2)
        )

        self.Center = (
            self.x + (self.Bullet_Width/2),
            self.y + (self.Bullet_Height/2)
        )

        self.clone = self.Window.blit(
            self.Bullet_Img, 
            (self.x, self.y)
        )

        #Special arguments
        self.rotate_angle = 0
        self.Returning = False

    def Update(self):
        if self.Returning:
            player_Center = self.player.Get_Position()[4:]
            self.Bullet_Slope = self.player.Game.Get_Slope(A=self.Center, B=player_Center)
            if (self.Center[0] < player_Center[0] and self.Bullet_vel<0) or (self.Center[0] > player_Center[0] and self.Bullet_vel>0):
                self.Bullet_vel = -self.Bullet_vel

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
        self.Special_VFX()
        if self.player.Game.Check_Collided(A=self.clone, B=self.player.clone):
            return self.Center[0], self.Center[1], True
        return self.Center[0], self.Center[1], False

    def Special_VFX(self):
        self.rotate_angle += 12
        if self.rotate_angle >= 360:
            self.rotate_angle -= 360
        self.Bullet_Img = pygame.transform.rotate(self.Bullet_Img_Copy, -self.rotate_angle)

class Compassionate(Weapon_Defaults):
    ID = "Compassionate"
    Loot_Type = "Weapon"
    Loot_Img = pygame.image.load(os.path.join("assets", "Weapon", "Compassionate", "Compassionate.png"))
    NameTag_Img = pygame.image.load(os.path.join("assets", "Weapon", "Compassionate", "Compassionate-NameTag.png"))
    def __init__(self, player):
        super().__init__(
            player=player,
            Max_Bullet_On_Screen=-1,
            Max_Bullet_Per_Shot=1, 
            Shotfire_Cooldown=18, 
            Shoot_Cooldown=18, 
            Bullet=Compassionate_Bullet,
            Weapon_Name="Compassionate"
        )
        self.Shoot = super()._Shoot
        self.Update = super()._Update

    def Spawn_Bullet(self):
        self.Bullet_Container.extend(
            [
                self.Bullet(player=self.player, window=self.Window, Slope=0, Looking_Left=self.player.state["Looking_Left"]),
            ]
        )

    def Draw_Holding(self):
        self.Window.blit(
            pygame.transform.flip(self.Holding_Img, self.player.state["Looking_Left"],  False), (
                self.player.x+self.player.Charactor_Width-(self.Holding_Img_Width/2) if not self.player.state["Looking_Left"] else self.player.x-(self.Holding_Img_Width/2), 
                self.player.y+(self.Holding_Img_Width/6)
            )
        )

    def Weapon_VFX(self):
        pass

    def Handle_Bullets(self):
        for idx, bullet in enumerate(self.Bullet_Container):
            New_Bullet_x, New_Bullet_y, Remove = bullet.Update()
            if Remove:
                self.Bullet_Container.pop(idx)
            elif New_Bullet_x > self.Win_Width or New_Bullet_x < 0 or New_Bullet_y > self.Win_Height or New_Bullet_y < 0 or any(hit for hit in bullet.Hit.values()):
                bullet.Returning = True















class Weapons():
    Weapon_Dict = {
        "SnowBall_Gun":SnowBall_Gun,
        "Shuriken":Shuriken,
        "Xueshang":Xueshang,
        "SwallowingBow":SwallowingBow,
        "DeadStarLaserGun":DeadStarLaserGun,
        "XLoad":XLoad,
        "Crescendum":Crescendum,
        "Compassionate":Compassionate,
    }

    SnowBall_Gun = SnowBall_Gun
    Shuriken = Shuriken
    Xueshang = Xueshang
    SwallowingBow = SwallowingBow
    DeadStarLaserGun = DeadStarLaserGun
    XLoad = XLoad
    Crescendum = Crescendum
    Compassionate = Compassionate