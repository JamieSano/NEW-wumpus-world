
import pygame as pyG

pyG.font.init()
btn_txt = pyG.font.SysFont('Arial', 25)

class Button:
    def __init__(self, xy, text_input, btn_color, hover_color):
        self.x_pos = xy[0]
        self.y_pos = xy[1]
        self.text_input = text_input
        self.text = btn_txt.render(self.text_input, True, 'black')
        self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.btn_color = btn_color
        self.hover_color = hover_color

    def draw_button(self, screen):
        pyG.draw.rect(screen, self.btn_color, pyG.Rect.inflate(self.rect, 30, 25))
        screen.blit(self.text, self.rect)

    def click_button(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def draw_button_transparent(self, screen):
        shape = pyG.Surface(self.rect.size, pyG.SRCALPHA)
        pyG.draw.rect(shape, self.btn_color, shape.get_rect())
        transparency_element = pyG.Surface(self.rect.size, pyG.SRCALPHA)        
        transparency_element.blit(screen, (0, 0), special_flags=pyG.BLEND_RGBA_MULT)
        screen.blit(self.text, self.rect)
    
    def update_color(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.text = btn_txt.render(self.text_input, True, self.hover_color)
        else:
            self.text = btn_txt.render(self.text_input, True, 'white')