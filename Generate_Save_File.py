import time
import json
import os

def Generate_SaveFile():
    with open(os.path.join("Config", "Default_PlayerData.json"), "r") as pd:
        PlayerData = json.load(pd)

    with open(os.path.join("Config", "Default_MapData.json"), "r") as md:
        MapData = json.load(md)

    Current_time = time.strftime("%B")+" "+time.strftime("%d")+", "+time.strftime("%Y")+" "+time.strftime("%I")+":"+time.strftime("%M")+" "+time.strftime("%p")

    SaveData = {
        "Create_Time":Current_time,
        "Last_Save":Current_time,
        "Player":PlayerData,
        "Map":MapData
    }

    i = 1
    while(os.path.exists(os.path.join("Saves", f"Save_File{i}.json"))):
        i+=1

    with open(os.path.join("Saves", f"Save_File{i}.json"), "w") as sf:
        json.dump(SaveData, sf)


if __name__ == "__main__":
    Generate_SaveFile()