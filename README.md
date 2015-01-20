AdventureGame
=============

This code uses pygame to create an adventure game GUI. 

It also uses pygbutton to toggle between the two possible motions
for the dog (the dog can move in circles or can randomly choose
a target and move towards it).  

The user can use the up/down/left/right arrow keys to move the cat
around the screen.  If the cat passes through an image before
the dog, then the cat gets points for that image.  If the dog 
gets to the image first, the cat gets no points for the image. 
The game can also be restarted by clicking on the 'Change Dog 
Motion' button.  That button changes the motion of the dog
and restarts the game.  

Note: holding down multiple arrow keys will accelerate the cat and
move the cat in diagonal motions.

Note: If the center of the moving image passes inside another 
image's boundary, a collision has happened (and a point may 
be gained).  Holding down arrow keys currently keeps the image 
in motion until a boundary of the background is reached.

To run the game, type the following command in your 
terminal (from this directory):
python Mittensgui.py

There is a folder called JavascriptVersion, which contains the 
version of the code that I rewrote in Javscript.  You can run it
in your web browser by typing your path to the 
JavascriptVersion/index.html file into your web browser.  It has 
been tested in some versions of Chrome, Internet Explorer and 
Safari.  It has some problems in Firefox that I have not yet resolved.  
If you don't want to clone this repository but want to play the game, 
you can do so at: GrassAdventures.github.io

