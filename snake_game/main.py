import pygame
from settings import *
from snake import Snake
from apple import Apple
from menu import MainMenu, OptionsMenu, GameOptions

class Main:

    def __init__(self):
        #initializes basics of pygame 
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        #game obj
        self.bg_rects = [pygame.Rect((col +int(row % 2 == 0)) * CELL_SIZE ,row * CELL_SIZE,CELL_SIZE, CELL_SIZE)
                        for col in range(0,COLS,2) for row in range(ROWS)]

        self.snake = Snake()
        self.apple = Apple(self.snake)
             
        #game timer
        self.update_event = pygame.event.custom_type()
        pygame.time.set_timer(self.update_event, 200)
        self.game_active = False


        
        # menu setup
        self.options = GameOptions()
        self.main_menu = MainMenu(self.display_surface, self.options)
        self.options_menu = OptionsMenu(self.display_surface, self.options)
        self.state = "menu"





    def draw_bg(self):
        for rect in self.bg_rects:
            pygame.draw.rect(self.display_surface, DARK_GREEN, rect)



    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.snake.direction = pygame.Vector2(1,0) if self.snake.direction.x != -1 else self.snake.direction
        if keys[pygame.K_LEFT]:
            self.snake.direction = pygame.Vector2(-1,0) if self.snake.direction.x != 1 else self.snake.direction
        if keys[pygame.K_UP]:
            self.snake.direction = pygame.Vector2(0,-1) if self.snake.direction.y != 1 else self.snake.direction
        if keys[pygame.K_DOWN]:
            self.snake.direction = pygame.Vector2(0,1) if self.snake.direction.y != -1 else self.snake.direction


    def colliion(self):
        
        if self.snake.body[0] == self.apple.pos:
            self.snake.has_eaten = True
            self.apple.set_pos()

            # game over
        if self.snake.body[0] in self.snake.body[1:] or \
            not 0 <= self.snake.body[0].x < COLS or \
            not 0 <= self.snake.body[0].y < ROWS:
            self.snake.reset()
            self.game_active = False
            
            #menu
            self.state = "menu"
            


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


                # added: menu states
                if self.state == "menu":
                    action = self.main_menu.handle_event(event)
                    if action == "play":
                        self.state = "game"
                        self.game_active = False
                        # speed
                        speeds = [400, 200, 100]  # slow, normal, fast
                        pygame.time.set_timer(self.update_event, speeds[self.options.speed])

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

                    if event.type == self.update_event and self.game_active:
                        self.snake.update()

                    if event.type == pygame.KEYDOWN and not self.game_active:
                        self.game_active = True

            #updates
            self.input()
            self.colliion()


            #draw
            self.display_surface.fill(LIGHT_GREEN)
            self.draw_bg()
            if self.state == "game":
                self.snake.draw()
                self.apple.draw()

            elif self.state == "menu":
                self.main_menu.draw()
            elif self.state == "options":
                self.options_menu.draw()

            pygame.display.update()
main = Main()
main.run()
