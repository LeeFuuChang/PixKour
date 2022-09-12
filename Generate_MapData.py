from PIL import Image
import json
import os

Elements = {
    ( 14, 209,  69):"Block",
    (236,  28,  36):"Spik1",
    (255, 127,  39):"Spik2",
    (255, 242,   0):"Spik3",
    (184,  61, 186):"Spik4",
    (140, 255, 251):"JumpS",
    ( 14, 209,  22):"Spawn",
}

image = Image.open(os.path.join("assets", "Map-design", "PLATEAU.png")).convert("RGB")


row_start = 0
col_start = 0


MapData = {}


for Rrow in range(4):
    for Ccol in range(4):
        
        if not image.getpixel((col_start, row_start)) == (0, 0, 0):
            input("Waiting. . . "+"{:0>2}{:0>2}".format(Ccol, Rrow))
            Map = []
            for row in range(0, 30):
                Map.append([])
                for col in range(0, 40):
                    Map[row].append(Elements.get(image.getpixel((col_start+col, row_start+row)), "Empty"))


            os.system("cls")
            with open("SavedMap.txt", "w") as mf:
                mf.write("[\n")
                for idx, _ in enumerate(Map):
                    mf.write("[")
                    for _z in range(len(_)):
                        if _z == len(_)-1:
                            mf.write(f"\"{_[_z]}\"")
                        else:
                            mf.write(f"\"{_[_z]}\",")
                    if idx == len(Map)-1:
                        mf.write("]\n")
                    else:
                        mf.write("],\n")
                    print(*_)
                mf.write("]")


        col_start += 41
    col_start = 0
    row_start += 31


