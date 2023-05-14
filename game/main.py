import pygame 
import time
import random

#this import certain variables(locals)
from pygame.locals import *
SIZE = 40 

class Apple: 
    def __init__(self, parent_screen) -> None:
        self.texture = pygame.image.load('resources/apple.png')
        self.block = pygame.transform.scale(self.texture,(SIZE,SIZE))
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3
        
    def draw(self):
        #this "draws" something over the screen (surface) in certain xy coordinates
        self.parent_screen.blit(self.block,(self.x, self.y))
        #this makes it so that you "redraw" the screen every time. If you deleted the first line, you'd get a "trail" of blocks remaining.
        
        
    
    #If you divide the screen size by SIZE, you get a screen area of 25x20 "squares" of 40x40.
    #You want a random number between these ranges, and multiply it by SIZE so that you can assign it a random "SQUARE" to pop in.
    #This assigns new random coordinates to the apple.
    def move(self):
        self.x = random.randint(0,19)*SIZE
        self.y = random.randint(0,14)*SIZE
        #You want to make it so that the apple doesnt appear out of screen. That is why we use 19 and 24.

class Snake:
    def __init__(self, parent_screen, length) -> None:
        #this loads the image 
        self.texture = pygame.image.load("resources/ducc.png")
        #this transforms the size of the image and asigns it to the variable "block"
        self.block = pygame.transform.scale(self.texture,(SIZE,SIZE))
        #this multiplies the array to have n =length elements
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.parent_screen = parent_screen
        self.direction = "down"
        self.length = length
        pass
    def increase_length(self):
        self.length+=1
        #We could append any value as the walk function would set it in the right position (alligned with SIZE)
        self.x.append(-1)
        self.y.append(-1)
    def draw(self):
        
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i], self.y[i]))
        
        #flip basically updates the screen 
        
    
    def walk(self):
        
        #this loop goes in reverse; 5,4,3,2...
        #makes it so that a block takes the position of the block before it
        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]
        
        if self.direction == "up":
            self.y[0]-=SIZE

        if self.direction == "down":
            self.y[0]+=SIZE

        if self.direction == "left":
            self.x[0]-=SIZE

        if self.direction == "right":
            self.x[0]+=SIZE 
        self.draw()
        
    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Danteboe's Apple Eating Duck Game")

        pygame.mixer.init()
        self.play_background_music()
        #this sets the screen size and color
        self.surface = pygame.display.set_mode((800, 600))
        self.render_background()
        
        #This is basically making it so that the game surface is entered as the parameter for snake's "parent screen"
        self.snake = Snake(self.surface,1)
        
        self.apple = Apple(self.surface)
        
    #this basically checks if the position is inside the square of the apple. xy1 and xy+SIZE are the 
    #boundaries of the apple, while xy2 is the position of the snake's head.    
    def collision(self, x1, y1, x2, y2):
        if x1==x2 and y1==y2:
            return True
        return False

    def play_background_music(self):
        #There is a difference between music and sound in pygame. Music repeats itself.
        pygame.mixer.music.load('resources/background_music.mp3')
        pygame.mixer.music.play()

    def play_sound(self, sound_file): 
        sound = pygame.mixer.Sound(sound_file)
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        background= pygame.image.load('resources/background_img.jpg')
        self.surface.blit(background, (-400,-400))
    
    def play(self):
        self.render_background()
        self.apple.draw()
        self.snake.walk()
        self.show_score()
        #flip basically updates the screen every time
        pygame.display.flip()
        
        #SNAKE COLLIDING WITH APPLE
        #if the snake collides with the apple, it teleports to a random place.
        if self.collision(self.apple.x,self.apple.y,self.snake.x[0],self.snake.y[0]):
            self.play_sound('resources/growth.wav')
            self.snake.increase_length()
            self.apple.move()

            
        #SNAKE COLLIDING WITH ITSELF.
        for i in range(1,self.snake.length):
            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('resources/game_over.wav')
                raise "Game Over"
        
        #SNAKE COLLIDING WITH THE WALLS
        if self.snake.x[0]<0 or self.snake.x[0]>800 or self.snake.y[0]<0 or self.snake.y[0]>600:
            self.play_sound('resources/game_over.wav')
            raise "Game Over"
        
    def show_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f'Score: {self.snake.length}', True, (255,255,255))
        self.surface.blit(score, (600,10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f'Oops! You lost. Final score: {self.snake.length}', True, (255,255,255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(f'Press Space to play again.', True, (255,255,255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                #this makes it so that it happens something after a user presses a key
                if event.type == KEYDOWN:
                    
                    #this makes the user exit the game when they press the escape key.
                    if event.key == K_ESCAPE:
                        running == False
                        pygame.quit()
                        
                    if event.key == K_SPACE:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:

                        
                        if event.key == K_w:
                            self.snake.move_up()
                        
                        if event.key == K_s:
                            self.snake.move_down()
                        
                        if event.key == K_a:
                            self.snake.move_left()
                        
                        if event.key == K_d:
                            self.snake.move_right()

                elif event.type == QUIT:
                    pygame.quit()
            try:
                if not pause:
                    self.play()
            except Exception:
                self.show_game_over()
                pause = True
                self.reset()
            #THIS MAKES IT SO THAT THE LOOP HAPPENS EVERY 0.2 SECONDS
            time.sleep(.1)
                

    
    
if __name__ == "__main__":
    
    
    game = Game()
    game.run()

    