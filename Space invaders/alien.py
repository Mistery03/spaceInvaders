import pygame
import os

class Alien(pygame.sprite.Sprite):
    def __init__(self,colour,x,y):
        super().__init__();
        filePath = './graphics/'+ colour + '.png';
        self.image = pygame.image.load(filePath).convert_alpha();
        self.rect = self.image.get_rect(topleft = (x,y))

        if colour == 'red':
            self.value = 100;
        elif colour == 'green':
            self.value = 200;
        else:
            self.value = 300;

    def update(self,direction):
        self.rect.x += direction;

class Extra(pygame.sprite.Sprite):
    def __init__(self,side,WIDTH):
        super().__init__();
        self.image = pygame.image.load(os.path.join("graphics","extra.png")).convert_alpha();

        if side == 'right':
            x = WIDTH + 50;
            self.speed = -3;
        else:
            x = -50;
            self.speed = 3;

        self.rect = self.image.get_rect(topleft = (x,80));

    def update(self):
        self.rect.x += self.speed;