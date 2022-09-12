import pygame
import json
import os

pygame.init()





#Special Surfaces
class Dim_Background_Surface():
    def __init__(self, Game):
        self.Game = Game
        self.Window = self.Game.Window

        self.Surface = pygame.Surface((self.Game.Width, self.Game.Height)) #Define a new surface
        self.Surface.set_alpha(180) #set the surface alpha(opacity) to 180
        self.Surface.fill((0, 0, 0)) #fill the surface black

        self.Window.blit(
            self.Surface, (0, 0)
        )
    
    def Update(self):
        self.Window.blit(
            self.Surface, (0, 0)
        )





#Game Backgrounds
class Title():
    def __init__(self, Game, Center_x, Center_y):
        #Game related
        self.Game = Game
        self.Window = self.Game.Window

        self.BackGround_img = pygame.transform.scale(
            pygame.image.load(
                os.path.join("assets", "Backgrounds", "MenuBackground.png")
            ), (self.Game.Width, self.Game.Height)
        )

        #Image and Positioning
        self.img_Width, self.img_Height = 864, 288

        self.Title_img = pygame.image.load(
            os.path.join("assets", "UI", "Title.png")
        )

        self.Title_img = pygame.transform.scale(
            self.Title_img, (int(self.img_Width*self.Game.Win_Scale), int(self.img_Height*self.Game.Win_Scale))
        )
        self.img_Width, self.img_Height = self.Title_img.get_size() #update image width and height after rescaling the image
        
        self.Center = ((Center_x*self.Game.Win_Scale), (Center_y*self.Game.Win_Scale))

        self.x, self.y = self.Center[0]-(self.img_Width/2), self.Center[1]-(self.img_Height/2)

        self.Window.blit(
            self.BackGround_img, (0, 0)
        )
        self.Window.blit(
            self.Title_img, (self.x, self.y)
        )
    
    def Update(self):
        self.Window.blit(
            self.BackGround_img, (0, 0)
        )
        self.Window.blit(
            self.Title_img, (self.x, self.y)
        )

class Choose_Charactor_Background():
    def __init__(self, Game):
        self.Game = Game
        self.Background_img = pygame.transform.scale(
            pygame.image.load(
                os.path.join("assets", "Backgrounds", "Choose_Charactor_Background.png")
            ), (self.Game.Width, self.Game.Height)
        )

    def Update(self):
        self.Game.Window.blit(
            self.Background_img, (0, 0)
        )





#Home page use only
class Home_Start_Button():
    def __init__(self, Game, Surface, Center_x, Center_y):
        #Game related
        self.Game = Game
        self.Surface = Surface

        #Image and Positioning
        self.Start_Button_img = pygame.image.load(
            os.path.join("assets", "UI", "Home_Start.png")
        )
        self.img_Width, self.img_Height = self.Start_Button_img.get_size() #update image width and height after rescaling the image

        self.Start_Button_img = pygame.transform.scale(
            self.Start_Button_img, (int(self.img_Width*self.Game.Win_Scale), int(self.img_Height*self.Game.Win_Scale))
        )
        self.Start_Button_img.set_alpha(255)
        self.img_Width, self.img_Height = self.Start_Button_img.get_size() #update image width and height after rescaling the image
        
        self.Center = ((Center_x*self.Game.Win_Scale), (Center_y*self.Game.Win_Scale))

        self.x, self.y = self.Center[0]-(self.img_Width/2), self.Center[1]-(self.img_Height/2)

        self.clone = self.Surface.blit(
            self.Start_Button_img, (self.x, self.y)
        )

        #Values
        self.Pressed = False
        self.Vertexs = self.Get_Vertex()

    def Get_Equation(self):
        # return b of y=ax+b
        b_1 = self.Vertexs[0][1]-self.Vertexs[0][0] #a (slope) = 1
        b_2 = self.Vertexs[1][1]+self.Vertexs[1][0] #a (slope) = -1
        b_3 = self.Vertexs[2][1]-self.Vertexs[2][0] #a (slope) = 1
        b_4 = self.Vertexs[3][1]+self.Vertexs[3][0] #a (slope) = -1
        return (b_1, b_2, b_3, b_4)

    def Get_Vertex(self):
        return (
            (self.x, self.y),
            (self.x+self.img_Width, self.y),
            (self.x+self.img_Width, self.y+self.img_Height),
            (self.x, self.y+self.img_Height),
            (self.x+(self.img_Height/2), self.y+(self.img_Height/2)),
            (self.x+self.img_Width-(self.img_Height/2), self.y+(self.img_Height/2))
        )

    def Detect_hover(self, mouse_x, mouse_y):
        if self.y <= mouse_y <= self.y+self.img_Height:
            if mouse_x < self.x or mouse_x > self.x+self.img_Width:
                return False
            elif self.x+(self.img_Height/2) <= mouse_x <= self.x+self.img_Width-(self.img_Height/2):
                return True
            
            Equation_b = self.Get_Equation()
            if self.y <= mouse_y <= self.y+(self.img_Height/2):
                x_points = [
                    mouse_y-Equation_b[0],
                    -(mouse_y-Equation_b[1])
                ]
                if min(x_points) <= mouse_x <= max(x_points):
                    return True
                else:
                    return False
            elif self.y+(self.img_Height/2) <= self.y+self.img_Height:
                x_points = [
                    mouse_y-Equation_b[2],
                    -(mouse_y-Equation_b[3])
                ]
                if min(x_points) <= mouse_x <= max(x_points):
                    return True
                else:
                    return False
        else:
            return False
    
    def Update(self, mouse_x, mouse_y, left_click):
        scale = 1
        if self.Detect_hover(mouse_x=mouse_x, mouse_y=mouse_y):
            if left_click:
                self.Pressed = True
            elif self.Pressed and not left_click:
                self.Pressed = False
                scale = 1
                return True
        if self.Pressed:
            if not left_click:
                self.Pressed = False
                scale = 1
            else:
                scale = 0.9

        w, h = int(self.img_Width*scale), int(self.img_Height*scale)
        self.clone = self.Surface.blit(
            pygame.transform.scale(
                self.Start_Button_img, (w, h)
            ), (self.Center[0]-(w/2), self.Center[1]-(h/2))
        )
        return False


class Home_Right_Button():
    def __init__(self, Game, Surface, Center_x, Center_y):
        #Game related
        self.Game = Game
        self.Surface = Surface

        #Image and Positioning
        self.Right_Button_img = pygame.image.load(
            os.path.join("assets", "UI", "Home_Right.png")
        )
        self.img_Width, self.img_Height = self.Right_Button_img.get_size() #update image width and height after rescaling the image

        self.Right_Button_img = pygame.transform.scale(
            self.Right_Button_img, (int(self.img_Width*self.Game.Win_Scale), int(self.img_Height*self.Game.Win_Scale))
        )
        self.Right_Button_img.set_alpha(255)
        self.img_Width, self.img_Height = self.Right_Button_img.get_size() #update image width and height after rescaling the image
        
        self.Center = ((Center_x*self.Game.Win_Scale), (Center_y*self.Game.Win_Scale))

        self.x, self.y = self.Center[0]-(self.img_Width/2), self.Center[1]-(self.img_Height/2)

        self.clone = self.Surface.blit(
            self.Right_Button_img, (self.x, self.y)
        )

        #Values
        self.Pressed = False
        self.Vertexs = self.Get_Vertex()
    
    def Get_Equation(self):
        # return b of y=ax+b
        b_1 = self.Vertexs[0][1]+self.Vertexs[0][0] #a (slope) = -1
        b_2 = self.Vertexs[2][1]-self.Vertexs[2][0] #a (slope) = 1
        b_3 = self.Vertexs[3][1]-self.Vertexs[3][0] #a (slope) = 1
        return (b_1, b_2, b_3)

    def Get_Vertex(self):
        return (
            (self.x+(self.img_Height/2), self.y),
            (self.x+self.img_Width-self.img_Height, self.y),
            (self.x+self.img_Width, self.y+self.img_Height),
            (self.x+(self.img_Height/2), self.y+self.img_Height),
            (self.x, self.y+(self.img_Height/2))
        )

    def Detect_hover(self, mouse_x, mouse_y):
        if self.y <= mouse_y <= self.y+self.img_Height:
            if mouse_x < self.x or mouse_x > self.x+self.img_Width:
                return False
            elif self.x+(self.img_Height/2) <= mouse_x <= self.x+self.img_Width-self.img_Height:
                return True
            
            Equation_b = self.Get_Equation()
            if self.y <= mouse_y <= self.y+(self.img_Height/2):
                x_points = [
                    -(mouse_y-Equation_b[0]),
                    mouse_y-Equation_b[1]
                ]
                if min(x_points) <= mouse_x <= max(x_points):
                    return True
                else:
                    return False
            elif self.y+(self.img_Height/2) <= self.y+self.img_Height:
                x_points = [
                    mouse_y-Equation_b[1],
                    mouse_y-Equation_b[2]
                ]
                if min(x_points) <= mouse_x <= max(x_points):
                    return True
                else:
                    return False
        else:
            return False

    def Update(self, mouse_x, mouse_y, left_click):
        scale = 1
        if self.Detect_hover(mouse_x=mouse_x, mouse_y=mouse_y):
            if left_click:
                self.Pressed = True
            elif self.Pressed and not left_click:
                self.Pressed = False
                scale = 1
                return True
        if self.Pressed:
            if not left_click:
                self.Pressed = False
                scale = 1
            else:
                scale = 0.9

        w, h = int(self.img_Width*scale), int(self.img_Height*scale)
        self.clone = self.Surface.blit(
            pygame.transform.scale(
                self.Right_Button_img, (w, h)
            ), (self.Center[0]-(w/2), self.Center[1]-(h/2))
        )
        return False


class Home_Left_Button():
    def __init__(self, Game, Surface, Center_x, Center_y):
        #Game related
        self.Game = Game
        self.Surface = Surface

        #Image and Positioning
        self.Left_Button_img = pygame.image.load(
            os.path.join("assets", "UI", "Home_Left.png")
        )
        self.img_Width, self.img_Height = self.Left_Button_img.get_size() #update image width and height after rescaling the image

        self.Left_Button_img = pygame.transform.scale(
            self.Left_Button_img, (int(self.img_Width*self.Game.Win_Scale), int(self.img_Height*self.Game.Win_Scale))
        )
        self.img_Width, self.img_Height = self.Left_Button_img.get_size() #update image width and height after rescaling the image
        
        self.Center = ((Center_x*self.Game.Win_Scale), (Center_y*self.Game.Win_Scale))

        self.x, self.y = self.Center[0]-(self.img_Width/2), self.Center[1]-(self.img_Height/2)

        self.clone = self.Surface.blit(
            self.Left_Button_img, (self.x, self.y)
        )

        #Values
        self.Pressed = False
        self.Vertexs = self.Get_Vertex()
    
    def Get_Equation(self):
        # return b of y=ax+b
        b_1 = self.Vertexs[0][1]+self.Vertexs[0][0] #a (slope) = -1
        b_2 = self.Vertexs[1][1]-self.Vertexs[1][0] #a (slope) = 1
        b_3 = self.Vertexs[3][1]+self.Vertexs[3][0] #a (slope) = -1
        return (b_1, b_2, b_3)

    def Get_Vertex(self):
        return (
            (self.x+self.img_Height, self.y),
            (self.x+self.img_Width-(self.img_Height/2), self.y),
            (self.x+self.img_Width, self.y+(self.img_Height/2)),
            (self.x+self.img_Width-(self.img_Height/2), self.y+self.img_Height),
            (self.x, self.y+self.img_Height)
        )

    def Detect_hover(self, mouse_x, mouse_y):
        if self.y <= mouse_y <= self.y+self.img_Height:
            if mouse_x < self.x or mouse_x > self.x+self.img_Width:
                return False
            elif self.x+(self.img_Height/2) <= mouse_x <= self.x+self.img_Width-self.img_Height:
                return True
            
            Equation_b = self.Get_Equation()
            if self.y <= mouse_y <= self.y+(self.img_Height/2):
                x_points = [
                    -(mouse_y-Equation_b[0]),
                    mouse_y-Equation_b[1]
                ]
                if min(x_points) <= mouse_x <= max(x_points):
                    return True
                else:
                    return False
            elif self.y+(self.img_Height/2) <= self.y+self.img_Height:
                x_points = [
                    -(mouse_y-Equation_b[0]),
                    -(mouse_y-Equation_b[2])
                ]
                if min(x_points) <= mouse_x <= max(x_points):
                    return True
                else:
                    return False
        else:
            return False

    def Update(self, mouse_x, mouse_y, left_click):
        scale = 1
        if self.Detect_hover(mouse_x=mouse_x, mouse_y=mouse_y):
            if left_click:
                self.Pressed = True
            elif self.Pressed and not left_click:
                self.Pressed = False
                scale = 1
                return True
        if self.Pressed:
            if not left_click:
                self.Pressed = False
                scale = 1
            else:
                scale = 0.9

        w, h = int(self.img_Width*scale), int(self.img_Height*scale)
        self.clone = self.Surface.blit(
            pygame.transform.scale(
                self.Left_Button_img, (w, h)
            ), (self.Center[0]-(w/2), self.Center[1]-(h/2))
        )
        return False





#Choose Save page use only
class Choose_Save():
    def __init__(self, Game, Surface):
        #Game related
        self.Game = Game
        self.Surface = Surface

        self.Button_Container = []

        self.y = 144*self.Game.Win_Scale

        self.Refresh_Buttons()

    def Refresh_Buttons(self):
        del self.Button_Container
        self.Button_Container = [Add_Save_Button(Game=self.Game, Surface=self.Surface, Center_x=self.Game.Width-(60*self.Game.Win_Scale), Center_y=660*self.Game.Win_Scale)]
        idx = 1
        while(os.path.exists(os.path.join("Saves", f"Save_File{idx}.json"))):
            self.Button_Container.append(
                Choose_Save_Button(Game=self.Game, Surface=self.Surface, Center_x=self.Game.Width/2, Center_y=self.y+((180*self.Game.Win_Scale)*(idx-1)), represent=idx)
            )
            idx += 1
        self.min_y = self.Game.Height-(144*self.Game.Win_Scale)-((180*self.Game.Win_Scale)*(idx-2))
        self.max_y = (144*self.Game.Win_Scale)

    def Draw_Button(self):
        for idx, button in enumerate(self.Button_Container[1:]):
            button.Center = (button.Center[0], self.y + (idx*(180*self.Game.Win_Scale)))

    def Update(self, mouse_x, mouse_y, left_click):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.min_y < self.max_y:
                    if event.button == 4:
                        self.y += 72*self.Game.Win_Scale
                        if self.y > self.max_y:
                            self.y = self.max_y
                    elif event.button == 5:
                        self.y -= 72*self.Game.Win_Scale
                        if self.y < self.min_y:
                            self.y = self.min_y
        self.Draw_Button()
        if self.Button_Container[0].Update(mouse_x=mouse_x, mouse_y=mouse_y, left_click=left_click):
            self.Game.Generate_SaveFile()
            self.Refresh_Buttons()
        for button in self.Button_Container:
            if button.Update(mouse_x=mouse_x, mouse_y=mouse_y, left_click=left_click):
                return button.Represent
        return False

class Choose_Save_Button():
    def __init__(self, Game, Surface, Center_x, Center_y, represent):
        #Game related
        self.Game = Game
        self.Surface = Surface

        #Image and Positioning
        self.img_Width, self.img_Height = int(576*self.Game.Win_Scale), int(144*self.Game.Win_Scale)

        self.Choose_Save_Button_img = pygame.image.load(
            os.path.join("assets", "UI", "Choose_SaveFile.png")
        )

        self.Choose_Save_Button_img = pygame.transform.scale(
            self.Choose_Save_Button_img, (self.img_Width, self.img_Height)
        )
        self.Choose_Save_Button_img.set_alpha(255)
        self.img_Width, self.img_Height = self.Choose_Save_Button_img.get_size() #update image width and height after rescaling the image
        
        self.Center = (Center_x, Center_y)

        self.x, self.y = self.Center[0]-(self.img_Width/2), self.Center[1]-(self.img_Height/2)

        self.clone = self.Surface.blit(
            self.Choose_Save_Button_img, (self.x, self.y)
        )

        #Save Texts
        with open(os.path.join("Saves", f"Save_File{represent}.json"), "r") as save_file:
            self.Playing_SaveData = json.load(save_file)
            Create_time = self.Playing_SaveData["Create_Time"]
            Last_Save = self.Playing_SaveData["Last_Save"]

            self.SaveFileTitle = pygame.font.SysFont('Comic Sans MS', int(50*self.Game.Win_Scale)).render(f"Save_File{represent}", True, (0, 0, 0))
            self.SaveDescription1 = pygame.font.SysFont('Comic Sans MS', int(22*self.Game.Win_Scale)).render(
                f"Create Time: {Create_time}", 
                True, (0, 0, 0)
            )
            self.SaveDescription2 = pygame.font.SysFont('Comic Sans MS', int(22*self.Game.Win_Scale)).render(
                f"Last Save: {Last_Save}", 
                True, (0, 0, 0)
            )

        #Values
        self.Represent = f"Save_File{represent}"
        self.Pressed = False

    def Detect_hover(self, mouse_x, mouse_y):
        if (self.y <= mouse_y <= self.y+self.img_Height) and (self.x <= mouse_x <= self.x+self.img_Width):
                return True
        return False

    def Draw(self, scale):
        w, h = int(self.img_Width*scale), int(self.img_Height*scale)
        self.x, self.y = self.Center[0]-(w/2), self.Center[1]-(h/2)
        self.clone = self.Surface.blit(
            pygame.transform.scale(
                self.Choose_Save_Button_img, (w, h)
            ), (self.Center[0]-(w/2), self.Center[1]-(h/2))
        )
        self.SaveFileTitle_clone = self.Surface.blit(
            self.SaveFileTitle, (self.x+(40*self.Game.Win_Scale), self.y+(h/18))
        )
        self.SaveDescription1_clone = self.Surface.blit(
            self.SaveDescription1, (self.x+(40*self.Game.Win_Scale), self.y+(h/2))
        )
        self.SaveDescription2_clone = self.Surface.blit(
            self.SaveDescription2, (self.x+(40*self.Game.Win_Scale), self.y+(h/2)+(h/6))
        )

    def Update(self, mouse_x, mouse_y, left_click):
        scale = 1
        if self.Detect_hover(mouse_x=mouse_x, mouse_y=mouse_y):
            if left_click:
                self.Pressed = True
            elif self.Pressed and not left_click:
                self.Pressed = False
                scale = 1
                return self.Represent
        if self.Pressed:
            if not left_click:
                self.Pressed = False
                scale = 1
            else:
                scale = 0.9
        self.Draw(scale=scale)
        return False

class Add_Save_Button(): #Pause // Achievement // Choose Charactor // Help // Setting
    def __init__(self, Game, Surface, Center_x, Center_y):
        #Game related
        self.Game = Game
        self.Surface = Surface

        #Image and Positioning
        self.img_Width, self.img_Height = int(72*self.Game.Win_Scale), int(72*self.Game.Win_Scale)

        self.Add_Save_Button_img = pygame.image.load(
            os.path.join("assets", "UI", "Add_Save_Button.png")
        )

        self.Add_Save_Button_img = pygame.transform.scale(
            self.Add_Save_Button_img, (self.img_Width, self.img_Height)
        )
        self.Add_Save_Button_img.set_alpha(255)
        self.img_Width, self.img_Height = self.Add_Save_Button_img.get_size() #update image width and height after rescaling the image
        
        self.Center = (Center_x, Center_y)

        self.x, self.y = self.Center[0]-(self.img_Width/2), self.Center[1]-(self.img_Height/2)

        self.clone = self.Surface.blit(
            self.Add_Save_Button_img, (self.x, self.y)
        )

        #Values
        self.Pressed = False

    def Detect_hover(self, mouse_x, mouse_y):
        if (self.y <= mouse_y <= self.y+self.img_Height) and (self.x <= mouse_x <= self.x+self.img_Width):
                return True
        return False

    def Update(self, mouse_x, mouse_y, left_click):
        scale = 1
        if self.Detect_hover(mouse_x=mouse_x, mouse_y=mouse_y):
            if left_click:
                self.Pressed = True
            elif self.Pressed and not left_click:
                self.Pressed = False
                scale = 1
                return True
        if self.Pressed:
            if not left_click:
                self.Pressed = False
                scale = 1
            else:
                scale = 0.9

        w, h = int(self.img_Width*scale), int(self.img_Height*scale)
        self.clone = self.Surface.blit(
            pygame.transform.scale(
                self.Add_Save_Button_img, (w, h)
            ), (self.Center[0]-(w/2), self.Center[1]-(h/2))
        )
        return False






#Global use Buttons
class Setting_Button(): #Home // Pause
    def __init__(self, Game, Surface, Center_x, Center_y):
        #Game related
        self.Game = Game
        self.Surface = Surface

        #Image and Positioning
        self.img_Width, self.img_Height = int(72*self.Game.Win_Scale), int(72*self.Game.Win_Scale)

        self.Setting_Button_img = pygame.image.load(
            os.path.join("assets", "UI", "Setting_Button.png")
        )

        self.Setting_Button_img = pygame.transform.scale(
            self.Setting_Button_img, (self.img_Width, self.img_Height)
        )
        self.Setting_Button_img.set_alpha(255)
        self.img_Width, self.img_Height = self.Setting_Button_img.get_size() #update image width and height after rescaling the image
        
        self.Center = ((Center_x*self.Game.Win_Scale), (Center_y*self.Game.Win_Scale))

        self.x, self.y = self.Center[0]-(self.img_Width/2), self.Center[1]-(self.img_Height/2)

        self.clone = self.Surface.blit(
            self.Setting_Button_img, (self.x, self.y)
        )

        #Values
        self.Pressed = False

    def Detect_hover(self, mouse_x, mouse_y):
        if (self.y <= mouse_y <= self.y+self.img_Height) and (self.x <= mouse_x <= self.x+self.img_Width):
                return True
        return False

    def Update(self, mouse_x, mouse_y, left_click):
        scale = 1
        if self.Detect_hover(mouse_x=mouse_x, mouse_y=mouse_y):
            if left_click:
                self.Pressed = True
            elif self.Pressed and not left_click:
                self.Pressed = False
                scale = 1
                return True
        if self.Pressed:
            if not left_click:
                self.Pressed = False
                scale = 1
            else:
                scale = 0.9

        w, h = int(self.img_Width*scale), int(self.img_Height*scale)
        self.clone = self.Surface.blit(
            pygame.transform.scale(
                self.Setting_Button_img, (w, h)
            ), (self.Center[0]-(w/2), self.Center[1]-(h/2))
        )
        return False


class Exit_Button(): #Home // Pause
    def __init__(self, Game, Surface, Center_x, Center_y):
        #Game related
        self.Game = Game
        self.Surface = Surface

        #Image and Positioning
        self.img_Width, self.img_Height = int(72*self.Game.Win_Scale), int(72*self.Game.Win_Scale)

        self.Exit_Button_img = pygame.image.load(
            os.path.join("assets", "UI", "Exit_Button.png")
        )

        self.Exit_Button_img = pygame.transform.scale(
            self.Exit_Button_img, (self.img_Width, self.img_Height)
        )
        self.Exit_Button_img.set_alpha(255)
        self.img_Width, self.img_Height = self.Exit_Button_img.get_size() #update image width and height after rescaling the image
        
        self.Center = ((Center_x*self.Game.Win_Scale), (Center_y*self.Game.Win_Scale))

        self.x, self.y = self.Center[0]-(self.img_Width/2), self.Center[1]-(self.img_Height/2)

        self.clone = self.Surface.blit(
            self.Exit_Button_img, (self.x, self.y)
        )

        #Values
        self.Pressed = False

    def Detect_hover(self, mouse_x, mouse_y):
        if (self.y <= mouse_y <= self.y+self.img_Height) and (self.x <= mouse_x <= self.x+self.img_Width):
                return True
        return False

    def Update(self, mouse_x, mouse_y, left_click):
        scale = 1
        if self.Detect_hover(mouse_x=mouse_x, mouse_y=mouse_y):
            if left_click:
                self.Pressed = True
            elif self.Pressed and not left_click:
                self.Pressed = False
                scale = 1
                return True
        if self.Pressed:
            if not left_click:
                self.Pressed = False
                scale = 1
            else:
                scale = 0.9

        w, h = int(self.img_Width*scale), int(self.img_Height*scale)
        self.clone = self.Surface.blit(
            pygame.transform.scale(
                self.Exit_Button_img, (w, h)
            ), (self.Center[0]-(w/2), self.Center[1]-(h/2))
        )
        return False



class Help_Button(): #Home // Pause
    def __init__(self, Game, Surface, Center_x, Center_y):
        #Game related
        self.Game = Game
        self.Surface = Surface

        #Image and Positioning
        self.img_Width, self.img_Height = int(72*self.Game.Win_Scale), int(72*self.Game.Win_Scale)

        self.Help_Button_img = pygame.image.load(
            os.path.join("assets", "UI", "Help_Button.png")
        )

        self.Help_Button_img = pygame.transform.scale(
            self.Help_Button_img, (self.img_Width, self.img_Height)
        )
        self.Help_Button_img.set_alpha(255)
        self.img_Width, self.img_Height = self.Help_Button_img.get_size() #update image width and height after rescaling the image
        
        self.Center = ((Center_x*self.Game.Win_Scale), (Center_y*self.Game.Win_Scale))

        self.x, self.y = self.Center[0]-(self.img_Width/2), self.Center[1]-(self.img_Height/2)

        self.clone = self.Surface.blit(
            self.Help_Button_img, (self.x, self.y)
        )

        #Values
        self.Pressed = False

    def Detect_hover(self, mouse_x, mouse_y):
        if (self.y <= mouse_y <= self.y+self.img_Height) and (self.x <= mouse_x <= self.x+self.img_Width):
                return True
        return False

    def Update(self, mouse_x, mouse_y, left_click):
        scale = 1
        if self.Detect_hover(mouse_x=mouse_x, mouse_y=mouse_y):
            if left_click:
                self.Pressed = True
            elif self.Pressed and not left_click:
                self.Pressed = False
                scale = 1
                return True
        if self.Pressed:
            if not left_click:
                self.Pressed = False
                scale = 1
            else:
                scale = 0.9

        w, h = int(self.img_Width*scale), int(self.img_Height*scale)
        self.clone = self.Surface.blit(
            pygame.transform.scale(
                self.Help_Button_img, (w, h)
            ), (self.Center[0]-(w/2), self.Center[1]-(h/2))
        )
        return False



class Achievement_Button(): #Pause
    def __init__(self, Game, Surface, Center_x, Center_y):
        #Game related
        self.Game = Game
        self.Surface = Surface

        #Image and Positioning
        self.img_Width, self.img_Height = int(72*self.Game.Win_Scale), int(72*self.Game.Win_Scale)

        self.Achievement_Button_img = pygame.image.load(
            os.path.join("assets", "UI", "Achievement_Button.png")
        )

        self.Achievement_Button_img = pygame.transform.scale(
            self.Achievement_Button_img, (self.img_Width, self.img_Height)
        )
        self.Achievement_Button_img.set_alpha(255)
        self.img_Width, self.img_Height = self.Achievement_Button_img.get_size() #update image width and height after rescaling the image
        
        self.Center = ((Center_x*self.Game.Win_Scale), (Center_y*self.Game.Win_Scale))

        self.x, self.y = self.Center[0]-(self.img_Width/2), self.Center[1]-(self.img_Height/2)

        self.clone = self.Surface.blit(
            self.Achievement_Button_img, (self.x, self.y)
        )

        #Values
        self.Pressed = False

    def Detect_hover(self, mouse_x, mouse_y):
        if (self.y <= mouse_y <= self.y+self.img_Height) and (self.x <= mouse_x <= self.x+self.img_Width):
                return True
        return False

    def Update(self, mouse_x, mouse_y, left_click):
        scale = 1
        if self.Detect_hover(mouse_x=mouse_x, mouse_y=mouse_y):
            if left_click:
                self.Pressed = True
            elif self.Pressed and not left_click:
                self.Pressed = False
                scale = 1
                return True
        if self.Pressed:
            if not left_click:
                self.Pressed = False
                scale = 1
            else:
                scale = 0.9

        w, h = int(self.img_Width*scale), int(self.img_Height*scale)
        self.clone = self.Surface.blit(
            pygame.transform.scale(
                self.Achievement_Button_img, (w, h)
            ), (self.Center[0]-(w/2), self.Center[1]-(h/2))
        )
        return False



class Respawn_Button(): #Pause
    def __init__(self, Game, Surface, Center_x, Center_y):
        #Game related
        self.Game = Game
        self.Surface = Surface

        #Image and Positioning
        self.img_Width, self.img_Height = int(72*self.Game.Win_Scale), int(72*self.Game.Win_Scale)

        self.Respawn_Button_img = pygame.image.load(
            os.path.join("assets", "UI", "Respawn_Button.png")
        )

        self.Respawn_Button_img = pygame.transform.scale(
            self.Respawn_Button_img, (self.img_Width, self.img_Height)
        )
        self.Respawn_Button_img.set_alpha(255)
        self.img_Width, self.img_Height = self.Respawn_Button_img.get_size() #update image width and height after rescaling the image
        
        self.Center = ((Center_x*self.Game.Win_Scale), (Center_y*self.Game.Win_Scale))

        self.x, self.y = self.Center[0]-(self.img_Width/2), self.Center[1]-(self.img_Height/2)

        self.clone = self.Surface.blit(
            self.Respawn_Button_img, (self.x, self.y)
        )

        #Values
        self.Pressed = False

    def Detect_hover(self, mouse_x, mouse_y):
        if (self.y <= mouse_y <= self.y+self.img_Height) and (self.x <= mouse_x <= self.x+self.img_Width):
                return True
        return False

    def Update(self, mouse_x, mouse_y, left_click):
        scale = 1
        if self.Detect_hover(mouse_x=mouse_x, mouse_y=mouse_y):
            if left_click:
                self.Pressed = True
            elif self.Pressed and not left_click:
                self.Pressed = False
                scale = 1
                return True
        if self.Pressed:
            if not left_click:
                self.Pressed = False
                scale = 1
            else:
                scale = 0.9

        w, h = int(self.img_Width*scale), int(self.img_Height*scale)
        self.clone = self.Surface.blit(
            pygame.transform.scale(
                self.Respawn_Button_img, (w, h)
            ), (self.Center[0]-(w/2), self.Center[1]-(h/2))
        )
        return False



class Return_Button(): #Pause // Achievement // Choose Charactor // Help // Setting
    def __init__(self, Game, Surface, Center_x, Center_y):
        #Game related
        self.Game = Game
        self.Surface = Surface

        #Image and Positioning
        self.img_Width, self.img_Height = int(72*self.Game.Win_Scale), int(72*self.Game.Win_Scale)

        self.Return_Button_img = pygame.image.load(
            os.path.join("assets", "UI", "Return_Button.png")
        )

        self.Return_Button_img = pygame.transform.scale(
            self.Return_Button_img, (self.img_Width, self.img_Height)
        )
        self.Return_Button_img.set_alpha(255)
        self.img_Width, self.img_Height = self.Return_Button_img.get_size() #update image width and height after rescaling the image
        
        self.Center = ((Center_x*self.Game.Win_Scale), (Center_y*self.Game.Win_Scale))

        self.x, self.y = self.Center[0]-(self.img_Width/2), self.Center[1]-(self.img_Height/2)

        self.clone = self.Surface.blit(
            self.Return_Button_img, (self.x, self.y)
        )

        #Values
        self.Pressed = False

    def Detect_hover(self, mouse_x, mouse_y):
        if (self.y <= mouse_y <= self.y+self.img_Height) and (self.x <= mouse_x <= self.x+self.img_Width):
                return True
        return False

    def Update(self, mouse_x, mouse_y, left_click):
        scale = 1
        if self.Detect_hover(mouse_x=mouse_x, mouse_y=mouse_y):
            if left_click:
                self.Pressed = True
            elif self.Pressed and not left_click:
                self.Pressed = False
                scale = 1
                return True
        if self.Pressed:
            if not left_click:
                self.Pressed = False
                scale = 1
            else:
                scale = 0.9

        w, h = int(self.img_Width*scale), int(self.img_Height*scale)
        self.clone = self.Surface.blit(
            pygame.transform.scale(
                self.Return_Button_img, (w, h)
            ), (self.Center[0]-(w/2), self.Center[1]-(h/2))
        )
        return False



class Home_Button(): #Pause
    def __init__(self, Game, Surface, Center_x, Center_y):
        #Game related
        self.Game = Game
        self.Surface = Surface

        #Image and Positioning
        self.img_Width, self.img_Height = int(72*self.Game.Win_Scale), int(72*self.Game.Win_Scale)

        self.Home_Button_img = pygame.image.load(
            os.path.join("assets", "UI", "Home_Button.png")
        )

        self.Home_Button_img = pygame.transform.scale(
            self.Home_Button_img, (self.img_Width, self.img_Height)
        )
        self.Home_Button_img.set_alpha(255)
        self.img_Width, self.img_Height = self.Home_Button_img.get_size() #update image width and height after rescaling the image
        
        self.Center = ((Center_x*self.Game.Win_Scale), (Center_y*self.Game.Win_Scale))

        self.x, self.y = self.Center[0]-(self.img_Width/2), self.Center[1]-(self.img_Height/2)

        self.clone = self.Surface.blit(
            self.Home_Button_img, (self.x, self.y)
        )

        #Values
        self.Pressed = False

    def Detect_hover(self, mouse_x, mouse_y):
        if (self.y <= mouse_y <= self.y+self.img_Height) and (self.x <= mouse_x <= self.x+self.img_Width):
                return True
        return False

    def Update(self, mouse_x, mouse_y, left_click):
        scale = 1
        if self.Detect_hover(mouse_x=mouse_x, mouse_y=mouse_y):
            if left_click:
                self.Pressed = True
            elif self.Pressed and not left_click:
                self.Pressed = False
                scale = 1
                return True
        if self.Pressed:
            if not left_click:
                self.Pressed = False
                scale = 1
            else:
                scale = 0.9

        w, h = int(self.img_Width*scale), int(self.img_Height*scale)
        self.clone = self.Surface.blit(
            pygame.transform.scale(
                self.Home_Button_img, (w, h)
            ), (self.Center[0]-(w/2), self.Center[1]-(h/2))
        )
        return False



#Setting Buttons
class Game_Setting_Button():
    def __init__(self, Game, Surface, Center_x, Center_y):
        #Game related
        self.Game = Game
        self.Surface = Surface

        #Image and Positioning
        self.img_Width, self.img_Height = int(288*self.Game.Win_Scale), int(72*self.Game.Win_Scale)

        self.Game_Setting_Button_img = pygame.image.load(
            os.path.join("assets", "UI", "Game_Setting_Button.png")
        )

        self.Game_Setting_Button_img = pygame.transform.scale(
            self.Game_Setting_Button_img, (self.img_Width, self.img_Height)
        )
        self.Game_Setting_Button_img.set_alpha(255)
        self.img_Width, self.img_Height = self.Game_Setting_Button_img.get_size() #update image width and height after rescaling the image
        
        self.Center = ((Center_x*self.Game.Win_Scale), (Center_y*self.Game.Win_Scale))

        self.x, self.y = self.Center[0]-(self.img_Width/2), self.Center[1]-(self.img_Height/2)

        self.clone = self.Surface.blit(
            self.Game_Setting_Button_img, (self.x, self.y)
        )

        #Values
        self.Pressed = False

    def Detect_hover(self, mouse_x, mouse_y):
        if (self.y <= mouse_y <= self.y+self.img_Height) and (self.x <= mouse_x <= self.x+self.img_Width):
                return True
        return False

    def Update(self, mouse_x, mouse_y, left_click):
        scale = 1
        if self.Detect_hover(mouse_x=mouse_x, mouse_y=mouse_y):
            if left_click:
                self.Pressed = True
            elif self.Pressed and not left_click:
                self.Pressed = False
                scale = 1
                return True
        if self.Pressed:
            if not left_click:
                self.Pressed = False
                scale = 1
            else:
                scale = 0.9

        w, h = int(self.img_Width*scale), int(self.img_Height*scale)
        self.clone = self.Surface.blit(
            pygame.transform.scale(
                self.Game_Setting_Button_img, (w, h)
            ), (self.Center[0]-(w/2), self.Center[1]-(h/2))
        )
        return False



class Audio_Setting_Button():
    def __init__(self, Game, Surface, Center_x, Center_y):
        #Game related
        self.Game = Game
        self.Surface = Surface

        #Image and Positioning
        self.img_Width, self.img_Height = int(288*self.Game.Win_Scale), int(72*self.Game.Win_Scale)

        self.Audio_Setting_Button_img = pygame.image.load(
            os.path.join("assets", "UI", "Audio_Setting_Button.png")
        )

        self.Audio_Setting_Button_img = pygame.transform.scale(
            self.Audio_Setting_Button_img, (self.img_Width, self.img_Height)
        )
        self.Audio_Setting_Button_img.set_alpha(255)
        self.img_Width, self.img_Height = self.Audio_Setting_Button_img.get_size() #update image width and height after rescaling the image
        
        self.Center = ((Center_x*self.Game.Win_Scale), (Center_y*self.Game.Win_Scale))

        self.x, self.y = self.Center[0]-(self.img_Width/2), self.Center[1]-(self.img_Height/2)

        self.clone = self.Surface.blit(
            self.Audio_Setting_Button_img, (self.x, self.y)
        )

        #Values
        self.Pressed = False

    def Detect_hover(self, mouse_x, mouse_y):
        if (self.y <= mouse_y <= self.y+self.img_Height) and (self.x <= mouse_x <= self.x+self.img_Width):
                return True
        return False

    def Update(self, mouse_x, mouse_y, left_click):
        scale = 1
        if self.Detect_hover(mouse_x=mouse_x, mouse_y=mouse_y):
            if left_click:
                self.Pressed = True
            elif self.Pressed and not left_click:
                self.Pressed = False
                scale = 1
                return True
        if self.Pressed:
            if not left_click:
                self.Pressed = False
                scale = 1
            else:
                scale = 0.9

        w, h = int(self.img_Width*scale), int(self.img_Height*scale)
        self.clone = self.Surface.blit(
            pygame.transform.scale(
                self.Audio_Setting_Button_img, (w, h)
            ), (self.Center[0]-(w/2), self.Center[1]-(h/2))
        )
        return False



class Video_Setting_Button():
    def __init__(self, Game, Surface, Center_x, Center_y):
        #Game related
        self.Game = Game
        self.Surface = Surface

        #Image and Positioning
        self.img_Width, self.img_Height = int(288*self.Game.Win_Scale), int(72*self.Game.Win_Scale)

        self.Video_Setting_Button_img = pygame.image.load(
            os.path.join("assets", "UI", "Video_Setting_Button.png")
        )

        self.Video_Setting_Button_img = pygame.transform.scale(
            self.Video_Setting_Button_img, (self.img_Width, self.img_Height)
        )
        self.Video_Setting_Button_img.set_alpha(255)
        self.img_Width, self.img_Height = self.Video_Setting_Button_img.get_size() #update image width and height after rescaling the image
        
        self.Center = ((Center_x*self.Game.Win_Scale), (Center_y*self.Game.Win_Scale))

        self.x, self.y = self.Center[0]-(self.img_Width/2), self.Center[1]-(self.img_Height/2)

        self.clone = self.Surface.blit(
            self.Video_Setting_Button_img, (self.x, self.y)
        )

        #Values
        self.Pressed = False

    def Detect_hover(self, mouse_x, mouse_y):
        if (self.y <= mouse_y <= self.y+self.img_Height) and (self.x <= mouse_x <= self.x+self.img_Width):
                return True
        return False

    def Update(self, mouse_x, mouse_y, left_click):
        scale = 1
        if self.Detect_hover(mouse_x=mouse_x, mouse_y=mouse_y):
            if left_click:
                self.Pressed = True
            elif self.Pressed and not left_click:
                self.Pressed = False
                scale = 1
                return True
        if self.Pressed:
            if not left_click:
                self.Pressed = False
                scale = 1
            else:
                scale = 0.9

        w, h = int(self.img_Width*scale), int(self.img_Height*scale)
        self.clone = self.Surface.blit(
            pygame.transform.scale(
                self.Video_Setting_Button_img, (w, h)
            ), (self.Center[0]-(w/2), self.Center[1]-(h/2))
        )
        return False



class Keyboard_Setting_Button():
    def __init__(self, Game, Surface, Center_x, Center_y):
        #Game related
        self.Game = Game
        self.Surface = Surface

        #Image and Positioning
        self.img_Width, self.img_Height = int(288*self.Game.Win_Scale), int(72*self.Game.Win_Scale)

        self.Keyboard_Setting_Button_img = pygame.image.load(
            os.path.join("assets", "UI", "Keyboard_Setting_Button.png")
        )

        self.Keyboard_Setting_Button_img = pygame.transform.scale(
            self.Keyboard_Setting_Button_img, (self.img_Width, self.img_Height)
        )
        self.Keyboard_Setting_Button_img.set_alpha(255)
        self.img_Width, self.img_Height = self.Keyboard_Setting_Button_img.get_size() #update image width and height after rescaling the image
        
        self.Center = ((Center_x*self.Game.Win_Scale), (Center_y*self.Game.Win_Scale))

        self.x, self.y = self.Center[0]-(self.img_Width/2), self.Center[1]-(self.img_Height/2)

        self.clone = self.Surface.blit(
            self.Keyboard_Setting_Button_img, (self.x, self.y)
        )

        #Values
        self.Pressed = False

    def Detect_hover(self, mouse_x, mouse_y):
        if (self.y <= mouse_y <= self.y+self.img_Height) and (self.x <= mouse_x <= self.x+self.img_Width):
                return True
        return False

    def Update(self, mouse_x, mouse_y, left_click):
        scale = 1
        if self.Detect_hover(mouse_x=mouse_x, mouse_y=mouse_y):
            if left_click:
                self.Pressed = True
            elif self.Pressed and not left_click:
                self.Pressed = False
                scale = 1
                return True
        if self.Pressed:
            if not left_click:
                self.Pressed = False
                scale = 1
            else:
                scale = 0.9

        w, h = int(self.img_Width*scale), int(self.img_Height*scale)
        self.clone = self.Surface.blit(
            pygame.transform.scale(
                self.Keyboard_Setting_Button_img, (w, h)
            ), (self.Center[0]-(w/2), self.Center[1]-(h/2))
        )
        return False








#Special Buttons
class Choose_Charactor_Button():
    def __init__(self, Game, Charactor_Name, Center_x, Center_y):
        #Game related
        self.Game = Game
        self.Window = self.Game.Window

        #Button Image and Positioning
        self.img_Width, self.img_Height = int(72*self.Game.Win_Scale), int(72*self.Game.Win_Scale)

        self.Button_Frame_img = pygame.image.load(
            os.path.join("assets", "UI", "Button_Frame.png")
        )

        self.Button_Frame_img = pygame.transform.scale(
            self.Button_Frame_img, (self.img_Width, self.img_Height)
        )
        self.Button_Frame_img.set_alpha(255)
        self.img_Width, self.img_Height = self.Button_Frame_img.get_size() #update image width and height after rescaling the image
        
        self.Center = ((Center_x*self.Game.Win_Scale), (Center_y*self.Game.Win_Scale))

        self.x, self.y = self.Center[0]-(self.img_Width/2), self.Center[1]-(self.img_Height/2)

        self.clone = self.Window.blit(
            self.Button_Frame_img, (self.x, self.y)
        )

        #Button Icon and Positioning
        self.Represent = Charactor_Name

        self.Icon_img = pygame.transform.scale(
            pygame.image.load(
                os.path.join("assets", "Charactor", f"{Charactor_Name}.png")
            ), (int(self.img_Width/36*23), int(self.img_Height/36*23))
        )
        self.Icon_img.set_alpha(255)
        self.Icon_img_size = self.Icon_img.get_size()

        self.Icon_x, self.Icon_y = self.Center[0]-(self.Icon_img_size[0]/2), self.Center[1]-(self.Icon_img_size[1]/2)

        self.Icon = self.Window.blit(
            self.Icon_img, (self.Icon_x, self.Icon_y)
        )

        #Values
        self.Pressed = False

    def Detect_hover(self, mouse_x, mouse_y):
        if (self.y <= mouse_y <= self.y+self.img_Height) and (self.x <= mouse_x <= self.x+self.img_Width):
                return True
        return False

    def Update(self, mouse_x, mouse_y, left_click):
        scale = 1
        if self.Detect_hover(mouse_x=mouse_x, mouse_y=mouse_y):
            if left_click:
                self.Pressed = True
            elif self.Pressed and not left_click:
                self.Pressed = False
                scale = 1
                return True
        if self.Pressed:
            if not left_click:
                self.Pressed = False
                scale = 1
            else:
                scale = 0.9

        Frame_w, Frame_h = int(self.img_Width*scale), int(self.img_Height*scale)
        self.clone = self.Window.blit(
            pygame.transform.scale(
                self.Button_Frame_img, (Frame_w, Frame_h)
            ), (self.Center[0]-(Frame_w/2), self.Center[1]-(Frame_h/2))
        )
        Icon_w, Icon_h = int(Frame_w/36*23*scale), int(Frame_h/36*23*scale)
        self.Icon = self.Window.blit(
            pygame.transform.scale(
                self.Icon_img, (Icon_w, Icon_h)
            ), (self.Center[0]-(Icon_w/2), self.Center[1]-(Icon_h/2))
        )
        return False















class UI_System():
    def __init__(self, Game):
        self.Game = Game

        self.Current = None

        self.UIs = {
            "Home_Page":self.Home_Page,
            "Pause_Page":self.Pause_Page,
            "Choose_Charactor_Page":self.Choose_Charactor_Page,
            "Choose_Save_Page":self.Choose_Save_Page,
            "Achievement_Page":self.Achievement_Page,
            "Help_Page":self.Help_Page,
            "Setting_Page":self.Setting_Page
        }

        self.Surfaces = []
        self.UI_Elements = {}
        self.Image_Backgrounds = []

    def Test_All_Button(self):
        self.UI_Elements = {
            Home_Start_Button( Game=self.Game, Surface=self.Game.Window, Center_x=480, Center_y=570):"Play",
            Home_Right_Button( Game=self.Game, Surface=self.Game.Window, Center_x=750, Center_y=570):"Right",
            Home_Left_Button(  Game=self.Game, Surface=self.Game.Window, Center_x=210, Center_y=570):"Left",
            Setting_Button(    Game=self.Game, Surface=self.Game.Window, Center_x=60,  Center_y=60) :"Setting",
            Help_Button(       Game=self.Game, Surface=self.Game.Window, Center_x=150, Center_y=60) :"Help",
            Exit_Button(       Game=self.Game, Surface=self.Game.Window, Center_x=240, Center_y=60) :"Exit",
            Achievement_Button(Game=self.Game, Surface=self.Game.Window, Center_x=330, Center_y=60) :"Achievement",
            Respawn_Button(    Game=self.Game, Surface=self.Game.Window, Center_x=420, Center_y=60) :"Respawn",
            Return_Button(     Game=self.Game, Surface=self.Game.Window, Center_x=510, Center_y=60) :"Return",

            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Baize",           Center_x=60,  Center_y=150):"Baize",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Green_Elf",       Center_x=150, Center_y=150):"Green_Elf",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Knight",          Center_x=240, Center_y=150):"Knight",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Ninja",           Center_x=330, Center_y=150):"Ninja",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Panda",           Center_x=420, Center_y=150):"Panda",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Yellow_Triangle", Center_x=510, Center_y=150):"Yellow_Triangle",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Rice_Ball",       Center_x=600, Center_y=150):"Rice_Ball",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Bloodly_Poop",    Center_x=690, Center_y=150):"Bloodly_Poop",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Poop",            Center_x=780, Center_y=150):"Poop",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Finn",            Center_x=870, Center_y=150):"Finn",
        }


    #Home Page
    def Home_Page(self):
        self.Surfaces = []
        self.Image_Backgrounds = [Title(Game=self.Game, Center_x=480, Center_y=340)]
        self.UI_Elements = {
            Home_Start_Button(Game=self.Game, Surface=self.Game.Window, Center_x=480, Center_y=570):"Play",
            Home_Right_Button(Game=self.Game, Surface=self.Game.Window, Center_x=750, Center_y=570):"Choose_Charactor",
            Home_Left_Button( Game=self.Game, Surface=self.Game.Window, Center_x=210, Center_y=570):"Achievement",
            Setting_Button(   Game=self.Game, Surface=self.Game.Window, Center_x=900, Center_y=60) :"Setting",
            Help_Button(      Game=self.Game, Surface=self.Game.Window, Center_x=900, Center_y=150):"Help",
            Exit_Button(      Game=self.Game, Surface=self.Game.Window, Center_x=60 , Center_y=60) :"Exit"
        }
        self.Current = self.Home_Page


    #Pause Page
    def Pause_Page(self):
        self.Surfaces = [Dim_Background_Surface(Game=self.Game)]
        self.Image_Backgrounds = []
        self.UI_Elements = {
            Setting_Button(    Game=self.Game, Surface=self.Game.Window, Center_x=300, Center_y=360):"Setting",
            Help_Button(       Game=self.Game, Surface=self.Game.Window, Center_x=390, Center_y=360):"Help",
            Home_Button(       Game=self.Game, Surface=self.Game.Window, Center_x=480, Center_y=360):"Home",
            Achievement_Button(Game=self.Game, Surface=self.Game.Window, Center_x=570, Center_y=360):"Achievement",
            Respawn_Button(    Game=self.Game, Surface=self.Game.Window, Center_x=660, Center_y=360):"Respawn",
            Return_Button(     Game=self.Game, Surface=self.Game.Window, Center_x=60,  Center_y=660):"Return",
        }
        self.Current = self.Pause_Page


    #Choose Charactor Page
    def Choose_Charactor_Page(self):
        self.Surfaces = []
        self.Image_Backgrounds = [Choose_Charactor_Background(Game=self.Game)]
        self.UI_Elements = {
            Return_Button(          Game=self.Game, Surface=self.Game.Window        , Center_x=60 , Center_y=660):"Return",

            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Baize"          , Center_x=75 , Center_y=315):"Baize",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Green_Elf"      , Center_x=165, Center_y=315):"Green_Elf",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Knight"         , Center_x=255, Center_y=315):"Knight",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Ninja"          , Center_x=345, Center_y=315):"Ninja",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Panda"          , Center_x=435, Center_y=315):"Panda",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Yellow_Triangle", Center_x=525, Center_y=315):"Yellow_Triangle",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Rice_Ball"      , Center_x=615, Center_y=315):"Rice_Ball",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Bloodly_Poop"   , Center_x=705, Center_y=315):"Bloodly_Poop",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Poop"           , Center_x=795, Center_y=315):"Poop",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Finn"           , Center_x=885, Center_y=315):"Finn",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Dino"           , Center_x=75 , Center_y=405):"Dino",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Puppy"          , Center_x=165, Center_y=405):"Puppy",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Sus"            , Center_x=255, Center_y=405):"Sus",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Ghosty"         , Center_x=345, Center_y=405):"Ghosty",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Orby"           , Center_x=435, Center_y=405):"Orby",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="Skull"          , Center_x=525, Center_y=405):"Skull",
            Choose_Charactor_Button(Game=self.Game, Charactor_Name="AAACube"        , Center_x=615, Center_y=405):"AAACube",
            # Choose_Charactor_Button(Game=self.Game, Charactor_Name="Bloodly_Poop",    Center_x=705, Center_y=405):"Bloodly_Poop",
            # Choose_Charactor_Button(Game=self.Game, Charactor_Name="Poop",            Center_x=795, Center_y=405):"Poop",
            # Choose_Charactor_Button(Game=self.Game, Charactor_Name="Finn",            Center_x=885, Center_y=405):"Finn",
        }
        self.Current = self.Choose_Charactor_Page


    #Choose Save Page
    def Choose_Save_Page(self):
        self.Surfaces = []
        self.Image_Backgrounds = [Choose_Charactor_Background(Game=self.Game)]
        self.UI_Elements = {
            Return_Button(Game=self.Game, Surface=self.Game.Window, Center_x=60                , Center_y=660):"Return",

            Choose_Save(  Game=self.Game, Surface=self.Game.Window                                           ):"None"
        }
        self.Current = self.Choose_Save_Page


    #Achievement Page
    def Achievement_Page(self):
        self.Current = self.Achievement_Page
        pass


    #Help Page
    def Help_Page(self):
        self.Current = self.Help_Page
        pass


    #Setting Pages
    def Setting_Page(self):
        self.Surfaces = [Dim_Background_Surface(Game=self.Game)]
        self.Image_Backgrounds = []
        self.UI_Elements = {
            Return_Button(          Game=self.Game, Surface=self.Game.Window, Center_x= 60, Center_y=660):"Return",

            Game_Setting_Button(    Game=self.Game, Surface=self.Game.Window, Center_x=480, Center_y=216):"Game",
            Audio_Setting_Button(   Game=self.Game, Surface=self.Game.Window, Center_x=480, Center_y=312):"Audio",
            Video_Setting_Button(   Game=self.Game, Surface=self.Game.Window, Center_x=480, Center_y=408):"Video",
            Keyboard_Setting_Button(Game=self.Game, Surface=self.Game.Window, Center_x=480, Center_y=504):"Keyboard"
        }
        self.Current = self.Setting_Page
        pass

    def Game_Setting_Page(self):
        pass

    def Audio_Setting_Page(self):
        pass

    def Video_Setting_Page(self):
        pass

    def KeyBind_Setting_Page(self):
        pass


    #Refresh all elements
    def Refresh(self):
        if self.Current:
            self.Current()
        else:
            pass


    #Update all elements
    def Update(self):
        for surface in self.Surfaces:
            surface.Update()
        for image in self.Image_Backgrounds:
            image.Update()
        for element in self.UI_Elements.items():
            mouse_position = pygame.mouse.get_pos()
            result = element[0].Update(mouse_x=mouse_position[0], mouse_y=mouse_position[1], left_click=pygame.mouse.get_pressed()[0])
            if result==True:
                return element[1]
            elif result:
                return result