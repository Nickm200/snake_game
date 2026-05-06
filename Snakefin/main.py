import pygame
from sys import exit
from settings import *
from snake import Snake
from apple import Apple
from menu import GameOptions, MainMenu, OptionsMenu

def resource_path(relative_path):
    import os
    import sys

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

class Main:

    def play_menu_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(resource_path("assets/menusong.mp3"))
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

    def play_game_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(resource_path("assets/noel.mp3"))
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.play_menu_music()

        self.eat_sound = pygame.mixer.Sound(resource_path("assets/eat.mp3"))
        self.eat_sound.set_volume(0.7)
        pygame.display.set_caption("Double Headed Snake")
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.bg_rects = [
            pygame.Rect(
                (col + int(row % 2 == 0)) * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            for col in range(0, COLS, 2)
            for row in range(ROWS)
        ]

        self.options = GameOptions()
        self.high_score = 0
        self.state = "menu"

        self.main_menu = MainMenu(self.display_surface, self.options, self.high_score)
        self.options_menu = OptionsMenu(self.display_surface, self.options)

        self.snake = None
        self.apple = None
        self.score = 0

        self.update_event = pygame.event.custom_type()
        self.set_speed_timer()



    

    def set_speed_timer(self):
        speed_name = GameOptions.SPEEDS[self.options.speed]

        if speed_name == "Slow":
            delay = 260
        elif speed_name == "Fast":
            delay = 120
        else:
            delay = 200

        pygame.time.set_timer(self.update_event, delay)

    def start_game(self):
        self.play_game_music()

        double_headed = GameOptions.GAME_MODES[self.options.game_mode] == "Two Headed"
        self.snake = Snake(double_headed=double_headed)
        self.apple = Apple(self.snake)
        self.score = 0
        self.set_speed_timer()
        self.state = "game"

    def draw_bg(self):
        self.display_surface.fill(LIGHT_GREEN)
        for rect in self.bg_rects:
            pygame.draw.rect(self.display_surface, DARK_GREEN, rect)

    def input(self):
        keys = pygame.key.get_pressed()
        new_direction = None

        if keys[pygame.K_RIGHT]:
            new_direction = pygame.Vector2(1, 0)
        elif keys[pygame.K_LEFT]:
            new_direction = pygame.Vector2(-1, 0)
        elif keys[pygame.K_UP]:
            new_direction = pygame.Vector2(0, -1)
        elif keys[pygame.K_DOWN]:
            new_direction = pygame.Vector2(0, 1)

        if new_direction is None:
            return

        # Prevent reversing directly into the active head's neck.
        head = self.snake.get_head()

        if len(self.snake.body) > 1:
            neck = self.snake.body[-2] if self.snake.flipped else self.snake.body[1]
            forbidden_direction = neck - head

            if new_direction == forbidden_direction:
                return

        self.snake.direction = new_direction

    def check_apple_collision(self):
        if self.snake.get_head() == self.apple.pos and not self.snake.has_eaten:
            self.eat_sound.play()
            self.snake.has_eaten = True
            self.score += 1

            if self.score > self.high_score:
                self.high_score = self.score
                self.main_menu.high_score = self.high_score

            self.apple.set_pos()

    def check_game_over(self):
        head = self.snake.get_head()

        # wall collision
        if head.x < 0 or head.x >= COLS or head.y < 0 or head.y >= ROWS:
            pygame.mixer.music.stop()
            self.play_menu_music()
            self.state = "menu"
            return

        # self collision
        if head in self.snake.get_body_without_head():
            self.state = "menu"
            return

    def draw_score(self):
        font = pygame.font.SysFont("comicsansms", 28)
        text = font.render(f"Score: {self.score}", True, "white")
        self.display_surface.blit(text, (20, 20))

    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.state == "menu":
                    action = self.main_menu.handle_event(event)
                    if action == "play":
                        self.start_game()
                    elif action == "options":
                        self.state = "options"
                    elif action == "quit":
                        pygame.quit()
                        exit()

                elif self.state == "options":
                    action = self.options_menu.handle_event(event)
                    if action == "back":
                        self.state = "menu"

                elif self.state == "game":
                    if event.type == self.update_event:
                        self.snake.update()
                        self.check_game_over()
                        if self.state == "game":
                            self.check_apple_collision()

            if self.state == "game":
                self.input()

            self.draw_bg()

            if self.state == "menu":
                self.main_menu.draw()
            elif self.state == "options":
                self.options_menu.draw()
            elif self.state == "game":
                self.snake.draw()
                self.apple.draw()
                self.draw_score()

            pygame.display.update()
            clock.tick(60)


if __name__ == "__main__":
    main = Main()
    main.run()
