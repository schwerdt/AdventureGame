import pygame
from pygame.locals import *
from sys import exit
import image_class
from check_for_collision import check_for_collision
import random
import sys

#Initialize pygame submodules (load drivers/query hardware, makes possible for
#hardware to be used by pygame)
#Could do pygame.sound.init() if just wanted sound for example
pygame.init()

SCREEN_SIZE = (900,700)
score = 0
collision = False
find_new_target = True  #determines whether the antogonist should find a new target. Set to false after target is chosen.
#Create a display surface
screen = pygame.display.set_mode(SCREEN_SIZE,0,32) #Returns a surface object (the window)
pygame.display.set_caption("Grass Adventures")

#Create background and rescale the image size
background = pygame.image.load('grass_sideview.jpg').convert()
background_size = background.get_size()
background = pygame.transform.scale(background,(int(2*background_size[0]),int(2*background_size[1])))

#Get picture of Mittens
Mittens_image = image_class.image_class('Mittens.jpg',0.1,[100,100])
Sunny_image = image_class.image_class('Sunny_Snow.png',0.45,[300,300])

#Create lists of flower and animal images
flower_list = []
hyacinth_image = image_class.image_class('hyacinths.jpg',0.1,[200,200])
lily_image = image_class.image_class('lilyplant.jpg',0.5,[500,500])
callalily_image = image_class.image_class('callalily.png',0.5,[700,200])
#callalily_image.set_color_key((255,255,255))
flower_list.append(hyacinth_image)
flower_list.append(lily_image)
flower_list.append(callalily_image)

animal_list = []
bunny_image = image_class.image_class('babybunny.jpg',0.4,[200,600])
bluebird_image = image_class.image_class('bluebird.png',0.4,[700,100])
animal_list.append(bunny_image)
animal_list.append(bluebird_image)

target_list = flower_list + animal_list

while True:
   for event in pygame.event.get():
      if event.type == QUIT:
         exit()
      if event.type == KEYDOWN:
         Mittens_image.update_position(event.key,SCREEN_SIZE)
                             
                         
   #Keep Mittens moving if a key is held down. Otherwise decelerate her.
   keys = pygame.key.get_pressed()
   if sum(keys) > 0:   #Some keys are pressed
      for i in range(len(keys)): #Check which keys are pressed
         if keys[i] != 0:
            Mittens_image.update_position(i,SCREEN_SIZE)
   else:
      Mittens_image.update_position(KEYUP,SCREEN_SIZE)

   #Update Sunny position randomly
#  Sunny_image.update_position_random(SCREEN_SIZE)

   #Update Sunny position by choosing a target image
   #randomly choose from flower list
   if find_new_target:
     current_target = random.choice(target_list)
   find_new_target = Sunny_image.update_position_target(SCREEN_SIZE,current_target)

   #Update Sunny position by having her run in circles
   # Sunny_image.update_position_circle([58.578,58.578],450)

   screen.blit(background,(0,0))
   screen.blit(Mittens_image.image,Mittens_image.pos)
   screen.blit(Sunny_image.image,Sunny_image.pos)

   #Check for collisions with Sunny and Mittens
   for target_item in target_list:
      screen.blit(target_item.image,target_item.pos)
      #Check for collision with Mittens
      if not target_item.collided:
         collision = check_for_collision(Mittens_image,target_item)
         if collision:
            score += 1
            target_item.update_collision_status(collision)
         #Check to see if Sunny collided with a flower, no points, but
         #now Mittens won't be able to get points for this image
         else:
            collision = check_for_collision(Sunny_image,target_item)
            if collision:
               target_item.update_collision_status(collision)

   #Display the score on the screen
   score_text = 'Score: ' + str(score)
   myfont = pygame.font.SysFont("monospace",35)
   label = myfont.render(score_text,1,(255,255,0))
   screen.blit(label,(600,30))   

   #Check to see if all items in target_list have had a collision
   already_hit = [target_item.collided for target_item in target_list]
   if sum(already_hit) == len(target_list):
      print 'Game is over.  All targets have been smelled.'
      sys.exit()

   pygame.display.update()


