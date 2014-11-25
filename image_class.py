import pygame

class image_class:
   """A class to hold information about sprites"""

   def __init__(self,filename,scale_factor,image_pos):
      self.filename = filename
      self.scale_factor = scale_factor
      self.pos = image_pos  #Should be x,y coordinates in a list, this is the center of the image
      self.collided = False #This variable is True if a meeting/collision has occured with Mittens

      self.image = pygame.image.load(filename).convert_alpha()
      self.size_tuple = self.image.get_size()
      self.size = [0,0]
      self.size[0] = int(self.size_tuple[0]*self.scale_factor)
      self.size[1] = int(self.size_tuple[1]*self.scale_factor)
      self.image = pygame.transform.scale(self.image,self.size)

   def update_position(self,key_press,screen_size):
      if key_press == pygame.K_LEFT:
         if self.pos[0] > 0:
            self.pos[0] -= 2
      if key_press == pygame.K_RIGHT:
         if self.pos[0] < (screen_size[0] - self.size[0]):
            self.pos[0] += 2
      if key_press == pygame.K_UP:
         if self.pos[1] > 0:
            self.pos[1] -= 2
      if key_press == pygame.K_DOWN:
         if self.pos[1] < (screen_size[1]- self.size[1]):
            self.pos[1] += 2
       
   def update_collision_status(self,collision):
      self.collided = True

