from PIL import Image
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

image = Image.open(os.path.join("assets", "Map-design", "Convert_Map.png")).convert("RGB")

Map = []

for row in range(0, 30):
    Map.append([])
    for col in range(0, 40):
        Map[row].append(Elements.get(image.getpixel((col, row)), "Empty"))

with open("SavedMap.txt", "w") as mf:
    mf.write("[\n")
    for _ in Map:
        mf.write("[")
        for _z in range(len(_)):
            if _z == len(_)-1:
                mf.write(f"\"{_[_z]}\"")
            else:
                mf.write(f"\"{_[_z]}\",")
        if _ == Map[-1]:
            mf.write("]\n")
        else:
            mf.write("],\n")
        print(*_)
    mf.write("]")