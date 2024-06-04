import pygame as pg
import sys
import random

# Constants
WIDTH = 600  # Width of the window
HEIGHT = 600 # Height of the window

SIZE = (WIDTH, HEIGHT) # Size of the window

# Frames Per Second (FPS)
FPS = 60

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GREY = (142, 142, 142)

obstacles = []

class Game():
    def __init__(self):
        global obstacles
        pg.init()
        self.surface = pg.display.set_mode(SIZE)
        self.clock = pg.time.Clock()
        self.running = True
        self.player = Player(self.surface)  # Initialize player here
        

        for i in range(3):
            self.obstacle = Obstacle(self.surface)
            obstacles.append(self.obstacle)
    
    def update(self):
        self.clock.tick(FPS)
        for event in pg.event.get():
            # Check if we want to close the window
            if event.type == pg.QUIT:
                self.running = False  # End the game
        
        self.surface.fill(BLACK)
        for obstacle in obstacles:
            obstacle.update()
            obstacle.draw()
            
        self.player.update()
        self.player.draw()
        pg.display.flip()  # Update the display

class Object():
    def __init__(self, surface):
        self.width = 20
        self.height = 20
        self.surface = surface
        self.x = 0
        self.y = 0
        self.color = WHITE
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self):
        pg.draw.rect(self.surface, self.color, [self.x, self.y, self.width, self.height])

class Player(Object):
    def __init__(self, surface):
        super().__init__(surface)
        self.color = GREEN
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT // 2 - self.height // 2
        self.speed = 2
        self.lastpressed = ""
        self.update_rect()
    
    def update_rect(self):
        self.rect.topleft = (self.x, self.y)

    def update(self):
        keys = pg.key.get_pressed()
        
        if keys[pg.K_LEFT]:
            self.x -= self.speed
            self.lastpressed = "l"
        elif keys[pg.K_RIGHT]:
            self.x += self.speed
            self.lastpressed = "r"
        elif keys[pg.K_UP]:
            self.y -= self.speed
            self.lastpressed = "u"
        elif keys[pg.K_DOWN]:
            self.y += self.speed
            self.lastpressed = "d"
            
        elif self.lastpressed == "l":
            self.x -= self.speed
        elif self.lastpressed == "r":
            self.x += self.speed
        elif self.lastpressed == "u":
            self.y -= self.speed
        elif self.lastpressed == "d":
            self.y += self.speed
        
        if self.x + self.width >= WIDTH or self.x <= 0:
            game.running = False
        if self.y + self.height >= HEIGHT or self.y <= 0:
            game.running = False

        self.update_rect()
    
    def draw(self):
        pg.draw.rect(self.surface, self.color, [self.x, self.y, self.width, self.height])

class Obstacle(Object):
    def __init__(self, surface):
        super().__init__(surface)
        self.color = YELLOW
        self.x = random.randint(0, WIDTH - self.width)
        self.y = random.randint(0, HEIGHT - self.height)
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.eaten = False
        self.cooldown = False
        self.collide = True
        self.place_obstacle()

    def place_obstacle(self):
        global obstacles
        while self.collide:
            self.collide = False
            if len(obstacles) > 0:
                for obstacle in obstacles:
                    if self.rect.colliderect(obstacle.rect):
                        self.collide = True
                        self.x = random.randint(0, WIDTH - self.width)
                        self.y = random.randint(0, HEIGHT - self.height)
                        self.rect.topleft = (self.x, self.y)
        
    def update(self):
        global obstacles
        
        if self.rect.colliderect(game.player.rect):
            if not self.eaten:
                self.eaten = True
                self.color = GREY
                self.cooldown = True
                new_obstacle = Obstacle(self.surface)
                obstacles.append(new_obstacle)
        else:
            if self.cooldown:
                self.cooldown = False
        
        if self.eaten and not self.cooldown:
            if self.rect.colliderect(game.player.rect):
                game.running = False

        # Update the rect to the new position
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        pg.draw.rect(self.surface, self.color, [self.x, self.y, self.width, self.height])

game = Game()

while game.running:
    game.update()
pg.quit()

