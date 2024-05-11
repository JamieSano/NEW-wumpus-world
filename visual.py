import pygame as pyG

space = 90
over_x = 70
over_y = 80
WORLD_SIZE = 4

WHITE = (255, 255, 255)
DARK_RED = (183, 28,28)
GRAY = (66, 66, 66)
BLACK = (33, 33, 33)
DARK_BROWN = (62, 39, 35) 
BROWN = (93, 64, 55) 

pyG.font.init()

class Visual:
    def __init__(self, screen):
        self.screen = screen
        self.agent_img = pyG.image.load("Images/player_facing_to_down.png")
        self.agent_side_img = pyG.image.load("Images/player_facing_to_left.png")
        self.agent_victory_img = pyG.image.load("Images/agent_victory_new.png")
        self.arrow_img = pyG.image.load("Images/arrow.png")
        self.arrow_side_img = pyG.image.load("Images/arrow_side-new.png")
        self.breeze_img = pyG.image.load("Images/breeze.png")
        self.breeze_stench_img = pyG.image.load("Images/breeze_stench.png")
        self.gold_img = pyG.image.load("Images/gold.png")
        self.pit_img = pyG.image.load("Images/new_pit.png")
        self.stench_img = pyG.image.load("Images/stench.png")
        self.wumpus_img = pyG.image.load("Images/wumpus.png")

        self.font = pyG.font.SysFont('Arial Black', 20)

    def board(self):
        pyG.draw.rect(self.screen, BROWN, pyG.Rect(over_x, over_y, 360, 360), 7)
        i = 1
        while(i*space)<360:
            line_width = 3
            pyG.draw.line(self.screen, BROWN, (over_x, over_y + i * space), (over_x + 355, over_y + i * space), line_width)
            pyG.draw.line(self.screen, BROWN, (over_x + i * space, over_y), (over_x + i * space, over_y + 355), line_width)
            i+=1

    def agent(self, row, col, direction):
        x = over_x + col * space + 10
        y = over_y + row * space + 20
        
        if direction == 'U':
            y-=10
            self.screen.blit(self.agent_img, (x,y))
        elif direction == 'D':
            self.screen.blit(self.agent_img, (x,y))
        elif direction == 'L':
            self.screen.blit(self.agent_side_img, (x,y))
        elif direction == 'R':
            agent_rightside = pyG.transform.flip(self.agent_side_img, True, False)
            self.screen.blit(agent_rightside, (x, y))
        elif direction == 'V':
            self.screen.blit(self.agent_victory_img, (x-10,y-20))
        
        self.board()
    
    def environment(self, world):
        for row in range(WORLD_SIZE):
            for col in range(WORLD_SIZE):
                self.make_env(row, col, world)

    def make_env(self, row, col, world):
        cell_type = world[row][col]
        x = over_x + col * space
        y = over_y + row * space

        if len(cell_type) > 1 and cell_type[0] == 'A':
            if len(cell_type) == 3 and cell_type[1] == 'B' and cell_type[2] == 'S':
                self.screen.blit(self.breeze_stench_img, (x+10, y+10))
            elif len(cell_type) == 2 and cell_type[1] == 'B':
                self.screen.blit(self.breeze_img, (x+10, y+10))
            elif len(cell_type) == 2 and cell_type[1] == 'S':
                self.screen.blit(self.stench_img, (x+10, y+10))
            elif len(cell_type) == 2 and cell_type[1] == 'G':
                self.screen.blit(self.gold_img, (x+10, y+10))
        if cell_type == '' or cell_type == 'A':
            cell_rect = pyG.Rect(x, y, space, space)
            pyG.draw.rect(self.screen, DARK_RED, cell_rect)
        elif cell_type == 'B':
            self.screen.blit(self.breeze_img, (x+10, y+10))
        elif cell_type == 'BS':
            self.screen.blit(self.breeze_stench_img, (x+10, y+10))
        elif cell_type == 'G' or cell_type == 'BG'  or cell_type == 'GS' or cell_type == 'BGS':
            self.screen.blit(self.gold_img, (x+10, y+10))
        elif cell_type == 'P' or cell_type == 'BP' or cell_type == 'PS' or cell_type == 'BPS':
            self.screen.blit(self.pit_img, (x+5, y+3))
        elif cell_type == 'S':
            self.screen.blit(self.stench_img, (x+10, y+10))
        elif cell_type == 'W' or cell_type == 'BW':
            self.screen.blit(self.wumpus_img, (x+10, y+10))

        self.board()
    
    def arrows(self, direction, pos):
        row, col = pos

        x = over_x + col * space +10
        y = over_y + row * space +10

        if direction == 'U':
            for r in range(row, -1, -1):
                self.screen.blit(self.arrow_img, (x, y))
        elif direction == 'D':
            for r in range(row, 4):
                y = over_y + r * space +10
                arrow_down = pyG.transform.flip(self.arrow_img, False, True)
                self.screen.blit(arrow_down, (x, y))
        elif direction == 'L':
            for c in range(col, -1, -1):
                x = over_x + c * space +10
                self.screen.blit(self.arrow_side_img, (x, y))
        elif direction == 'R':
            for c in range(col, 4):
                arrow_west = pyG.transform.flip(self.arrow_side_img, False, True)
                self.screen.blit(arrow_west, (x, y))

    def status(self, text, color):
        text_bg = pyG.Surface((240, 90))
        text_bg.fill(BLACK)
        bg_rect = text_bg.get_rect(center=(610, 400))
        pyG.draw.rect(self.screen, DARK_RED, pyG.Rect(bg_rect.left-2, bg_rect.top-2, 244, 94), 2)


        if len(text) <= 16:
            output = self.font.render(text, True, color)
            text_rect = output.get_rect(center=bg_rect.center)

            self.screen.blit(text_bg, bg_rect)
            self.screen.blit(output, text_rect)
        else:
            text_line1 = text[:16]
            text_line2 = text[16:]
            output1 = self.font.render(text_line1, True, color)
            output2 = self.font.render(text_line2, True, color)

            text_rect1 = output1.get_rect(center=(bg_rect.centerx, bg_rect.centery - 15))
            text_rect2 = output2.get_rect(center=(bg_rect.centerx, bg_rect.centery + 15))

            self.screen.blit(text_bg, bg_rect)
            self.screen.blit(output1, text_rect1)
            self.screen.blit(output2, text_rect2)

    def score(self, text, color):
        text_bg = pyG.Surface((115, 60))
        text_bg.fill(WHITE)
        bg_rect = text_bg.get_rect(center=((500, 200)))

        output = self.font.render("Score", True, color)
        score = self.font.render(text, True, color)
        text_rect1 = score.get_rect(center=(bg_rect.centerx, bg_rect.centery + 10))
        text_rect2 = output.get_rect(center=(bg_rect.centerx, bg_rect.centery - 10))

        self.screen.blit(text_bg, bg_rect)
        self.screen.blit(score, text_rect1)
        self.screen.blit(output, text_rect2)