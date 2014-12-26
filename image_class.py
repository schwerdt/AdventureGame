import pygame
from pygame.locals import *
import random
import math
from check_for_collision import check_for_collision

class image_class:
   """A class to hold information about sprites"""

   def __init__(self,filename,scale_factor,image_pos):
      self.filename = filename
      self.scale_factor = scale_factor
      self.pos = image_pos  #Should be x,y coordinates in a list, this is the center of the image
      self.vel = [0,0]  #Velocity of the image
      self.collided = False #This variable is True if a meeting/collision has occured with Mittens
      self.circle_angle = 0
      self.circle_angle_limit = 0

      self.image = pygame.image.load(filename).convert_alpha()
      self.size_tuple = self.image.get_size()
      self.size = [0,0]
      self.size[0] = int(self.size_tuple[0]*self.scale_factor)
      self.size[1] = int(self.size_tuple[1]*self.scale_factor)
      self.image = pygame.transform.scale(self.image,self.size)

   def update_position(self,key_press,screen_size):
      if key_press == pygame.K_LEFT:
         if self.pos[0] > 0:
            if self.vel[0] <= 0:
               self.vel[0] -= 0.01
            else:
               self.vel[0] = 0.0
            self.pos[0] = self.pos[0] + self.vel[0]
      if key_press == pygame.K_RIGHT:
         if self.pos[0] < (screen_size[0] - self.size[0]):
            if self.vel[0] >= 0:
               self.vel[0] += 0.01  
            else:
               self.vel[0] = 0
            self.pos[0] = self.pos[0]  + self.vel[0]
      if key_press == pygame.K_UP:
         if self.pos[1] > 0:
            if self.vel[1] <= 0:
               self.vel[1] -= 0.01
            else:
               self.vel[1] = 0.0
            self.pos[1] = self.pos[1] + self.vel[1]
      if key_press == pygame.K_DOWN:
         if self.pos[1] < (screen_size[1]- self.size[1]):
            if self.vel[1] >= 0:
               self.vel[1] += 0.01
            else:
               self.vel[1] = 0.0
            self.pos[1] = self.pos[1] + self.vel[1]
      if (key_press != pygame.K_UP) and (key_press != pygame.K_DOWN) and (key_press !=pygame.K_LEFT) and (key_press != pygame.K_RIGHT):
         self.vel[0] = 0.99*self.vel[0]
         self.vel[1] = 0.99*self.vel[1]
         #Check to make sure the image stays on the screen before updating pos
         if (self.pos[0] > 0) and (self.pos[0] < screen_size[0] -self.size[0]) and (self.pos[1] > 0) and (self.pos[1] < screen_size[1] - self.size[1]):
           self.pos[0] = self.pos[0] + self.vel[0]
           self.pos[1] = self.pos[1] + self.vel[1]
    

   
   def update_collision_status(self,collision):
      self.collided = True



   def update_position_random(self, screen_size):
      """This function will move the image through the screen, without requiring key presses."""
      #Use random numbers to generate the horizontal and vertical displacement
      range_max = 2
      vert_disp = random.randrange(0,range_max)
      horiz_disp = random.randrange(0,range_max)
      #Choose the direction of the displacement
      sign = [-1,1]
      vert_sign = random.choice(sign)
      horiz_sign = random.choice(sign)

     #Make sure the image remains on the screen
      if (self.pos[0] > 0) and (self.pos[0] < screen_size[0] - self.size[0]) and (self.pos[1] > 0) and (self.pos[1] < screen_size[1] - self.size[1]):
         self.pos[0] += horiz_disp*vert_sign
         self.pos[1] += vert_disp*horiz_sign

   def update_position_target(self,screen_size,target):
      """This function will move the image through the screen towards an image."""
      #target is an image_class object.  It also has coordinates
      find_new_target = False
      #Find the vector along which the image should move toward the target.
      direction_vector = [target.pos[0] - self.pos[0], target.pos[1] - self.pos[1]]
      #Turn image away from boundary.  Change logical so we can find a new target next iteration
      if (self.pos[0] < 0) or (self.pos[0] > screen_size[0] - self.size[0]) or (self.pos[1] < 0) and (self.pos[1] > screen_size[1] - self.size[1]):
         find_new_target = True
      else:
         self.pos[0] += direction_vector[0]*.005
         self.pos[1] += direction_vector[1]*.005
 
      #Check to see if there was a collision
      find_new_target = check_for_collision(self,target)

      return find_new_target


   def update_position_circle(self,circle_center,radius):
      """This routine will move the image in a circle around the gui."""
      self.circle_angle += math.pi/500 #This is the new angle
      #(x-x0) = radius*cos(theta)
      #(y-y0) = radius*sin(theta)
      #Compute the values of x and y, which are the image's position
      #x0 and y0 are the coordinates in circle_center
      coord_save = self.pos[:]
      self.pos[0] = circle_center[0] + radius*math.cos(self.circle_angle)
      self.pos[1] = circle_center[1] + radius*math.sin(self.circle_angle)
#     if abs(coord_save[0] - self.pos[0]) > 5 or (abs(coord_save[1] - self.pos[1]) > 5):
#        print 'large diff in coordinates'
      if self.circle_angle >= self.circle_angle_limit:
         return True
      else:
         return False
