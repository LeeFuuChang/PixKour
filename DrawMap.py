from queue import PriorityQueue
import pygame
import os


WIDTH = 960
HEIGHT = 720
B_WIDTH = 24
B_HEIGHT = 24
COLS = WIDTH//B_WIDTH
ROWS = HEIGHT//B_HEIGHT
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draw Map")


WHITE = (255, 255, 255)
Spawn_Color = (0, 0, 255)
Block_Color = (0, 255, 0)
Spik1_Color = (255, 0, 0)
Spik2_Color = (255, 127, 39)
Spik3_Color = (255, 202, 24)
Spik4_Color = (184, 61, 186)

class Point:
    def __init__(self, row, col, width, height, color=WHITE):
        self.row = row
        self.col = col
        self.x = col*width
        self.y = row*height
        self.color = color
        self.width = width
        self.height = height
        
    def get_pos(self):
        return self.row, self.col

    def reset(self):
        self.color = WHITE
        return "Empty"

    def make_Block(self):
        self.color = Block_Color
        return "Block"

    def make_Spik1(self):
        self.color = Spik1_Color
        return "Spik1"

    def make_Spik2(self):
        self.color = Spik2_Color
        return "Spik2"

    def make_Spik3(self):
        self.color = Spik3_Color
        return "Spik3"
        
    def make_Spik4(self):
        self.color = Spik4_Color
        return "Spik4"

    def make_Spawn(self):
        self.color = Spawn_Color
        return "Spawn"

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))




def make_grid(rows, cols, width, height):
    grid = []
    endMap = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            point = Point(i, j, width, height)
            grid[i].append(point)
    for i in range(rows):
        endMap.append([])
        for j in range(cols):
            endMap[i].append("Empty")
    return grid, endMap


def draw(window, grid):
    window.fill(WHITE)

    for row in grid:
        for point in row:
            point.draw(window)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(window, width):
    grid, EndMap = make_grid(rows=ROWS, cols=COLS, width=B_WIDTH, height=B_HEIGHT)
    os.system("cls")
    for _ in EndMap:
        print(*_)

    run = True

    while(run):
        draw(window, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                point = grid[(y//B_HEIGHT)][(x//B_WIDTH)]

                EndMap[(y//B_HEIGHT)][(x//B_WIDTH)] = point.make_Block()

            elif pygame.mouse.get_pressed()[2]:
                x, y = pygame.mouse.get_pos()
                point = grid[(y//B_HEIGHT)][(x//B_WIDTH)]

                EndMap[(y//B_HEIGHT)][(x//B_WIDTH)] = point.reset()



            if event.type == pygame.KEYDOWN:
                x, y = pygame.mouse.get_pos()
                point = grid[(y//B_HEIGHT)][(x//B_WIDTH)]
                if event.key == pygame.K_r:
                    for i in range(ROWS):
                        for j in range(COLS):
                            point = grid[i][j]
                            EndMap[i][j] = point.reset()


                elif event.key == pygame.K_1:
                    EndMap[(y//B_HEIGHT)][(x//B_WIDTH)] = point.make_Spik1()
                elif event.key == pygame.K_2:
                    EndMap[(y//B_HEIGHT)][(x//B_WIDTH)] = point.make_Spik2()
                elif event.key == pygame.K_3:
                    EndMap[(y//B_HEIGHT)][(x//B_WIDTH)] = point.make_Spik3()
                elif event.key == pygame.K_4:
                    EndMap[(y//B_HEIGHT)][(x//B_WIDTH)] = point.make_Spik4()
                elif event.key == pygame.K_5:
                    EndMap[(y//B_HEIGHT)][(x//B_WIDTH)] = point.make_Spawn()
                elif event.key == pygame.K_6:
                    EndMap[(y//B_HEIGHT)][(x//B_WIDTH)] = point.make_Boss_Portal()
                elif event.key == pygame.K_7:
                    EndMap[(y//B_HEIGHT)][(x//B_WIDTH)] = point.make_Shop_Portal()


                elif event.key == pygame.K_RETURN:
                    os.system("cls")
                    with open("SavedMap.txt", "w") as mf:
                        mf.write("[\n")
                        for _ in EndMap:
                            mf.write("[")
                            for _z in range(len(_)):
                                if _z == len(_)-1:
                                    mf.write(f"\"{_[_z]}\"")
                                else:
                                    mf.write(f"\"{_[_z]}\",")
                            mf.write("],\n")
                            print(*_)
                        mf.write("]")
    
    pygame.quit()


if __name__ == "__main__":
    main(SCREEN, WIDTH)