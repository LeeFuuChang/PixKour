import pygame
import os

class Key_Icons():
    def __init__(self, Charactor_Width, Charactor_Height):
        self.Icon_Width, self.Icon_Height = int(Charactor_Width/2), int(Charactor_Height/2)

        self.Keys = {}
        for code in range(97, 123):
            self.Keys[f"K_{chr(code)}"] = pygame.transform.scale(
                pygame.image.load(
                    os.path.join("assets", "KeyIcons", f"K_{chr(code)}.png")
                ), (self.Icon_Width, self.Icon_Height)
            )


class Font_Images():
    n_0 = pygame.image.load(
        os.path.join("assets", "Fonts", "0.png")
    )
    n_1 = pygame.image.load(
        os.path.join("assets", "Fonts", "1.png")
    )
    n_2 = pygame.image.load(
        os.path.join("assets", "Fonts", "2.png")
    )
    n_3 = pygame.image.load(
        os.path.join("assets", "Fonts", "3.png")
    )
    n_4 = pygame.image.load(
        os.path.join("assets", "Fonts", "4.png")
    )
    n_5 = pygame.image.load(
        os.path.join("assets", "Fonts", "5.png")
    )
    n_6 = pygame.image.load(
        os.path.join("assets", "Fonts", "6.png")
    )
    n_7 = pygame.image.load(
        os.path.join("assets", "Fonts", "7.png")
    )
    n_8 = pygame.image.load(
        os.path.join("assets", "Fonts", "8.png")
    )
    n_9 = pygame.image.load(
        os.path.join("assets", "Fonts", "9.png")
    )
    Number_Dict = {
        "0":n_0,
        "1":n_1,
        "2":n_2,
        "3":n_3,
        "4":n_4,
        "5":n_5,
        "6":n_6,
        "7":n_7,
        "8":n_8,
        "9":n_9,
    }


#Player Gameplay UI
class Player_Gameplay_UI():
    def __init__(self, player):
        self.player = player
        self.Game = self.player.Game
        self.Window = self.player.Window

        self.Player_Coins_UI_Surface = pygame.Surface((self.Game.Width, self.Game.Height//20))
        self.Player_Coins_UI_Surface.set_alpha(128)
        self.Player_Coins_UI_Surface.fill((0, 0, 0))

        self.Player_Coins_UI_Icon_size = (((self.Game.Height//20) - (self.Game.Height//60)), ((self.Game.Height//20) - (self.Game.Height//60)))
        
        self.Gap = (self.Game.Width//8, (self.Game.Height//60)//2)

        self.Rescale_Font_Images()

        #Coin
        self.Player_Coin_Number_String = None
        self.Coin_Icon = pygame.transform.scale(
            pygame.image.load(
                os.path.join("assets", "Textures", "Coin", "Coin.png")
            ), self.Player_Coins_UI_Icon_size
        )
        self.Coin_Icon_Position = (self.Game.Width-(self.Gap[0]*2), self.Gap[1])

        #Boss_Approval
        self.Player_Boss_Approvals_Number_String = None
        self.Boss_Approval_Icon = pygame.transform.scale(
            pygame.image.load(
                os.path.join("assets", "Textures", "Coin", "Boss_Approval.png")
            ), self.Player_Coins_UI_Icon_size
        )
        self.Boss_Approval_Icon_Position = (self.Game.Width-(self.Gap[0]*1), self.Gap[1])

    def Handle_Coin_Numbers(self):
        self.Player_Coin_Number_String = str(self.player.Coins)
        Number_Frame_x = self.Coin_Icon_Position[0]+self.Player_Coins_UI_Icon_size[0]+(self.Font_Image_Size[0]/4)
        for idx, Number in enumerate(self.Player_Coin_Number_String):
            self.Window.blit(
                self.Font_Images[Number], 
                (Number_Frame_x+((self.Font_Image_Size[0]+(self.Font_Image_Size[0]/5))*idx), self.Coin_Icon_Position[1])
            )
    
    def Handle_Boss_Approval_Numbers(self):
        self.Player_Boss_Approvals_Number_String = str(self.player.Boss_Approvals)
        Number_Frame_x = self.Boss_Approval_Icon_Position[0]+self.Player_Coins_UI_Icon_size[0]+(self.Font_Image_Size[0]/4)
        for idx, Number in enumerate(self.Player_Boss_Approvals_Number_String):
            self.Window.blit(
                self.Font_Images[Number], 
                (Number_Frame_x+((self.Font_Image_Size[0]+(self.Font_Image_Size[0]/5))*idx), self.Boss_Approval_Icon_Position[1])
            )

    def Rescale_Font_Images(self):
        Font_Image_Original_Size = Font_Images.n_1.get_size()
        Rescale_Rate = self.Player_Coins_UI_Icon_size[1]/Font_Image_Original_Size[1]
        self.Font_Image_Size = (int(Font_Image_Original_Size[0]*Rescale_Rate), int(Font_Image_Original_Size[1]*Rescale_Rate))

        self.Font_Images = {}
        for Str, Img in Font_Images.Number_Dict.items():
            self.Font_Images[Str] = pygame.transform.scale(Img, self.Font_Image_Size)

    def Update(self):
        self.Window.blit(self.Boss_Approval_Icon, self.Boss_Approval_Icon_Position)
        self.Window.blit(self.Coin_Icon, self.Coin_Icon_Position)
        self.Handle_Boss_Approval_Numbers()
        self.Handle_Coin_Numbers()




#-----------------------------------------------------------------------------------------------------------------------------------------------------
""" Player & Charactor Stuffs """
#Player Default Values
class Player_Defaults():
    pygame.mixer.init()
    Jump_sound = pygame.mixer.Sound(os.path.join("assets", "Music", "Jump.wav"))
    Dash_sound = pygame.mixer.Sound(os.path.join("assets", "Music", "Dash.wav"))
    def __init__(self, Game, Charactor, Charactor_Width, Charactor_Height):
        self.Game = Game

        self.Charactor_Width, self.Charactor_Height = Charactor_Width, Charactor_Height

        self.Charactors = {
            "Yellow_Triangle":pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "Charactor", "Yellow_Triangle.png")), (self.Charactor_Width, self.Charactor_Height)
            ),
            "Knight":pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "Charactor", "Knight.png")), (self.Charactor_Width, self.Charactor_Height)
            ),
            "Ninja":pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "Charactor", "Ninja.png")), (self.Charactor_Width, self.Charactor_Height)
            ),
            "Baize":pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "Charactor", "Baize.png")), (self.Charactor_Width, self.Charactor_Height)
            ),
            "Panda":pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "Charactor", "Panda.png")), (self.Charactor_Width, self.Charactor_Height)
            ),
            "Green_Elf":pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "Charactor", "Green_Elf.png")), (self.Charactor_Width, self.Charactor_Height)
            ),
            "Rice_Ball":pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "Charactor", "Rice_Ball.png")), (self.Charactor_Width, self.Charactor_Height)
            ),
            "Bloodly_Poop":pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "Charactor", "Bloodly_Poop.png")), (self.Charactor_Width, self.Charactor_Height)
            ),
            "Poop":pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "Charactor", "Poop.png")), (self.Charactor_Width, self.Charactor_Height)
            ),
            "Finn":pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "Charactor", "Finn.png")), (self.Charactor_Width, self.Charactor_Height)
            ),
            "Dino":pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "Charactor", "Dino.png")), (self.Charactor_Width, self.Charactor_Height)
            ),
            "Puppy":pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "Charactor", "Puppy.png")), (self.Charactor_Width, self.Charactor_Height)
            ),
            "Ghosty":pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "Charactor", "Ghosty.png")), (self.Charactor_Width, self.Charactor_Height)
            ),
            "Sus":pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "Charactor", "Sus.png")), (self.Charactor_Width, self.Charactor_Height)
            ),
            "Orby":pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "Charactor", "Orby.png")), (self.Charactor_Width, self.Charactor_Height)
            ),
            "Skull":pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "Charactor", "Skull.png")), (self.Charactor_Width, self.Charactor_Height)
            ),
            "AAACube":pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "Charactor", "AAACube.png")), (self.Charactor_Width, self.Charactor_Height)
            ),
        }

        
        self.Interact_Frame = pygame.transform.scale(
            pygame.image.load(
                os.path.join("assets", "Textures", "Interactive", "Interact_Frame.png")
            ), (self.Charactor_Width*2, self.Charactor_Height*2)
        )
        self.Interact_Stage_Imgs = [
            pygame.transform.scale(
                pygame.image.load(
                    os.path.join("assets", "Textures", "Interactive", f"Interact_Button_Stage_{stage}.png")
                ), (self.Charactor_Width, self.Charactor_Height)
            ) for stage in range(0, 9)
        ]
        self.Key_Icons = Key_Icons(Charactor_Width=self.Charactor_Width, Charactor_Height=self.Charactor_Height).Keys


        self.state = {
            "Looking_Left":False,
            "Jumping":False,

            "Double_Jump_Unlocked":True,
            "Double_Jumping":False,
            "Can_Double_Jump":False,
            
            "Dash_Unlocked":True,
            "Dashing":False,
        }

        self.Img = self.Charactors[Charactor]

        self.Charactor_Name = Charactor

        self.Coins = 0
        self.Boss_Approvals = 0

    def Set_Defaults(self):
        #Interacting properties
        self.Interact_Counter = 0

        #Player attack properties
        self.Shooting = False

        #Player properties
        self.Health = 100
        self.is_dead = False

        self.state["Looking_Left"] = self.state["Jumping"] = self.state["Double_Jumping"] = self.state["Can_Double_Jump"] = self.state["Dashing"] = False

        self.Respawn_Time_Counter = 0

        self.Charactor_vel = (self.Charactor_Width+self.Charactor_Height)/16

        self.Falling_Gravity = 0
        self.Gravity = self.Jumping_Gravity = 14*self.Game.Win_Scale
        self.Jumping_Falling_vel = self.Charactor_vel//3 * ((self.Game.Win_Scale%1)+1)

        self.Dash_Counts = self._Dash_Counts = 8
        self.Dashing_Cooldown = 0
        self._Dashing_Cooldown = 60
        self.Dashing_vel = (self.Charactor_Width+self.Charactor_Height)/2

#Player movement and animation
class Player(Player_Defaults):
    def __init__(self, Game, Player_Width, Player_Height):
        super().__init__(Game=Game, Charactor="AAACube", Charactor_Width=Player_Width, Charactor_Height=Player_Height)
        self.Reset_Default = super().Set_Defaults
        self.Reset_Default()

        self.x, self.y =  (30, 500)
        self.Window = self.Game.Window

        self.GamePlay_UI = Player_Gameplay_UI(player=self)

        self.Respawn_Point = {} #Respawn_Scene , Respawn_Scene_Map_x , Respawn_Scene_Map_y , Respawn_x , Respawn_y

        self.Win_Width, self.Win_Height = self.Game.Width, self.Game.Height

        self.Center = (self.x+(self.Charactor_Width/2), self.y+(self.Charactor_Height/2))

        self.clone = self.Window.blit(self.Img, (self.x, self.y))

        self.Weapon = None



    """
    Player Death Control
    """
    #Player Dead
    def Dead(self):
        self.is_dead = True
        self.Game.Particle_System.Add_Particle(self.Game.Particle_System.Player_Dead)
        self.Respawn_Time_Counter = 90

    #Respawn
    def Respawn(self):
        self.Respawn_Time_Counter -= 1
        if self.Respawn_Time_Counter <= 0 and self.is_dead:
            self.Game.Clear_All_Entity()
            self.Reset_Default()
            self.Environment.Set_Scene(Scene=self.Respawn_Point["Scene"][0], Map_x=self.Respawn_Point["Scene"][1], Map_y=self.Respawn_Point["Scene"][2])
            self.x, self.y = self.Respawn_Point["Position"]

    #Set Player's Respawn position
    def Set_Respawn(self, Scene, Map_x, Map_y, x, y):
        self.Respawn_Point["Scene"] = (Scene, Map_x, Map_y)
        self.Respawn_Point["Position"] = (x, y)
        self.Game.Save_Game()



    """
    Scene/Environment Functions
    """
    #Bind Environment System
    def Bind_Env(self, Env):
        self.Environment = Env

    #Detect if the player Landed on the platform or fell in to the void
    def Check_Landed(self, next_move_val):
        Top_Border, Bottom_Border, Left_Border, Right_Border, Center_x, Center_y = self.Get_Position() #Get Player Position info

        for Block in sorted(self.Environment.Blocks, key=lambda Block:Block.y):
            if Block.x < Right_Border and Left_Border < Block.x+Block.Block_Width: #Check if the player's x position is in between the Land border
                if Bottom_Border <= Block.y and (Bottom_Border - next_move_val) >= Block.y: #Check if the player will fall onto/into the Land after next fall
                    self.y = Block.y-self.Charactor_Height #if so, keep the player on top of the Land
                    return True
        
        Available_Next_Scene_Directions = self.Environment.Get_Available_Directions()
        if  Available_Next_Scene_Directions[1]:
            if (self.y - next_move_val) >= self.Win_Height: #Check if player is at the bottom of the whole scene
                self.y = self.Win_Height #if so, keep the player there to stop player from falling out of the scene
                return False
        elif(self.y - next_move_val) >= self.Win_Height-self.Charactor_Height: #Check if player fall out of the scene
            self.Dead() #if so, player is dead, respawn the Charactor
            return False
        return False

    #Detect if the player's head hit the Environment
    def Check_Hit_Roof(self, next_move_val):
        Top_Border, Bottom_Border, Left_Border, Right_Border, Center_x, Center_y = self.Get_Position() #Get Player Position info

        for Block in sorted(self.Environment.Blocks, key=lambda Block:Block.y):
            if Block.x < Right_Border and Left_Border < Block.x+Block.Block_Width: #Check if the player's x position is in between the Land border
                if Top_Border+next_move_val <= Block.y+Block.Block_Height and Bottom_Border > Block.y:  #Check if the player will Jump into the Land after next move
                    self.y = Block.y+Block.Block_Height #if so, set the player right above the Land
                    return True
        return False

    #Detect if the player's Left / Right is blocked
    def Check_Left_Right_Collided(self, next_move_val):
        Top_Border, Bottom_Border, Left_Border, Right_Border, Center_x, Center_y = self.Get_Position() #Get Player Position info

        Available_Next_Scene_Directions = self.Environment.Get_Available_Directions()

        for Block in sorted(self.Environment.Blocks, key=lambda Block:Block.y):
            if Block.y < Bottom_Border and self.y < (Block.y+Block.Block_Height): #Check if the player's y position is in between the Land's MAX and MIN y
                if next_move_val > 0: #if move_val is positive, player is moving RIGHT, means we check if player's Right Border hits the Land's Left Border
                    if Block.x < (Right_Border+next_move_val) < (Block.x+Block.Block_Width): # Check if the player will move into the Land after next move
                        self.x = Block.x - self.Charactor_Width #if so, set the player at the Left Border of the Land
                        return True
                elif next_move_val < 0: #if move_val is negative, player is moving LEFT, means we check if player's Left Border hits the Land's Right Border
                    if Block.x < (Left_Border+next_move_val) < (Block.x+Block.Block_Width): # Check if the player will move into the Land after next move
                        self.x = Block.x+Block.Block_Width #if so, set the player at the Right Border of the Land
                        return True

        if next_move_val > 0: #if move_val is positive, player is moving RIGHT, means we check if player's Right Border hits the Land's Left Border
            if (self.x+next_move_val <= self.Win_Width-self.Charactor_Width):
                return False
            elif Available_Next_Scene_Directions[3] and (self.x+next_move_val <= self.Win_Width):
                return False
            elif Available_Next_Scene_Directions[3]:
                self.x = self.Win_Width
                return True
            else:
                self.x = self.Win_Width-self.Charactor_Width
                return True
        elif next_move_val < 0: #if move_val is negative, player is moving LEFT, means we check if player's Left Border hits the Land's Right Border
            if (self.x+next_move_val >= 0):
                return False
            elif Available_Next_Scene_Directions[2] and (self.x+next_move_val >= -self.Charactor_Width):
                return False
            elif Available_Next_Scene_Directions[2]:
                self.x = -self.Charactor_Width
                return True
            else:
                self.x = 0
                return True

        return False



    """
    Movement Controls
    """
    #Weapon / Shooting / Drawing
    def Control_Shoot(self, pressed_keys):
        if self.Weapon:
            if pressed_keys[self.Game.Key_Handler[self.Game.Controls["shoot"]]]:
                if self.Weapon._Shoot_Cooldown <= 0 and not self.Weapon.Shooting:
                    self.Weapon.Shooting = True
            else:
                self.Weapon.Shooting = False
            self.Weapon.Shoot()
            self.Weapon.Update()

    #Jumping / Falling / Double_Jump
    def Control_Jump_Fall(self, pressed_keys):
        if pressed_keys[self.Game.Key_Handler[self.Game.Controls["jump"]]] and not self.state["Jumping"]:
            self.state["Jumping"] = True
            self.Jump_sound.play()

        if self.state["Jumping"]:
            if self.state["Double_Jump_Unlocked"]:
                if not self.state["Double_Jumping"]:
                    if not pressed_keys[self.Game.Key_Handler[self.Game.Controls["jump"]]]:
                        self.state["Can_Double_Jump"] = True
                    elif self.state["Can_Double_Jump"] and pressed_keys[self.Game.Key_Handler[self.Game.Controls["jump"]]]:
                        self.state["Double_Jumping"] = True
                        self.Jump_sound.play()
                        self.Jumping_Gravity = self.Gravity
                        self.Game.Particle_System.Add_Particle(self.Game.Particle_System.Player_Double_Jump)
            if not self.Check_Hit_Roof(next_move_val=-self.Jumping_Gravity):
                if not self.state["Dashing"]:
                    self.y -= self.Jumping_Gravity
            else:
                self.Jumping_Gravity = 0
            if not self.state["Dashing"]:
                if self.Jumping_Gravity > -self.Gravity:
                    if self.Jumping_Gravity > 0 and self.Jumping_Gravity-self.Jumping_Falling_vel <0:
                        self.Jumping_Gravity = 0
                    else:
                        self.Jumping_Gravity -= self.Jumping_Falling_vel
                else:
                    self.Jumping_Gravity = -self.Gravity
            if self.Check_Landed(next_move_val=self.Jumping_Gravity):
                if self.Jumping_Gravity <= -self.Gravity:
                    self.Game.Particle_System.Add_Particle(self.Game.Particle_System.Player_Land)
                self.Falling_Gravity = 0
                self.Jumping_Gravity = self.Gravity
                self.state["Jumping"] = self.state["Double_Jumping"] = self.state["Can_Double_Jump"] = False

        elif not self.Check_Landed(next_move_val=0):
            if not self.state["Dashing"]:
                self.y -= self.Falling_Gravity
                if self.Falling_Gravity > -self.Gravity:
                    self.Falling_Gravity -= self.Jumping_Falling_vel
                else:
                    self.Falling_Gravity = -self.Gravity
            else:
                self.Falling_Gravity = 0
            if self.Check_Landed(next_move_val=self.Falling_Gravity):
                if self.Falling_Gravity <= -self.Gravity:
                    self.Game.Particle_System.Add_Particle(self.Game.Particle_System.Player_Land)
                self.Falling_Gravity = 0
                self.Jumping_Gravity = self.Gravity
                self.state["Jumping"] = self.state["Double_Jumping"] = self.state["Can_Double_Jump"] = False

    #Moving / Dashing
    def Control_Move(self, pressed_keys): 
        Next_Move_Value = ((self.Charactor_vel/self.Game.Win_Scale)*( 2**(1/2) ))*self.Game.Win_Scale

        if not self.state["Dashing"]:
            if pressed_keys[self.Game.Key_Handler[self.Game.Controls["left"]]]:
                self.state["Looking_Left"] = True # if pressed Left, then set Looking_Left to True
                if not self.Check_Left_Right_Collided(next_move_val=-Next_Move_Value):
                    self.x -= Next_Move_Value

            if pressed_keys[self.Game.Key_Handler[self.Game.Controls["right"]]]:
                self.state["Looking_Left"] = False # if pressed Right, then set Looking_Left to False
                if not self.Check_Left_Right_Collided(next_move_val=Next_Move_Value):
                    self.x += Next_Move_Value

            if self.state["Dash_Unlocked"] and pressed_keys[self.Game.Key_Handler[self.Game.Controls["dash"]]] and self.Dashing_Cooldown <= 0:
                self.state["Dashing"] = True
                self.Dash_sound.play()
                self.Game.Particle_System.Add_Particle(self.Game.Particle_System.Player_Dash)
        
        else:
            if self.state["Looking_Left"]:
                for multiplier in range(1, int(self.Dashing_vel/Next_Move_Value)+1):
                    if self.Check_Left_Right_Collided(next_move_val=-(Next_Move_Value*multiplier)):
                        self.Dash_Counts = 0
                        self.state["Dashing"] = False
                        self.Dash_Counts = self._Dash_Counts
                        self.Dashing_Cooldown = self._Dashing_Cooldown
                        return
                self.x -= self.Dashing_vel
                self.Dash_Counts -= 1

            else:
                for multiplier in range(1, int(self.Dashing_vel/Next_Move_Value)+1):
                    if self.Check_Left_Right_Collided(next_move_val=(Next_Move_Value*multiplier)):
                        self.Dash_Counts = 0
                        self.state["Dashing"] = False
                        self.Dash_Counts = self._Dash_Counts
                        self.Dashing_Cooldown = self._Dashing_Cooldown
                        return
                self.x += self.Dashing_vel
                self.Dash_Counts -= 1

            if self.Dash_Counts <= 0:
                self.state["Dashing"] = False
                self.Dash_Counts = self._Dash_Counts
                self.Dashing_Cooldown = self._Dashing_Cooldown
        
        if self.Dashing_Cooldown > 0:
            self.Dashing_Cooldown -= 1

        self.Center = (self.x+(self.Charactor_Width/2), self.y+(self.Charactor_Height/2))

    #Get Player Position
    def Get_Position(self): #return (Top_Border, Bottom_Border, Left_Border, Right_Border, Center_x, Center_y)
        info = ((self.y), (self.y+self.Charactor_Height), (self.x), (self.x+self.Charactor_Width))+self.Center
        return info



    """
    Update
    """
    #Update Position / Take input / Environment interaction / Respawn
    def Update(self): #Return whether the Charactor is out of the current Scene
        if not self.is_dead:
            pressed_keys = pygame.key.get_pressed()
            if -self.Charactor_Width < self.x < self.Win_Width and -self.Charactor_Height < self.y < self.Win_Height: #Execute Control functions only if the Charactor is still in the Scene
                self.Control_Jump_Fall(pressed_keys=pressed_keys)
                self.Control_Shoot(pressed_keys=pressed_keys)
                self.Control_Move(pressed_keys=pressed_keys)
            if self.Health <= 0:
                self.Dead()
        else:
            self.Respawn()
        return (
            self.y+self.Charactor_Height <= 0, # Leave the Scene from Top
            self.y >= self.Win_Height, # Leave the Scene from Bottom
            self.x+self.Charactor_Width <= 0, # Leave the Scene from Left
            self.x >= self.Win_Width# Leave the Scene from Right
        )

    #Draw Charactor / Weapon / UI
    def Draw(self):
        self.clone = self.Window.blit(
            pygame.transform.flip(
                self.Img, self.state["Looking_Left"], False
            ), (self.x, self.y)
        )
        if self.Weapon:
            self.Weapon.Draw_Holding()
        self.GamePlay_UI.Update()



    """
    Other
    """
    #Set Player's Charactor Skin
    def Set_Charactor(self, Charactor_Name):
        self.Img = self.Charactors[Charactor_Name]

    #Interact with Scene / Environment Object
    def Interact(self, Object):
        Interact_Key = self.Game.Controls["use"]

        Interact_Frame = self.Window.blit(
            self.Interact_Frame, (self.x-(self.Charactor_Width/2), self.y-(self.Charactor_Height*2))
        )
        Interact_Button = self.Window.blit(
            self.Interact_Stage_Imgs[self.Interact_Counter//7], (
                (self.x),
                (self.y-(self.Charactor_Height*2)-(self.Charactor_Height/2))
            )
        )
        Interact_Key_Icon = self.Window.blit(
            self.Key_Icons[f"K_{Interact_Key}"], (
                (self.x-(self.Charactor_Width/4)+(self.Charactor_Width/2)),
                (self.y-(self.Charactor_Height*2)-(self.Charactor_Height/4))
            )
        )
        Icon = self.Window.blit(
            Object.Img, (
                (self.x-(self.Charactor_Width/2)+(Object.Img_Width/2)), 
                (self.y-(self.Charactor_Height*2)+(Object.Img_Height/2))
            )
        )
        if pygame.key.get_pressed()[self.Game.Key_Handler[Interact_Key]]:
            self.Interact_Counter += 1
            if self.Interact_Counter > 60:
                self.Interact_Counter = 0
                return True
        else:
            self.Interact_Counter = 0
        return False

    #Equip Weapon and Drop Original Weapon if the Player Originally has one
    def Equip_Weapon(self, Weapon):
        if self.Weapon:
            self.Game.Loot_System.Make_Loot(
                Loot_Item=self.Weapon.__class__, 
                Spawn_Center=(self.x+(self.Charactor_Width/2), self.y+(self.Charactor_Height/2))
            )
        self.Weapon = Weapon(Game=self.Game)

    #Load Game Progess Save
    def Load_Saving(self, Player_data):
        self.state["Double_Jump_Unlocked"] = Player_data["state"]["Double_Jump_Unlocked"]
        self.state["Dash_Unlocked"] = Player_data["state"]["Dash_Unlocked"]

        Respawn_Point = [int(Player_data["RespawnPoint"][i:i+2]) for i in range(0, len(Player_data["RespawnPoint"]), 2)]
        self.Set_Respawn(
            Scene=self.Environment.Map[Respawn_Point[1]][Respawn_Point[0]], Map_x=Respawn_Point[0], Map_y=Respawn_Point[1], 
            x=Respawn_Point[2]*self.Charactor_Width, y=Respawn_Point[3]*self.Charactor_Height,
        )

        Player_Position = [int(Player_data["Position"][i:i+2]) for i in range(0, len(Player_data["Position"]), 2)]
        self.Environment.Set_Scene(
            Scene=self.Environment.Map[Player_Position[1]][Player_Position[0]], Map_x=Player_Position[0], Map_y=Player_Position[1]
        )
        self.x, self.y = Player_Position[2]*self.Charactor_Width, Player_Position[3]*self.Charactor_Height

        self.Coins = Player_data["Coin"]
        self.Boss_Approvals = Player_data["Boss_Approval"]

        self.Weapon = self.Game.Weapons.Weapon_Dict[Player_data["Weapon"]](Game=self.Game)

    def Get_Saving_Data(self):
        Player_data = {
            "state":{
                "Double_Jump_Unlocked":self.state["Double_Jump_Unlocked"],
                "Dash_Unlocked":self.state["Dash_Unlocked"]
            },
            "RespawnPoint":"{:0>2}{:0>2}{:0>2}{:0>2}".format(
                self.Respawn_Point["Scene"][1], self.Respawn_Point["Scene"][2], 
                int(self.Respawn_Point["Position"][0]/self.Charactor_Width), int(self.Respawn_Point["Position"][1]/self.Charactor_Height)
            ),
            "Position":"{:0>2}{:0>2}{:0>2}{:0>2}".format(
                self.Environment.Current_Scene.Map_x, self.Environment.Current_Scene.Map_y, 
                int(self.x/self.Charactor_Width), int(self.y/self.Charactor_Height)
            ),
            "Weapon":self.Weapon.ID,
            "Coin":self.Coins,
            "Boss_Approval":self.Boss_Approvals
        }
        return Player_data