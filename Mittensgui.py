import pygame
from pygame.locals import *
from sys import exit
import image_class
from check_for_collision import check_for_collision
import random

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
Sunny_image = image_class.image_class('Sunny_Snow.png',0.7,[300,300])

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

   #Always update the position of the random movement sprite
   #Sunny_image.update_position_random(SCREEN_SIZE)
   #randomly choose from flower list
#  if find_new_target:
#    target_flower = random.choice(flower_list)
#    print 'finding a new target'
#  find_new_target = Sunny_image.update_position_target(SCREEN_SIZE,target_flower)
#  print 'after sunny update, find_new_target is', find_new_target
   Sunny_image.update_position_circle([200,200],170)

   screen.blit(background,(0,0))
   screen.blit(Mittens_image.image,Mittens_image.pos)
   screen.blit(Sunny_image.image,Sunny_image.pos)
   for flower in flower_list:
      screen.blit(flower.image,flower.pos)
      #Check for collision with Mittens
      if not flower.collided:
         collision = check_for_collision(Mittens_image,flower)
         if collision:
            score += 1
            flower.update_collision_status(collision)
         #Check to see if Sunny collided with a flower, no points, but
         #now Mittens won't be able to get points for this image
         collision = check_for_collision(Sunny_image,flower)

   for animal in animal_list:
      screen.blit(animal.image,animal.pos)
      #Check for collision with Mittens
      if not animal.collided:
         collision = check_for_collision(Mittens_image,animal)
         if collision:
            score += 1
            animal.update_collision_status(collision)
         #Check to see if Sunny collided with a flower, no points, but
         #now Mittens won't be able to get points for this image
         collision = check_for_collision(Sunny_image,flower)

   #Display the score on the screen
   score_text = 'Score: ' + str(score)
   myfont = pygame.font.SysFont("monospace",35)
   label = myfont.render(score_text,1,(255,255,0))
   screen.blit(label,(600,30))   

   #Check for collisions

   pygame.display.update()


