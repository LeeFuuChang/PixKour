import time



class History_Stack():
    def __init__(self):
        self.List = []

    def Push(self, arguments):
        self.List.append(arguments)

    def Pop(self):
        self.List.pop(-1)
        return self.List[-1]

    def Get(self):
        return self.List[-1]


class Event_System():
    def __init__(self):
        self.Start_Time = time.time()
        self.Timers = {}
        self.Events = {}

    def Make_Event(self, Event_Name, Time): #Events[Timer_Name] = (Current_Time, TimeToEvent)
        self.Timers[Event_Name] = (time.time()-self.Start_Time, Time)
        self.Events[Event_Name] = False

    def Remove_Timer(self, Event_Name):
        del self.Timers[Event_Name]
        del self.Events[Event_Name]

    def Reset(self):
        self.Start_Time = time.time()
        for Event_Name, elements in self.Timers.items(): 
            self.Timers[Event_Name] = (time.time()-self.Start_Time, elements[1])
            self.Events[Event_Name] = False

    def Get_Events(self):
        return self.Events

    def Update(self):
        Current_Time = int(time.time()-self.Start_Time)
        for Event_Name, Elements in self.Timers.items(): #Elements = (Event_Create_Time, Event_Loop_Time)
            if int(Current_Time-Elements[0])%int(Elements[1]) == 0:
                self.Events[Event_Name] = True
            else:
                self.Events[Event_Name] = False


class Handle_Keys():
    Key_IDs = {
        "esc": 27, 
        "f1": 1073741882, 
        "f2": 1073741883, 
        "f3": 1073741884, 
        "f4": 1073741885, 
        "f5": 1073742085, 
        "f6": 1073742084, 
        "f7": 1073742083, 
        "f8": 1073742082, 
        "f9": 1073742086, 
        "f10": 1073741953, 
        "f11": 1073741952, 
        "f12": 1073742051, 
        "~": 96, 
        "1": 49, 
        "2": 50, 
        "3": 51, 
        "4": 52, 
        "5": 53, 
        "6": 54, 
        "7": 55, 
        "8": 56, 
        "9": 57, 
        "0": 48, 
        "-": 45, 
        "=": 61, 
        "backspace": 8, 
        "tab": 9, 
        "q": 113, 
        "w": 119, 
        "e": 101, 
        "r": 114, 
        "t": 116, 
        "y": 121, 
        "u": 117, 
        "i": 105, 
        "o": 111, 
        "p": 112, 
        "[": 91, 
        "]": 93, 
        "\\": 92, 
        "caps": 1073741881, 
        "a": 97, 
        "s": 115, 
        "d": 100, 
        "f": 102, 
        "g": 103, 
        "h": 104, 
        "j": 106, 
        "k": 107, 
        "l": 108, 
        ";": 59, 
        "'": 39, 
        "return": 13, 
        "lshift": 1073742049, 
        "z": 122, 
        "x": 120, 
        "c": 99, 
        "v": 118, 
        "b": 98, 
        "n": 110, 
        "m": 109, 
        ",": 44, 
        ".": 46, 
        "/": 47, 
        "rshift": 1073742053, 
        "lctrl": 1073742048,
        "lalt": 1073742050, 
        "space": 32, 
        "ralt": 1073742054, 
        "rctrl": 1073742052, 
        "up": 1073741906, 
        "down": 1073741905, 
        "left": 1073741904, 
        "right": 1073741903, 
        "numpad[lock]": 1073741907, 
        "numpad[/]": 1073741908, 
        "numpad[*]": 1073741909, 
        "numpad[-]": 1073741910, 
        "numpad[7]": 1073741919, 
        "numpad[8]": 1073741920, 
        "numpad[9]": 1073741921, 
        "numpad[+]": 1073741911, 
        "numpad[4]": 1073741916, 
        "numpad[5]": 1073741917, 
        "numpad[6]": 1073741918, 
        "numpad[1]": 1073741913, 
        "numpad[2]": 1073741914, 
        "numpad[3]": 1073741915, 
        "numpad[return]": 1073741912, 
        "numpad[0]": 1073741922, 
        "numpad[.]": 1073741923,
        27:"esc",
        1073741882:"f1",
        1073741883:"f2",
        1073741884:"f3",
        1073741885:"f4",
        1073742085:"f5",
        1073742084:"f6",
        1073742083:"f7",
        1073742082:"f8",
        1073742086:"f9",
        1073741953:"f10",
        1073741952:"f11",
        1073742051:"f12",
        96:"~",
        49:"1",
        50:"2",
        51:"3",
        52:"4",
        53:"5",
        54:"6",
        55:"7",
        56:"8",
        57:"9",
        48:"0",
        45:"-",
        61:"=",
        8:"backspace",
        9:"tab",
        113:"q",
        119:"w",
        101:"e",
        114:"r",
        116:"t",
        121:"y",
        117:"u",
        105:"i",
        111:"o",
        112:"p",
        91:"[",
        93:"]",
        92:"\\",
        1073741881:"caps",
        97:"a",
        115:"s",
        100:"d",
        102:"f",
        103:"g",
        104:"h",
        106:"j",
        107:"k",
        108:"l",
        59:";",
        39:"'",
        13:"return",
        1073742049:"lshift",
        122:"z",
        120:"x",
        99:"c",
        118:"v",
        98:"b",
        110:"n",
        109:"m",
        44:",",
        46:".",
        47:"/",
        1073742053:"rshift",
        1073742048:"lctrl",
        1073742050:"lalt",
        32:"space",
        1073742054:"ralt",
        1073742052:"rctrl",
        1073741906:"up",
        1073741905:"down",
        1073741904:"left",
        1073741903:"right",
        1073741907:"numpad[lock]",
        1073741908:"numpad[/]",
        1073741909:"numpad[*]",
        1073741910:"numpad[-]",
        1073741919:"numpad[7]",
        1073741920:"numpad[8]",
        1073741921:"numpad[9]",
        1073741911:"numpad[+]",
        1073741916:"numpad[4]",
        1073741917:"numpad[5]",
        1073741918:"numpad[6]",
        1073741913:"numpad[1]",
        1073741914:"numpad[2]",
        1073741915:"numpad[3]",
        1073741912:"numpad[return]",
        1073741922:"numpad[0]",
        1073741923:"numpad[.]"
    }
