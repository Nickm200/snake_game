
from biome import Biome
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
        #self.apple = Apple(self.snake)

        self.biome = Biome()
        self.apple = Apple(self.snake, self.biome)

             
        #game timer
        self.update_event = pygame.event.custom_type()
        pygame.time.set_timer(self.update_event, 200)
        self.game_active = False

         # score tracking
        self.score = 0
        self.high_score = 0
        self.score_font = pygame.font.SysFont("comicsansms", 24, bold = True)


        
        # menu setup
        self.options = GameOptions()

        self.main_menu = MainMenu(self.display_surface, self.options, self.high_score)
        self.options_menu = OptionsMenu(self.display_surface, self.options)
        self.state = "menu"





        # for biome feature
        #self.biome = Biome()





    def draw_bg(self):

        for rect in self.bg_rects:
            #pygame.draw.rect(self.display_surface, DARK_GREEN, rect)

            #for biome changed
            pygame.draw.rect(self.display_surface, self.biome.dark, rect)



    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            if self.snake.direction.x == -1 and self.snake.two_headed:
                self.snake.flipped = not self.snake.flipped  # reversing, swap head
            if self.snake.direction.x != -1 or self.snake.two_headed:
                self.snake.direction = pygame.Vector2(1, 0)

        if keys[pygame.K_LEFT]:
            if self.snake.direction.x == 1 and self.snake.two_headed:
                self.snake.flipped = not self.snake.flipped  # reversing, swap head
            if self.snake.direction.x != 1 or self.snake.two_headed:
                self.snake.direction = pygame.Vector2(-1, 0)

        if keys[pygame.K_UP]:
            if self.snake.direction.y == 1 and self.snake.two_headed:
                self.snake.flipped = not self.snake.flipped  # reversing, swap head
            if self.snake.direction.y != 1 or self.snake.two_headed:
                self.snake.direction = pygame.Vector2(0, -1)

        if keys[pygame.K_DOWN]:
            if self.snake.direction.y == -1 and self.snake.two_headed:
                self.snake.flipped = not self.snake.flipped  # reversing, swap head
            if self.snake.direction.y != -1 or self.snake.two_headed:
                self.snake.direction = pygame.Vector2(0, 1)

   
    def colliion(self):
    # active head depends on flipped state
        head1 = self.snake.body[0] if not self.snake.flipped else self.snake.body[-1]
        head2 = self.snake.body[-1] if self.snake.two_headed and not self.snake.flipped else None

        for head in ([head1, head2] if head2 else [head1]):
            if head == self.apple.pos:
                self.snake.has_eaten = True
                self.apple.set_pos()
                self.score += 1
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.main_menu.high_score = self.high_score

        inner_body = self.snake.body[1:-1] if self.snake.two_headed else self.snake.body[1:]
        heads = [head1] + ([head2] if head2 else [])

        for head in heads:
            if head in inner_body or \
            not 0 <= head.x < COLS or \
            not 0 <= head.y < ROWS:
                self.snake.reset()
                self.score = 0
                self.game_active = False
                self.state = "menu"
                return

        if self.snake.two_headed and self.snake.body[0] == self.snake.body[-1]:
            self.snake.reset()
            self.score = 0
            self.game_active = False
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

                        self.score = 0

                        self.snake.two_headed = (self.options.game_mode == 1)  # set mode from options before reset
                        self.snake.reset()                                      # reset after setting mode so head2 initializes correctly


                        #randomize the biome 
                        if self.options.random_biome:
                            self.biome.randomize()
                            self.apple.update_image(True)
                        else:
                            self.apple.update_image(False)


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

            if self.state == "game":
                if self.game_active:
                    self.input()
                self.colliion()


            #draw
            self.display_surface.fill(self.biome.light)
            self.draw_bg()
            #
            

            if self.state == "game":
                self.snake.draw()
                self.apple.draw()

                # draw score
                score_surf = self.score_font.render(f"Score: {self.score}", True, (255, 255, 255))
                score_shadow = self.score_font.render(f"Score: {self.score}", True, (0, 0, 0))
                self.display_surface.blit(score_shadow, (12, 12))
                self.display_surface.blit(score_surf, (10, 10))

                #added for biome
                if self.options.random_biome:
                    self.biome.draw_label(self.display_surface)


            elif self.state == "menu":
                self.main_menu.draw()
            elif self.state == "options":
                self.options_menu.draw()

            pygame.display.update()
main = Main()
main.run()


