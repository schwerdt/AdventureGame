import math
def compute_angle_newcircle(input_image,circle_center):
   """This code takes the current image position and the new circle center and computes the angle of the image in the circle.  The goal is to achieve continuity for the image."""
   x_component = input_image.pos[0] - circle_center[0]
   y_component = input_image.pos[1] - circle_center[1]   
   radius = math.sqrt(x_component**2 + y_component**2)   

   #compute the angle associate with the current image position and the new center
   #Because of the default quadrants for arccos and arcsin, we have to know ahead of time 
   #which quadrant of the new circle the point is in
   #Quadrants 1 and 2 (including axes)
   if y_component >= 0.0:
      theta = math.acos(x_component/radius)   
   #Quadrant 4 
   elif x_component >= 0.0 and y_component < 0.0:
      theta = math.asin(y_component/radius) + 2*math.pi
   elif x_component < 0.0 and y_component < 0.0:
      theta = 2*math.pi - math.acos(x_component/radius) 
   else: 
      print 'There was a problem with determining the quadrant of the new circle where the current point is located.\n'

   return theta  #This is the angle of the image around the circle
