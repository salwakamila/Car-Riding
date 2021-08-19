import random
from time import sleep

import pygame
from pathlib2 import Path


class CarRiding:
    def __init__(self):

        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        self.root_path = str(Path(__file__).parent)

        self.initialize()

    def initialize(self):

        self.crashed = False
        
        # car
        self.carImg = pygame.image.load(self.root_path + "/asset/car.png")
        self.car_x_coordinate = (self.display_width * 0.41)
        self.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 45

        # stone
        self.stone = pygame.image.load(self.root_path + "/asset/stone.png")
        self.stone_startx = random.choice([320,410])
        self.stone_starty = -600
        self.stone_speed = 3
        self.stone_width = 75
        self.stone_height = 75

        # Background
        self.bgImg = pygame.image.load(self.root_path + "/asset/back_ground.jpg")
        self.bg_x1 = (self.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 1
        self.count = 0
        
        # Sound
        self.sound = pygame.mixer.Sound(self.root_path + "/asset/music.mp3")

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Riding -- Group E')
        self.run_car()

    def run_car(self):

        while not self.crashed:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.car_x_coordinate -= 100
                        print("CAR X COORDINATES: %s" % self.car_x_coordinate)
                    if event.key == pygame.K_RIGHT:
                        self.car_x_coordinate += 100
                        print("CAR X COORDINATES: %s" % self.car_x_coordinate)
                    print ("x: {x}, y: {y}".format(x=self.car_x_coordinate, y=self.car_y_coordinate))

            self.gameDisplay.fill(self.black)
            self.back_ground_road()
            self.sound.play()

            self.run_stone(self.stone_startx, self.stone_starty)
            self.stone_starty += self.stone_speed

            if self.stone_starty > self.display_height:
                self.stone_starty = 0 - self.stone_height
                self.stone_startx = random.choice([320,410])

            self.car(self.car_x_coordinate, self.car_y_coordinate)
            self.highscore(self.count)
            self.count += 1
            
            if self.count % 100 == 0:
                self.stone_speed += 0.5
                self.bg_speed += 0.5

            # crash logic
            if self.car_y_coordinate < self.stone_starty + self.stone_height:
                if self.car_x_coordinate > self.stone_startx and self.car_x_coordinate < self.stone_startx + self.stone_width or self.car_x_coordinate + self.car_width > self.stone_startx and self.car_x_coordinate + self.car_width < self.stone_startx + self.stone_width:
                    self.crashed = True
                    self.display_message("Game Over!")

            if self.car_x_coordinate < 300 or self.car_x_coordinate > 450:
                self.crashed = True
                self.display_message("Game Over!")

            pygame.display.update()
            self.clock.tick(60)

    def display_message(self, msg):
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, (255, 255, 255))
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
        pygame.display.update()
        self.clock.tick(60)
        sleep(1)
        car_riding.initialize()
        car_riding.racing_window()

    def back_ground_road(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

    def run_stone(self, thingx, thingy):
        self.gameDisplay.blit(self.stone, (thingx, thingy))

    def highscore(self, count):
        font = pygame.font.SysFont("lucidaconsole", 20)
        text = font.render("Score : " + str(count), True, self.white)
        self.gameDisplay.blit(text, (0, 0))

if __name__ == '__main__':
    car_riding = CarRiding()
    car_riding.racing_window()