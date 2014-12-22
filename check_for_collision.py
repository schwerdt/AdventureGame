import sys

def check_for_collision(item1,item2): #item1 and item2 should be image objects
   #Check for a collision by checking of the x and y coordinates of item1 are within the edges of item2

   item1_center = item1.pos  #item1.pos[:] if I want a copy
   item2_center = item2.pos

   #Compute the max/min x and max/min y in item2's rectangle
   item2_size = item2.image.get_size() #this is a tuple
   x_min = item2_center[0] - item2_size[0]/2
   x_max = item2_center[0] + item2_size[0]/2
   y_min = item2_center[1] - item2_size[1]/2
   y_max = item2_center[1] + item2_size[1]/2


   #Determine if the center of item1 is within the bounds of item2's rectangle
   if (x_min < item1_center[0]) and (x_max > item1_center[0]) and (y_min < item1_center[1]) and (y_max > item1_center[1]):
      return True
   else:
      return False


