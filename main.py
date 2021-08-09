import pygame
import sys
import os
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser

class Game:
    def __init__(self):
        playerSprite = Player((WIDTH/2,HEIGHT),WIDTH,5);
        self.player = pygame.sprite.GroupSingle(playerSprite);

        #health and score setup
        self.lives = 3;
        self.liveSurf = pygame.image.load(os.path.join("graphics","player.png")).convert_alpha();
        self.live_x_start_pos = WIDTH - (self.liveSurf.get_size()[0] * 2 + 20);
        self.score = 0;
        self.font = pygame.font.Font('font/Pixeled.ttf',20);

        #obstacle setup
        self.shape = obstacle.shape;
        self.blockSize = 6;
        self.blocks = pygame.sprite.Group();
        self.obstacleAmount = 4;
        self.obstacle_x_pos = [num * (WIDTH/self.obstacleAmount) for num in range(self.obstacleAmount)];
        self.createMultipleObstacles(*self.obstacle_x_pos, x_start= WIDTH/15, y_start=480);

        #Alien setup
        self.aliens = pygame.sprite.Group();
        self.alienSetup(rows = 6, cols = 8);
        self.alienDirection = 1;
        self.alienLasers = pygame.sprite.Group();

        #Extra setup
        self.extra = pygame.sprite.GroupSingle();
        self.extraSpawnTime = randint(40,80);

        #Audio
        music = pygame.mixer.Sound(os.path.join("audio","music.wav"));
        music.set_volume(0.2);
        music.play(loops = -1);
        self.laserSound = pygame.mixer.Sound(os.path.join("audio","laser.wav"));
        self.laserSound.set_volume(0.5);
        self.explosionSound = pygame.mixer.Sound(os.path.join("audio", "explosion.wav"));
        self.explosionSound.set_volume(0.3);

    def victoryMessage(self):
        if not self.aliens.sprites():
            victorySurf = self.font.render("YOU WON", False,"white");
            victoryRect = victorySurf.get_rect(center = (WIDTH/2,HEIGHT/2));
            screen.blit(victorySurf,victoryRect);

    def displayScore(self):
        scoreSurf = self.font.render(f"score: {self.score}",False,"white");
        scoreRect = scoreSurf.get_rect(topleft = (10,-10));
        screen.blit(scoreSurf,scoreRect);

    def displayLives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.liveSurf.get_size()[0] + 10));
            screen.blit(self.liveSurf,(x,8));

    def collisionCheck(self):
        #player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                #obstacle collisions
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill();

                #alien collisions
                aliensHit = pygame.sprite.spritecollide(laser,self.aliens,True);
                if aliensHit:
                    for alien in aliensHit:
                        self.score += alien.value;
                    laser.kill();
                    self.explosionSound.play();

                #extra collisions
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 500;
                    laser.kill();

        #alien lasers
        if self.alienLasers:
            for laser in self.alienLasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill();

                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill();
                    self.lives -= 1;
                    if self.lives <= 0:
                        pygame.quit();
                        exit();

        #aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True);

                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit();
                    exit();

    def extraAlienTimer(self):
        self.extraSpawnTime -= 1;
        if self.extraSpawnTime <= 0:
            self.extra.add(Extra(choice(['right','left']),WIDTH));
            self.extraSpawnTime = randint(400,800);

    def alienShoot(self):
        if self.aliens.sprites():
            randomAlien = choice(self.aliens.sprites());
            laserSprite = Laser(randomAlien.rect.center,6,HEIGHT);
            self.alienLasers.add(laserSprite);
            self.laserSound.play();

    def alienMoveDown(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance;

    def alienPosChecker(self):
        allAlien = self.aliens.sprites();
        for alien in allAlien:
            if alien.rect.right >= WIDTH:
                self.alienDirection = -1;
                self.alienMoveDown(2);
            elif alien.rect.left <= 0:
                self.alienDirection = 1;
                self.alienMoveDown(2);

    def alienSetup(self,rows,cols,x_dist = 60,y_dist = 48,x_offset = 70,y_offtset =100):
        for rowIndex, row in enumerate(range(rows)):
            for colIndex, col in enumerate(range(cols)):
                x = colIndex * x_dist + x_offset;
                y = rowIndex * y_dist + y_offtset;

                if rowIndex == 0:
                    alienSprite = Alien("yellow",x,y);
                elif 1 <= rowIndex <= 2:
                    alienSprite = Alien("green",x,y);
                else:
                    alienSprite = Alien("red",x,y);
                self.aliens.add(alienSprite);

    def createObstacle(self,x_start,y_start,offset_x):
        for rowIndex, row in enumerate(self.shape):
            for colIndex, col in enumerate(row):
                if col == 'x':
                    x = x_start + colIndex *self.blockSize + offset_x;
                    y = y_start + rowIndex * self.blockSize;
                    block = obstacle.Block(self.blockSize,(241,79,80),x,y);
                    self.blocks.add(block);

    def createMultipleObstacles(self,*offset,x_start,y_start):
        for offset_x in offset:
            self.createObstacle(x_start,y_start,offset_x);

    def run(self):
        self.player.update();
        self.aliens.update(self.alienDirection);
        self.alienLasers.update();
        self.extra.update();
        self.extraAlienTimer();
        self.alienPosChecker();
        self.collisionCheck();


        self.player.sprite.lasers.draw(screen);
        self.player.draw(screen);
        self.blocks.draw(screen);
        self.aliens.draw(screen);
        self.alienLasers.draw(screen);
        self.extra.draw(screen);

        self.displayLives();
        self.displayScore();
        self.victoryMessage();

class CRT:
    def __init__(self):
        self.tv = pygame.image.load(os.path.join("graphics","tv.png")).convert_alpha();
        self.tv = pygame.transform.scale(self.tv,(WIDTH,HEIGHT));

    def draw(self):
        self.tv.set_alpha(randint(75,90));
        self.createCRTLines();
        screen.blit(self.tv,(0,0));

    def createCRTLines(self):
        lineHeight = 3;
        lineAmount = int(HEIGHT/lineHeight);
        for line in range(lineAmount):
            y_pos = line*lineHeight;
            pygame.draw.line(self.tv,"black",(0,y_pos),(WIDTH,y_pos),1);

if __name__ == "__main__":
    pygame.init();
    WIDTH, HEIGHT = 600,600;
    pygame.display.set_caption("Space Invader");
    screen = pygame.display.set_mode((WIDTH,HEIGHT));
    clock = pygame.time.Clock();
    FPS = 60;
    game = Game();
    crt = CRT();

    ALIENLASER = pygame.USEREVENT +1;
    pygame.time.set_timer(ALIENLASER,800);

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                quit();
            if event.type == ALIENLASER:
                game.alienShoot();

        screen.fill((30,30,30));
        game.run();
        crt.draw();

        clock.tick(FPS);
        pygame.display.update();