import math
def compute_radius(input_image,circle_center):
   """This function returns the radius of the new circle."""

   x_component = input_image.pos[0] - circle_center[0]
   y_component = input_image.pos[1] - circle_center[1]

   radius = math.sqrt(x_component**2 + y_component**2)

   return radius
