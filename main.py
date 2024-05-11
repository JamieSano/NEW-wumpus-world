import sys, pygame as pyG
import numpy as np
import tkinter as tk
from tkinter import ttk

from button import Button
from visual import Visual
from game import WumpusWorld


space = 85

WHITE = (255, 255, 255)
DARK_RED = (183, 28,28)
GRAY = (66, 66, 66)
BLACK = (33, 33, 33)
DARK_BROWN = (62, 39, 35) 
BROWN = (93, 64, 55) 
TRANSPARENT = (0, 0, 0, 255)

HEIGHT = 550
WIDTH = 780

pyG.init()
screen = pyG.display.set_mode((WIDTH, HEIGHT))
pyG.display.set_caption("Wumpus World AI Solver")

def create_board():
    board = np.zeros((4,4))
    return board

def updated():
    draw = Visual(screen)

    while True:
        MOUSE_POS = pyG.mouse.get_pos()
        btn_reset = Button((380, 480), " Reset ", BLACK, GRAY)
        btn_menu = Button((80, 40), "\u25C4 Home ", GRAY, DARK_RED)

        for button in [btn_reset, btn_menu]:
            button.update_color(MOUSE_POS)
            button.draw_button(screen)

        for event in pyG.event.get():
            if event.type == pyG.QUIT: 
                if confirm_quit():
                    pyG.quit()
                    sys.exit()
        
        if event.type == pyG.MOUSEBUTTONDOWN:
                    
                if btn_reset.click_button(MOUSE_POS):
                    wumpus_world()

                if btn_menu.click_button(MOUSE_POS):
                    main() 

        draw.board()
        pyG.display.flip()

def wumpus_world():
    pyG.event.clear()

    arrows_count = 3
    grabbed = killed = False   

    draw = Visual(screen)
    ww = WumpusWorld()
    ww.prepare_environment()
    
    game_bg = pyG.image.load("Images/game_bg.png")
    screen.blit(game_bg, (0,0)) 
    while True:
        MOUSE_POS = pyG.mouse.get_pos()

        btn_ai = Button((125, 480), "AI Agent", DARK_RED, GRAY)
        btn_reset = Button((380, 480), " Reset ", BLACK, GRAY)
        btn_menu = Button((80, 40), "\u25C4 Home ", GRAY, DARK_RED)
       
        for button in [btn_ai, btn_reset, btn_menu]:
            button.update_color(MOUSE_POS)
            button.draw_button(screen)
            
        draw.make_env(ww.cur_row, ww.cur_col, ww.world)        
        for event in pyG.event.get():
            if event.type == pyG.QUIT: 
                if confirm_quit():
                    pyG.quit()
                    sys.exit()

            if event.type == pyG.MOUSEBUTTONDOWN:
                
                if btn_reset.click_button(MOUSE_POS):
                    wumpus_world()

                if btn_menu.click_button(MOUSE_POS):
                    main()

                if btn_ai.click_button(MOUSE_POS):
                    while True:
                        ww.cur_row, ww.cur_col = ww.agent.get_move(ww.agent.has_gold)
                        ww.agent.direction(ww.cur_row, ww.cur_col)
                        draw.make_env(ww.cur_row, ww.cur_col, ww.world)  
                        ww.move_agent(ww.cur_row, ww.cur_col)
                        ww.path[ww.cur_row][ww.cur_col] = 1     

                        pyG.time.delay(500)
                        draw.agent(ww.cur_row, ww.cur_col, ww.agent.facing)  
                        draw.score(f"{ww.agent.score}", BLACK)
                        for row in range(4):
                            for col in range(4):
                                if ww.path[row][col]:
                                    draw.make_env(row, col, ww.world)
                                draw.agent(ww.cur_row, ww.cur_col, ww.agent.facing)  
                        
                        agent_status = ww.game_status()
                        if agent_status == -1:
                            draw.status("THE GAME IS ON!", WHITE)            
                        elif agent_status == 0 and not grabbed:
                            draw.status(" WOAH GOLD! Money~", WHITE)                  
                            ww.world = ww.agent.grab(ww.cur_row, ww.cur_col, ww.world)
                            draw.agent(ww.cur_row, ww.cur_col, ww.agent.facing)   
                            ww.g_w_p_coords[0] = None
                            pyG.display.update()
                            grabbed = True
                        elif agent_status == 1:
                            draw.status(" Game over! DELICIOUS DINNER!", WHITE) 
                            draw.environment(ww.world)
                            updated()
                        elif 2 <= agent_status < 5:
                            draw.status(" Game over! How dark a pit looks like.", WHITE) 
                            draw.environment(ww.world)
                            updated()
                        elif agent_status == 9 and grabbed:
                            if ww.agent.location == (0, 0):
                                draw.status(" AGENT WON! HE  SURVIVED.", WHITE) 
                                draw.environment(ww.world)
                                draw.agent(ww.cur_row, ww.cur_col, 'V')  
                                updated()
                        elif agent_status == 10:
                            if arrows_count != 0:
                                draw.make_env(ww.agent.w_pos[0], ww.agent.w_pos[1], ww.world)  
                                draw.arrows(ww.agent.facing, ww.agent.location)
                                ww.agent.score -= 10

                                if ww.is_wumpus_killed(ww.agent.facing):
                                    ww.g_w_p_coords[1] = None
                                    draw.status(" ACKKK! You killed Wumpus.", WHITE)  
                                    ww.agent.score += 2000
                                else:
                                    draw.status("OH NO! WHAT A BAD ARCHER.", DARK_BROWN)  
                                arrows_count -= 1

                            ww.agent.w_found = False
                            pyG.display.update()

                        else:
                            pass      

                        pyG.display.update()
                            
        draw.score(f"{ww.agent.score}", BROWN)
        draw.status("Let AI play!", WHITE)    
        draw.agent(ww.cur_row, ww.cur_col, ww.agent.facing)  
        
        draw.board()
        pyG.display.flip()

def description():
    game_bg = pyG.image.load("Images/direction_bg.png")
    screen.blit(game_bg, (0,0))
    
    while True:
        MOUSE_POS = pyG.mouse.get_pos()

        btn_menu = Button((710, 490), "LEZGO \u25BA", DARK_RED, WHITE)
       
        btn_menu.update_color(MOUSE_POS)
        btn_menu.draw_button_transparent(screen)

        for event in pyG.event.get():
            if event.type == pyG.QUIT: 
                if confirm_quit():
                    pyG.quit()
                    sys.exit()

            if event.type == pyG.MOUSEBUTTONDOWN:

                if btn_menu.click_button(MOUSE_POS):
                    wumpus_world()
        
        pyG.display.flip()

def confirm_quit():
    def center_window(window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


    root = tk.Tk()
    root.withdraw()
    custom_dialog = tk.Toplevel(root, bg="white")
    
    def destroy_dialog():
        custom_dialog.destroy()

    def quit_game():
        custom_dialog.destroy()
        pyG.quit()
        sys.exit()
        

    custom_dialog.title("Quit")

    custom_style = ttk.Style()
    custom_style.configure("Custom.TButton", borderwidth=0, relief="solid", border_radius=5, background="white")

    message_label = tk.Label(custom_dialog, text="Getting out of the cave? Bye then!", bg="white")
    message_label.pack(padx=40, pady=20)

    no_button = ttk.Button(custom_dialog, text="No", style="Custom.TButton", command=destroy_dialog)
    no_button.pack(side="right", padx=(5, 25), pady=15)
    yes_button = ttk.Button(custom_dialog, text="Yes", style="Custom.TButton", command=quit_game)
    yes_button.pack(side="right", padx=(25, 5), pady=15)

    center_window(custom_dialog)
    root.wait_window(custom_dialog)
    return 


def main():
    menu_bg = pyG.image.load("Images/start_bg.png")
    screen.blit(menu_bg, (0,0))

    while True:
        MOUSE_POS = pyG.mouse.get_pos()

        start = Button((370, 480), "Start Game", DARK_RED, WHITE)
        
       
        for button in [start]:
            button.update_color(MOUSE_POS)
            start.draw_button(screen)

        for event in pyG.event.get():
            if event.type == pyG.QUIT: 
                if confirm_quit():
                    pyG.quit()
                    sys.exit()

            if event.type == pyG.MOUSEBUTTONDOWN:
                if start.click_button(MOUSE_POS):
                    description()

        pyG.display.flip()


if __name__ == "__main__":
    main()