from math import fabs
from Generate_Save_File import Generate_SaveFile
from Particle_System import *
from UI_System import *
from Weapon import *
from Scenes import *
from Player import *
from Enemy import *
from Loot import *

from Tools import *

import pygame
import json


pygame.init()



#-----------------------------------------------------------------------------------------------------------------------------------------------------
#App: window, mainloop, fps_control... etc
class Application():
    #Default Width=960, Height=720
    def __init__(self, Win_Scale=1, fps=60):
        #Game
        self.Default_Width = 960
        self.Default_Height = 720
        self.Default_block_w_h = 24

        self.Generate_SaveFile = Generate_SaveFile
        self.Playing_Save_File = None

        #Tools
        self.Loop_Function_History_Stack = History_Stack()
        self.Event_Timer = Event_System()

        #Application
        self.Played = False
        self.Running = True
        self.Can_Esc = True

        #FPS related
        self.FPS = fps
        self.FPS_wait = pygame.time.Clock().tick
        
        #Init Game
        self.Init_Game(Win_Scale=Win_Scale)

        #UI
        self.Controls = None
        self.Key_Handler = Handle_Keys.Key_IDs
        self.UI_System = UI_System(Game=self)

    def Init_Game(self, Win_Scale):
        #Window init
        self.Win_Scale = Win_Scale
        self.Width, self.Height = int(self.Default_Width*self.Win_Scale), int(self.Default_Height*self.Win_Scale)
        self.Window = pygame.display.set_mode(((self.Width), self.Height))
        pygame.display.set_caption("PixKour")

        pygame.draw.rect(self.Window, (0, 0, 0), pygame.Rect(0, 0, self.Width, self.Height))

        #Weapons
        self.Weapons = Weapons

        #Player
        self.Player_Width, self.Player_Height = int(self.Default_block_w_h*self.Win_Scale), int(self.Default_block_w_h*self.Win_Scale)
        self.player = Player(Game=self, Player_Width=self.Player_Width, Player_Height=self.Player_Height)
        self.player.Equip_Weapon(Weapon=Weapons.Crescendum)

        #Enemy
        self.Enemy = Enemy(Game=self)

        #Loot
        self.Loot_System = Loot_System(Game=self)

        #Environment
        self.Block_Width, self.Block_Height = int(self.Default_block_w_h*self.Win_Scale), int(self.Default_block_w_h*self.Win_Scale)
        self.Environment = Environment(Game=self, Block_Width=self.Block_Width, Block_Height=self.Block_Height)

        #Particle
        self.Particle_System = Particles(Game=self)



    #Tool Functions
    def Check_Collided(self, A, B):
        A_x, A_y, A_w, A_h = (A.x, A.y)+A.size
        B_x, B_y, B_w, B_h = (B.x, B.y)+B.size
        Judgement = (
            (A_x <= B_x <= A_x+A_w or A_x <= B_x+B_w <= A_x+A_w) or (B_x <= A_x <= B_x+B_w or B_x <= A_x+A_w <= B_x+B_w)
            ) and (
            (A_y <= B_y <= A_y+A_h or A_y <= B_y+B_h <= A_y+A_h) or (B_y <= A_y <= B_y+B_h or B_y <= A_y+A_h <= B_y+B_h)
        )
        if Judgement:
            return True
        return False

    def Get_Slope(self, A, B):
        return ((B[1]-A[1]) / (B[0]-A[0]))

    def Clear_All_Entity(self):
        self.Enemy.Clear_All_Enemy()
        self.Loot_System.Clear_All_Loot()
        self.player.Weapon.Bullet_Container = []



    #Main Run Function
    def run(self):
        self.Home_Page_Function()
        self.z = False
        self.k = 1
        self.player.state["Double_Jump_Unlocked"] = True
        self.player.state["Dash_Unlocked"] = True
        while(not any(evt.type == pygame.QUIT for evt in pygame.event.get()) and self.Running):
            self.FPS_wait(self.FPS)

            self.Looping_Function()

            pygame.display.update()

        if self.Played:
            self.Save_Game()

        pygame.quit()



    #Saving and Loading
    def Load_Saving(self, file_name):
        self.Playing_Save_File = file_name
        with open(os.path.join("Saves", f"{self.Playing_Save_File}.json"), "r") as save_file:
            self.Playing_SaveData = json.load(save_file)
            self.Environment.Load_Saving(Environment_data=self.Playing_SaveData["Map"])
            self.player.Load_Saving(Player_data=self.Playing_SaveData["Player"])
        with open(os.path.join("Config", "KeyBinding.json"), "r") as Key_file:
            self.Controls = json.load(Key_file)

    def Save_Game(self):
        Current_time = time.strftime("%B")+" "+time.strftime("%d")+", "+time.strftime("%Y")+" "+time.strftime("%I")+":"+time.strftime("%M")+" "+time.strftime("%p")
        Game_data = {
            "Create_Time":self.Playing_SaveData["Create_Time"],
            "Last_Save":Current_time,
            "Player":self.player.Get_Saving_Data(),
            "Map":self.Environment.Get_Saving_Data()
        }
        with open(os.path.join("Saves", f"{self.Playing_Save_File}.json"), "w") as save_file:
            json.dump(Game_data, save_file, sort_keys=True)
        self.Played = False



    #~*~< | Loop Functions | >~*~
    #Home Page Functions
    def Home_Page_Function(self):
        self.UI_System.Home_Page()
        self.Looping_Function = self.Home_Page_Looping_Function
        self.Loop_Function_History_Stack.Push(arguments=(self.UI_System.Home_Page.__name__, self.UI_System.Home_Page, self.Home_Page_Looping_Function))
        self.Looping_Function()
    def Home_Page_Looping_Function(self):
        Result = self.UI_System.Update()
        if Result == "Play":
            self.Choose_Save_Function()

        elif Result == "Setting":
            self.Setting_Menu_Function()

        elif Result == "Help":
            self.Help_Menu_Function()

        elif Result == "Achievement":
            self.Achievement_Menu_Function()

        elif Result == "Choose_Charactor":
            self.Choose_Charactor_Menu_Function()

        elif Result == "Exit":
            self.Exit_Function()


    #Pausing related Functions
    def Pause_Menu_Function(self):
        self.UI_System.Pause_Page()
        self.Looping_Function = self.Pause_Menu_Looping_Function
        self.Loop_Function_History_Stack.Push(arguments=(self.UI_System.Pause_Page.__name__, self.UI_System.Pause_Page, self.Pause_Menu_Looping_Function))
        self.Looping_Function()
    def Pause_Menu_Looping_Function(self):
        self.Environment.Draw_Environment()
        self.player.Draw()
        Result = self.UI_System.Update()
        if not pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.Can_Esc = True

        if Result == "Setting":
            self.Setting_Menu_Function()

        elif Result == "Help":
            self.Help_Menu_Function()

        elif Result == "Achievement":
            self.Achievement_Menu_Function()

        elif Result == "Return" or (pygame.key.get_pressed()[pygame.K_ESCAPE] and self.Can_Esc):
            self.Can_Esc = False
            self.Return_Last_Page_Function()
            
        elif Result == "Respawn":
            self.Respawn_Function()
            self.Game_Function()

        elif Result == "Home":
            self.Home_Page_Function()
            if self.Played:
                self.Save_Game()


    #Choose Save related Functions
    def Choose_Save_Function(self):
        self.UI_System.Choose_Save_Page()
        self.Looping_Function = self.Choose_Save_Looping_Function
        self.Loop_Function_History_Stack.Push(arguments=(self.UI_System.Choose_Save_Page.__name__, self.UI_System.Choose_Save_Page, self.Choose_Save_Looping_Function))
        self.Looping_Function()
    def Choose_Save_Looping_Function(self):
        Result = self.UI_System.Update()
        if not pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.Can_Esc = True

        if Result == "Return" or (pygame.key.get_pressed()[pygame.K_ESCAPE] and self.Can_Esc):
            self.Can_Esc = False
            self.Return_Last_Page_Function()
        elif Result:
            if Result == "Add_Save":
                self.Generate_SaveFile()
            else:
                self.Load_Saving(file_name=Result)
                self.Game_Function()


    #Main Game related Functions
    def Game_Function(self):
        self.UI_System.Current = self.Game_Function
        self.Looping_Function = self.Game_Looping_Function
        self.Loop_Function_History_Stack.Push(arguments=(self.Game_Looping_Function.__name__, self.Game_Looping_Function, self.Game_Looping_Function))
        self.Event_Timer.Reset()
        self.Looping_Function()
        self.Played = True
    def Game_Looping_Function(self):
        if not pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.Can_Esc = True

        self.Environment.Draw_Environment()

        state = self.player.Update()

        self.Environment.Update(state=state)

        self.player.Draw()

        self.Particle_System.Update()

        self.Event_Timer.Update()

        if (pygame.key.get_pressed()[pygame.K_ESCAPE] and self.Can_Esc):
            self.Can_Esc = False
            self.Pause_Menu_Function()


    #Choose_Charactor related Functions
    def Choose_Charactor_Menu_Function(self):
        self.UI_System.Choose_Charactor_Page()
        self.Looping_Function = self.Choose_Charactor_Menu_Looping_Function
        self.Loop_Function_History_Stack.Push(arguments=(self.UI_System.Choose_Charactor_Page.__name__, self.UI_System.Choose_Charactor_Page, self.Choose_Charactor_Menu_Looping_Function))
        self.Looping_Function()
    def Choose_Charactor_Menu_Looping_Function(self):
        if not pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.Can_Esc = True
        Result = self.UI_System.Update()
        if Result:
            if Result != "Return":
                self.player.Set_Charactor(Charactor_Name=Result)
            else:
                self.Return_Last_Page_Function()
        if (pygame.key.get_pressed()[pygame.K_ESCAPE] and self.Can_Esc):
            self.Can_Esc = False
            self.Return_Last_Page_Function()


    #Help related Functions
    def Help_Menu_Function(self):
        self.UI_System.Help_Page()
        self.Looping_Function = self.Help_Menu_Looping_Function
        self.Loop_Function_History_Stack.Push(arguments=(self.UI_System.Help_Page.__name__, self.UI_System.Help_Page, self.Help_Menu_Looping_Function))
        self.Looping_Function()
    def Help_Menu_Looping_Function(self):
        self.Return_Last_Page_Function()
        return
        if not pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.Can_Esc = True
        Result = self.UI_System.Update()


    #Achievement related Functions
    def Achievement_Menu_Function(self):
        self.UI_System.Achievement_Page()
        self.Looping_Function = self.Achievement_Menu_Looping_Function
        self.Loop_Function_History_Stack.Push(arguments=(self.UI_System.Achievement_Page.__name__, self.UI_System.Achievement_Page, self.Achievement_Menu_Looping_Function))
        self.Looping_Function()
    def Achievement_Menu_Looping_Function(self):
        self.Return_Last_Page_Function()
        return
        if not pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.Can_Esc = True
        Result = self.UI_System.Update()


    #Setting related Functions
    def Setting_Menu_Function(self):
        self.UI_System.Setting_Page()
        self.Looping_Function = self.Setting_Menu_Looping_Function
        self.Loop_Function_History_Stack.Push(arguments=(self.UI_System.Setting_Page.__name__, self.UI_System.Setting_Page, self.Setting_Menu_Looping_Function))
        self.Looping_Function()
    def Setting_Menu_Looping_Function(self):
        if not pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.Can_Esc = True
        Result = self.UI_System.Update()
        if Result:
            if Result == "Return":
                self.Return_Last_Page_Function()
            elif Result == "Game":
                self.Game_Setting_Menu_Function()
            elif Result == "Audio":
                self.Audio_Setting_Menu_Function()
            elif Result == "Video":
                self.Video_Setting_Menu_Function()
            elif Result == "Keyboard":
                self.Keyboard_Setting_Menu_Function()
        if (pygame.key.get_pressed()[pygame.K_ESCAPE] and self.Can_Esc):
            self.Can_Esc = False
            self.Return_Last_Page_Function()

    def Game_Setting_Menu_Function(self):
        self.UI_System.Setting_Page()
        self.Looping_Function = self.Setting_Menu_Looping_Function
        self.Loop_Function_History_Stack.Push(arguments=(self.UI_System.Setting_Page.__name__, self.UI_System.Setting_Page, self.Setting_Menu_Looping_Function))
        self.Looping_Function()
    def Game_Setting_Menu_Looping_Function(self):
        self.Return_Last_Page_Function()
        return
        if not pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.Can_Esc = True
        Result = self.UI_System.Update()
        if (pygame.key.get_pressed()[pygame.K_ESCAPE] and self.Can_Esc):
            self.Can_Esc = False
            self.Return_Last_Page_Function()

    def Audio_Setting_Menu_Function(self):
        self.UI_System.Setting_Page()
        self.Looping_Function = self.Setting_Menu_Looping_Function
        self.Loop_Function_History_Stack.Push(arguments=(self.UI_System.Setting_Page.__name__, self.UI_System.Setting_Page, self.Setting_Menu_Looping_Function))
        self.Looping_Function()
    def Audio_Setting_Menu_Looping_Function(self):
        self.Return_Last_Page_Function()
        return
        if not pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.Can_Esc = True
        Result = self.UI_System.Update()
        if (pygame.key.get_pressed()[pygame.K_ESCAPE] and self.Can_Esc):
            self.Can_Esc = False
            self.Return_Last_Page_Function()

    def Video_Setting_Menu_Function(self):
        self.UI_System.Setting_Page()
        self.Looping_Function = self.Setting_Menu_Looping_Function
        self.Loop_Function_History_Stack.Push(arguments=(self.UI_System.Setting_Page.__name__, self.UI_System.Setting_Page, self.Setting_Menu_Looping_Function))
        self.Looping_Function()
    def Video_Setting_Menu_Looping_Function(self):
        self.Return_Last_Page_Function()
        return
        if not pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.Can_Esc = True
        Result = self.UI_System.Update()
        if (pygame.key.get_pressed()[pygame.K_ESCAPE] and self.Can_Esc):
            self.Can_Esc = False
            self.Return_Last_Page_Function()

    def Keyboard_Setting_Menu_Function(self):
        self.UI_System.Setting_Page()
        self.Looping_Function = self.Setting_Menu_Looping_Function
        self.Loop_Function_History_Stack.Push(arguments=(self.UI_System.Setting_Page.__name__, self.UI_System.Setting_Page, self.Setting_Menu_Looping_Function))
        self.Looping_Function()
    def Keyboard_Setting_Menu_Looping_Function(self):
        if not pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.Can_Esc = True
        Result = self.UI_System.Update()
        if (pygame.key.get_pressed()[pygame.K_ESCAPE] and self.Can_Esc):
            self.Can_Esc = False
            self.Return_Last_Page_Function()




    #Others
    def Return_Last_Page_Function(self):
        Last_Page_Initialize_Function_Name, Last_Page_Initialize_Function, Last_Page_Looping_Function = self.Loop_Function_History_Stack.Pop()
        Result_Function = self.UI_System.UIs.get(Last_Page_Initialize_Function_Name, False)
        if Result_Function:
            Result_Function()
        else:
            Last_Page_Initialize_Function()
        self.Looping_Function = Last_Page_Looping_Function
        self.Looping_Function()


    def Exit_Function(self):
        self.Running = False


    def Respawn_Function(self):
        self.player.is_dead = True
        self.player.Respawn()


    def Looping_Function(self):
        pass




App = Application()
App.run()