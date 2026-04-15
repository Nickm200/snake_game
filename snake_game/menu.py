import pygame
from settings import *
 
 
# helper functions
 
def draw_text(surface, text, font, color, center):
    surf = font.render(text, True, color)
    r = surf.get_rect(center = center)
    surface.blit(surf, r)
 
 

# stores the game options
class GameOptions:
    GAME_MODES = ["Single", "Two Headed"]
    SPEEDS = ["Slow", "Normal", "Fast"]
 
    def __init__(self):
        self.game_mode = 0
        self.speed = 1
 
 
# main menu screen
 

class MainMenu:
 
    BUTTONS = ["Play", "Options", "Exit"]
 
    def __init__(self, display_surface, options, high_score = 0):
        self.surface = display_surface
        self.options = options

        self.high_score = high_score

        self.font_title = pygame.font.SysFont("comicsansms", 68, bold=True)
        self.font_btn = pygame.font.SysFont("comicsansms", 30)

        self.font_score = pygame.font.SysFont("comicsansms", 22)


        self.btn_rects = []
        self.action = None
 
    def handle_event(self, event):
        self.action = None
 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, r in enumerate(self.btn_rects):
                if r.collidepoint(event.pos):
                    self.action = ["play", "options", "quit"][i]
 
        return self.action
 
    def draw(self):
        cx = WINDOW_WIDTH // 2
        cy = WINDOW_HEIGHT // 2
 

        # draw the background panel
        panel_w = 480
        panel_h = 380
        panel_rect = pygame.Rect(0, 0, panel_w, panel_h)
        panel_rect.center = (cx, cy)
        pygame.draw.rect(self.surface, (50, 90, 30), panel_rect, border_radius=4)
 
        # draw the title
        draw_text(self.surface, "MAIN MENU", self.font_title, (255, 255, 255), (cx, panel_rect.top + 68))

        # draw high score
        hs_text = f"High Score: {self.high_score}"
        draw_text(self.surface, hs_text, self.font_score, LIGHT_GREEN, (cx, panel_rect.top + 118))

      

        
       
       
    
 
        # draw buttons

        self.btn_rects = []
        btn_w = 260
        btn_h = 48
        gap = 12
        start_y = panel_rect.top + 142
 
        for i, label in enumerate(self.BUTTONS):
            r = pygame.Rect(0, 0, btn_w, btn_h)
            r.centerx = cx
            r.y = start_y + i * (btn_h + gap)
            self.btn_rects.append(r)
 
            btn_surf = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
            btn_surf.fill((255, 255, 255, 30))
            self.surface.blit(btn_surf, r)

            pygame.draw.rect(self.surface, (255, 255, 255, 120), r, 2, border_radius = 4)

            draw_text(self.surface, label, self.font_btn, (255, 255, 255), r.center)
 
 
# options screen
 
class OptionsMenu:
 
    def __init__(self, display_surface, options):
        self.surface = display_surface
        self.options = options
        self.font_title = pygame.font.SysFont("comicsansms", 56, bold = True)
        self.font_label = pygame.font.SysFont("comicsansms", 24, bold = True)
        self.font_value = pygame.font.SysFont("comicsansms", 24)

        self.action = None
        self.back_rect = None
        self.arrow_rects = {}
 
    def handle_event(self, event):
        self.action = None
 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
 
            # check if back button was clicked
            if self.back_rect and self.back_rect.collidepoint(pos):
                self.action = "back"
                return self.action
 
            # check game mode arrows
            if "mode_left" in self.arrow_rects:
                if self.arrow_rects["mode_left"].collidepoint(pos):
                    self.options.game_mode = (self.options.game_mode - 1) % len(GameOptions.GAME_MODES)

                elif self.arrow_rects["mode_right"].collidepoint(pos):

                    self.options.game_mode = (self.options.game_mode + 1) % len(GameOptions.GAME_MODES)
 

            # check speed arrows

            if "speed_left" in self.arrow_rects:
                if self.arrow_rects["speed_left"].collidepoint(pos):

                    self.options.speed = (self.options.speed - 1) % len(GameOptions.SPEEDS)

                elif self.arrow_rects["speed_right"].collidepoint(pos):

                    self.options.speed = (self.options.speed + 1) % len(GameOptions.SPEEDS)
 
        return self.action
 
    def draw(self):
        cx = WINDOW_WIDTH // 2
        cy = WINDOW_HEIGHT // 2
 
        # draw background panel
        panel_w = 540
        panel_h = 360
        panel_rect = pygame.Rect(0, 0, panel_w, panel_h)
        panel_rect.center = (cx, cy)
        pygame.draw.rect(self.surface, (50, 90, 30), panel_rect, border_radius=4)
 
        # title
        draw_text(self.surface, "OPTIONS", self.font_title, (255, 255, 255), (cx, panel_rect.top + 58))
 
        row_h = 64
        start_y = panel_rect.top + 138
 
        settings = [
            ("Game Mode", GameOptions.GAME_MODES[self.options.game_mode], "mode"),
            ("Speed", GameOptions.SPEEDS[self.options.speed], "speed"),
        ]
 
        self.arrow_rects = {}
 
        for i, (label, value, key) in enumerate(settings):
            row_y = start_y + i * row_h
 
            # draw the label
            lbl_surf = self.font_label.render(label, True, (255, 255, 255))
            self.surface.blit(lbl_surf, (panel_rect.left + 44, row_y))
 
            arr_size = 28
            lx = cx + 20
 
            # left arrow
            arr_left = pygame.Rect(lx, row_y, arr_size, arr_size)
            self.draw_arrow(arr_left, "left")
            self.arrow_rects[key + "_left"] = arr_left
 
            # current value
            val_surf = self.font_value.render(value, True, LIGHT_GREEN)
            val_rect = val_surf.get_rect(midleft=(lx + arr_size + 10, row_y + arr_size // 2))
            self.surface.blit(val_surf, val_rect)
 
            # right arrow
            arr_right = pygame.Rect(val_rect.right + 10, row_y, arr_size, arr_size)
            self.draw_arrow(arr_right, "right")
            self.arrow_rects[key + "_right"] = arr_right
 
        # back button
        back_w = 160
        back_h = 44
        self.back_rect = pygame.Rect(0, 0, back_w, back_h)
        self.back_rect.centerx = cx
        self.back_rect.y = panel_rect.bottom - back_h - 20
        back_surf = pygame.Surface((back_w, back_h), pygame.SRCALPHA)
        back_surf.fill((255, 255, 255, 30))
        self.surface.blit(back_surf, self.back_rect)


        pygame.draw.rect(self.surface, (255, 255, 255, 120), self.back_rect, 2, border_radius=4)
        draw_text(self.surface, "Back", self.font_label, (255, 255, 255), self.back_rect.center)
 
    def draw_arrow(self, rect, direction):
        cx = rect.centerx
        cy = rect.centery
        s = 8
 
        if direction == "left":
            pts = [(cx + s, cy - s), (cx - s, cy), (cx + s, cy + s)]
        else:
            pts = [(cx - s, cy - s), (cx + s, cy), (cx - s, cy + s)]
 
        pygame.draw.polygon(self.surface, (220, 220, 220), pts)
