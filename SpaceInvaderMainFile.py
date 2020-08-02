# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 11:45:23 2020

@author: SpencerAndTheMatt

Space invaders python game, using pygame
This tutorial from freeCodeCamp helped me greatly - https://www.youtube.com/watch?v=FfWpgLFMI7w

Thank you to https://www.remove.bg/upload for removing whitespace from images

Background music from zapsplat.com
Sound effects from soundbible.com
End game music from https://www.fesliyanstudios.com/royalty-free-music/downloads-c/sad-music/1
"""


#Initialising variables/imports

#Define imports
import pygame;
import random;
import math;
from pygame import mixer;

#Define game_over_bool as a list containing False
game_over_bool = [False];

#Initialise pygame
pygame.init();

#Make screen with set_mode((width, height))
screen = pygame.display.set_mode((800, 600));

#Title and icon
pygame.display.set_caption("Space Invaders"); #Title
icon = pygame.image.load('ufo.png'); #Load image, set it to icon
pygame.display.set_icon(icon); #Icon from https://toppng.com/ixel-space-ufo-spaceship-metal-lights-colors-alien-pixel-ufo-PNG-free-PNG-Images_174097?search-result=pixel-sunglass


#Load player image and set co ordinates
playerImg = pygame.image.load('player-no-background.png'); #https://www.pngkey.com/pngs/spaceship/
playerImgResized = pygame.transform.scale(playerImg, (64, 64));
playerX = 370; #X co ordinate
playerY = 480; #Y co ordinate


#Load enemy image
enemyImg = pygame.image.load('enemy-no-background.png'); #https://www.pinclipart.com/pindetail/ihwxmhJ_space-invaders-png-high-quality-image-space-invaders/

#Form enemy lists
enemyImgResized = [];
enemyX = [];
enemyY = [];
enemyX_Change = [];
enemyY_Change = [];
num_of_enemies = 6;

#Fill enemy lists
for i in range(num_of_enemies):
    enemyImgResized.append(pygame.transform.scale(enemyImg, (64, 64)));
    enemyX.append(random.randint(0, 735));
    enemyY.append(random.randint(50, 150));
    enemyX_Change.append(2);
    enemyY_Change.append(40);
    

#Load bullet image and set parameters
bulletImg = pygame.image.load('bullet-no-background.png'); #https://dlpng.com/png/6431381
bulletImgResized = pygame.transform.scale(bulletImg, (32, 64));
bulletX = 0;
bulletY = 480;
bulletX_Change = 0;
bulletY_Change = 10;
bullet_state = "ready"; #state = ready: cannot see bullet on screen. State = fire: bullet in motion.

#Load background image
background = pygame.image.load('background-other.png'); #https://opengameart.org/content/space-backgrounds-9
backgroundResized = pygame.transform.scale(background, (800, 600));


#Background sound
if game_over_bool[0] == True:
    mixer.music.unload();
    mixer.music.load('endgame.mp3');
    mixer.music.play(-1);
else:
    mixer.music.load('background-music.mp3');
    mixer.music.play(-1); #Makes music play on loop


#Define playerX change and playerY change
playerX_Change = 0;
playerY_Change = 0;


#Score variable
score_value = 0;
font = pygame.font.Font('freesansbold.ttf', 32); #pyagme.font.Font('font', size)
textX = 10;
textY = 10;


#Game over text
game_over_font = pygame.font.Font('freesansbold.ttf', 128);


################################################################################################
#Defining functions
'''
#Define game_over_music() function
def game_over_music():
    if game_over_bool[0] == True:
        mixer.music.load('endgame.mp3');
        mixer.music.play(-1); #Makes music play on loop
'''
#Define show_score() function
def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (150, 0, 150)); #Render text first
    screen.blit(score, (x, y)); #Now blit text to show on screen


#Define game_over_text() function
def game_over_text():
    over_text = font.render("GAME OVER", True, (150, 0, 150));
    over_text2 = font.render("ALIENS WIN", True, (255, 255, 255));
    screen.blit(over_text, (300, 250));
    screen.blit(over_text2, (300, 350));
    
    
#Define player() function to load player image
def player(x, y): 
    screen.blit(playerImgResized, (x, y)); #Blit draws an image of the player on screen args (image (x, y))


#Define enemy() function to load enemy image  
def enemy(x, y, i):
    screen.blit(enemyImgResized[i], (x, y));
    
    
#Define bullet() function to fire bullet
def fire_bullet(x, y):
        global bullet_state; #Makes bullet_state accessible from within function
        bullet_state = "fire";
        screen.blit(bulletImgResized, (x + 16, y + 10));

#Define isCollision() to determine if a collision as occurred
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)));
    if distance < 27:
        return True; #Collision occurs
    else:
        return False; #No collision. You missed!
    
###########################################################################################################
#START GAME LOOP
#Game loop. Runs until running = False
running = True;
while running:
    #Fill with ((r, g, b)) - maximum value of 255 for each        
    screen.fill((150, 0, 150)); #Purple fill (I love purple)
    
    #Background image
    screen.blit(backgroundResized, (0, 0));
    
    #If quit button pressed, quit by running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False; #Close programme on close
            
        #MOVEMENT/BULLET
        #If key stroke is pressed, check whether right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_Change = -5;
            if event.key == pygame.K_RIGHT:
                playerX_Change = 5;   
            if event.key == pygame.K_UP: #Firing bullet with up key
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser-sound-new.wav');
                    bullet_sound.play();  #Load and play laser sound
                    
                    bulletX = playerX; #Can't use playerX value in function else the bullet follows the ship the whole time
                    fire_bullet(bulletX, bulletY);
                
        #If key stroke released        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0;

    
    
    #Changes x value depending on keystrokes
    playerX += playerX_Change;
    
    #Setting boundaries for player
    if playerX <= 0:
        playerX = 0;
    elif playerX >= 736: #736 is because width of playerImgResized = 64, and 800 - 64 = 736
        playerX = 736; #
        
    #For loop for number of enemies
    #Deals with collision for every enemy & every enemy change in direction
    for i in range(num_of_enemies):
        
        #Game over clause - ends game if enemy reaches player
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000;
            game_over_text();
            game_over_bool.clear();
            game_over_bool.append(True);
            break;
            
        
        enemyX[i] += enemyX_Change[i];
        
        if enemyX[i] <= 0:
            enemyX_Change[i] = 2;
            enemyY[i] += enemyY_Change[i]; #Brings enemy down when side is hit
        elif enemyX[i] >= 736:
            enemyX_Change[i] = -2;
            enemyY[i] += enemyY_Change[i];
        
        #Collision check
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY);
        if collision:#If true
            explosion_sound = mixer.Sound('explosion-sound-new.wav');
            explosion_sound.play(); #Playing explosion sound
            bulletY = 480;
            bullet_state = 'ready';
            score_value += 1;
            #Reset enemy position 
            enemyX[i] = random.randint(0, 735);
            enemyY[i] = random.randint(50, 150);
        enemy(enemyX[i], enemyY[i], i);
    #Enemy For loop end
        
    #Bullet movement
    if bulletY <= 0:
        bulletY = 480;
        bullet_state = 'ready';
        
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY);
        bulletY -= bulletY_Change;
        
    #Show score function
    show_score(textX, textY);
        
          
    #Spawns player
    player(playerX, playerY);   
    
    #Constantly update display
    pygame.display.update();       
    
####################################################################################################################
#END GAME LOOP    
#Actually quits game instead of making it not respond  
pygame.quit();


    
    
    
    