alert('Instructions: Move the cat with the arrow keys. Earn points by visiting targets before the dog visits them.  The motion of the dog can be changed by clicking the Change Dog Motion button.');
//Get the canvas ready
var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d'); 
canvas.width = 1000;  //Set the size of the canvas
canvas.height = 600;

var button_size = [120,30];  //the size of the button (that changes dog motion)
var button_pos = [0,0];  //The position (upper left corner) of button

var find_new_target = true;   //If dog is doing targeted motion, this variable is true if the dog reached the target and must look for a new one
var current_target = -1;
var move_in_circle = false; //this is true if the dog will do circular motion, rather than targeted motion
var new_circle = true;  //true when the dog completes a circle and a new circle should be generated


//Create the background for the canvas
var grass_background = new Image();
grass_background.src = 'grass_sideview.jpg';
grass_background.onload = function() {
   var pattern = ctx.createPattern(this,"no-repeat");
   ctx.fillStyle = pattern; 
   ctx.rect(0,0,canvas.width,canvas.height);
   ctx.fill();
};

//Get pressed keys
var keysDown = {};
window.addEventListener('keydown',function(e) {
   keysDown[e.keyCode] = true;
});
window.addEventListener('keyup',function(e) {
   delete keysDown[e.keyCode];  //remove this key from keys down
});


      
//If move_in_circle is true: the dog moves in a full circle.  Then a new circle center
//is randomly chosen.  We need to compute the angle of the dog relative to the new
//circle center.
function compute_angle_newcircle(input_image,circle_center) {
   var x_component = input_image.pos[0] - circle_center[0];
   var y_component = input_image.pos[1] - circle_center[1];
   var radius = Math.sqrt(Math.pow(x_component,2) + Math.pow(y_component,2));

   //Need to figure out which quadrant of the new circle the image is currently in
   if( y_component >= 0.0) {
      var theta = Math.acos(x_component/radius); 
      return theta; }
   else if(x_component >= 0.0  && y_component < 0.0) { 
      var theta = Math.asin(y_component/radius) + 2*Math.PI; 
      return theta; } 
   else if(x_component < 0.0 && y_component < 0.0) {
      var theta = 2*Math.PI - Math.acos(x_component/radius); 
      return theta; }
   else {
      console.log('Some problem with determining the quadrant of the angle'); }
}

 



//Create an image object that store the position/velocity,image, collision status
var image_object = function(filename,scale_factor,initial_position,image_size) {
   this.image = new Image();
   this.image.ready = true;
   this.image.src = filename;

   this.pos = initial_position;
   this.vel = [0,0];
   this.collided = false;
   this.size = image_size;
   this.scale_factor = scale_factor;
   this.circle_angle = 0.0;
   this.circle_angle_limit = 0.0;
   

   this.listDetails = function() {
      document.write('the image is ' + this.filename + "<br /?");
      document.write('the pos is ' + this.pos + "<br />");
   }


   //Updates the position of the cat, which is controlled by the arrow keys
   this.update_position = function() {
      var vel_change = 0.01;
      if(37 in keysDown) {  //left arrow
         if (this.pos[0] > 0) {
            if (this.vel[0] <= 0) {
               this.vel[0] -= vel_change;  }
            else {
               this.vel[0] = 0.0; }
            this.pos[0] += this.vel[0];  } }
      if(38 in keysDown) {  //up arrow
         if (this.pos[1] > 0) {
            if (this.vel[1] <= 0.0) {
               this.vel[1] -= vel_change; }
            else {
               this.vel[1] = 0.0; }
            this.pos[1] += this.vel[1];  } }
      if(39 in keysDown) { //right arrow
         if(this.pos[0] < canvas.width - this.size[0]) {
            if(this.vel[0] >= 0) { 
               this.vel[0] += vel_change;  }
            else {
               this.vel[0] = 0.0; } 
            this.pos[0] += this.vel[0]; } }
      if(40 in keysDown) { //down arrow
         if(this.pos[1] < canvas.height - this.size[1]) {
            if(this.vel[1] >= 0) {
               this.vel[1] += vel_change; }
            else {
               this.vel[1] = 0.0; }
            this.pos[1] += this.vel[1]; } }
      //If up/down keys not pressed, decelerate velocity in y direction
      if(!(40 in keysDown) && !(38 in keysDown)) {
         this.vel[1] = this.vel[1] *0.99; }
      //if left/right keys not pressed, decelerate velocity in x direction
      if(!(37 in keysDown) && !(39 in keysDown)) {
         this.vel[0] = this.vel[0] * 0.99; }
      if((this.pos[0] > 0) && (this.pos[0] < canvas.width - this.size[0])) {
         this.pos[0] = this.pos[0] + this.vel[0]; }
      if((this.pos[1] > 0) && (this.pos[1] < canvas.height - this.size[1])) {
         this.pos[1] = this.pos[1] + this.vel[1]; } 

  }

   //Updates the position of the dog if move_in_circle is false 
   //(so we are choosing a target and moving the dog towards it)
   this.update_position_target = function(screen_size, target) {
      find_new_target = false;
      direction_vector = [target.pos[0] - this.pos[0], target.pos[1] - this.pos[1]];

      this.pos[0] += direction_vector[0]*.01;
      this.pos[1] += direction_vector[1]*.01; 

       //Check to see if there was a collision
       find_new_target = check_for_collision(this,target);
       return find_new_target; }


   //Updates the position of the dog, if move_in_circle is true
   this.update_position_circle = function(circle_center, radius) { 
      this.circle_angle += Math.PI/300; //Updates the circle angle
      coord_save = this.pos;
      this.pos[0] = circle_center[0] + radius*Math.cos(this.circle_angle);
      this.pos[1] = circle_center[1] + radius*Math.sin(this.circle_angle);
      if (this.circle_angle >= this.circle_angle_limit)  { 
         return true; }
      else {
         return false; }
    }


      
   
};


function check_for_collision(item1, item2) {
   //Check for a collision by checking that the x and y coordinates of item1 are within the bounds of item2
   var item1_center = item1.pos;
   var item2_center = item2.pos;
 
   var item2_size = item2.size;
   //Compute the max/min x and max/min y in item2's rectangle
   var x_min = item2_center[0] - item2_size[0]/2;
   var x_max = item2_center[0] + item2_size[0]/2;
   var y_min = item2_center[1] - item2_size[1]/2;
   var y_max = item2_center[1] + item2_size[1]/2;

   //Determine if the center of item1 is within the bounds of item2's rectangle
   if((x_min < item1_center[0]) && (x_max > item1_center[0]) && (y_min < item1_center[1]) && (y_max > item1_center[1])) {
      return true; }
   else  {
      return false; }
}

//This routine processes the location of a mouse click.  The reason it exists is to see
//if a mouse click occurred inside the button on the canvas (which controls the dog motion)
function getPosition(event) {
   if(event.x != undefined && event.y != undefined) {
      var x = event.x; 
      var y = event.y;
      if(x > button_pos[0] && x < button_size[0] + button_pos[0] && y > button_pos[1] && y < button_pos[1] + button_size[1]) {
         //Button was clicked. 
         move_in_circle = !move_in_circle;
         //Restart the game
         score = 0;
         //Change status of all target images to not collided
         for(var j = 0;j < target_list.length; j++) { 
            target_list[j].collided = false; }
        }
   }
}


//Computes the number of targets that have been visited (by cat and dog)
function getNumTargetsVisited(target_list) {
   var num_targets_visited = 0;
   for(var j=0; j < target_list.length; j++) {
      if (target_list[j].collided == true) {
         num_targets_visited += 1
       }
    }
   return num_targets_visited; 
}



var Mittens_obj = new image_object('Mittens.jpg',0.1,[100,100],[50,75]);
var Sunny_obj = new image_object('Sunny_Snow.png',0.1,[300,300],[150,125]);

//Read in other object with which collisions will occur and store in array
var target_list = new Array();
target_list[0] = new image_object('babybunny.png',0.4,[200,500],[75,75]);
target_list[1] = new image_object('bluebird.png',0.4, [700,100],[75,75]);
target_list[2] = new image_object('hyacinths.png',0.1,[200,200],[100,100]);
target_list[3] = new image_object('lilyplant.png',0.5,[500,500],[100,100]);
target_list[4] = new image_object('callalily.png',0.5,[700,300],[100,100]);

var score = 0;



function render() {
  //draws grass background
  ctx.drawImage(grass_background,0,0,canvas.width,canvas.height); 
  //draw Mittens at her current position
  ctx.drawImage(Mittens_obj.image,Mittens_obj.pos[0], Mittens_obj.pos[1],Mittens_obj.size[0], Mittens_obj.size[1]);
  ctx.drawImage(Sunny_obj.image,Sunny_obj.pos[0], Sunny_obj.pos[1], Sunny_obj.size[0], Sunny_obj.size[1]);
  
  //Draw all of the targets at their current stored position
  for(var j=0; j< target_list.length; j++) {
     ctx.drawImage(target_list[j].image,target_list[j].pos[0], target_list[j].pos[1],target_list[j].size[0], target_list[j].size[1]); }

   //Print the score to the screen
   ctx.font = "50px Ariel";
   ctx.fillStyle = "Yellow";
   ctx.fillText("Score: " + score,700,50);

   //Put the button (to change dog motion) on the canvas
   ctx.fillStyle = "#707070";
   ctx.fillRect(button_pos[0], button_pos[1], button_size[0], button_size[1]);
   ctx.fillStyle = "#FFFFFF";
   ctx.font = "14px Ariel";
   ctx.fillText("Change Dog Motion",button_pos[0],button_pos[1]+button_size[1]/2);

   //Check to see if all targets have been visited
   var target_visited_sum = getNumTargetsVisited(target_list);

   if(target_visited_sum == target_list.length) { 
      ctx.font = "50px Ariel";
      ctx.fillStyle = "Yellow";
      ctx.fillText("Game over.  All objects have been visited.",100,300); }
      

}

function run() {

   render();

   if(find_new_target) {
      current_target = Math.floor(Math.random()*target_list.length);
      //During game play, only visit targets that have not experienced a collision
      //After the game is over, any random target can be visited because we don't go into the if statement 
      //to check if current_target has been visited.
      if(getNumTargetsVisited(target_list) != target_list.length) { 
         while(target_list[current_target].collided == true) {
            current_target = Math.floor(Math.random()*target_list.length); }
         }
      }

   
   Mittens_obj.update_position();

   //If a circle has been completed, then randomly choose a new circle center
   if(new_circle) {
      circle_range = [500,300];
      circle_center = [Math.floor(Math.random()*circle_range[0])+200, Math.floor(Math.random()*circle_range[1])+200];
      Sunny_obj.circle_angle = compute_angle_newcircle(Sunny_obj,circle_center);
      Sunny_obj.circle_angle_limit = Sunny_obj.circle_angle + 2*Math.PI;
      radius = Math.sqrt(Math.pow((Sunny_obj.pos[0] - circle_center[0]),2) + Math.pow((Sunny_obj.pos[1] - circle_center[1]),2));
      new_circle = false;
    }

   //Update position of dog (for either circular or targeted motion)
   if(move_in_circle) {
      new_circle = Sunny_obj.update_position_circle(circle_center,radius); }
   else {
     find_new_target = Sunny_obj.update_position_target([canvas.width,canvas.height],target_list[current_target]); }

   //Check to see if the cat and then the dog had a collision with a target
   for(var j=0; j < target_list.length; j++) {
      if(!(target_list[j].collided)) {
         collision = check_for_collision(Mittens_obj,target_list[j]);
         if(collision) {
            score += 1
            target_list[j].collided = true;  //update the collision status of this target
            }
         else {  
            collision = check_for_collision(Sunny_obj,target_list[j]);
            if(collision) {
               target_list[j].collided = true; } }
        }
    }




   time = Date.now();
}

var time = Date.now();
setInterval(run,10);







