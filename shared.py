import os
from PIL import Image
from turtle import Screen, Turtle
import constants as c
from time import sleep, time

# variable holder work folder for image files management
base_path = os.path.dirname(os.path.abspath(__file__)) + c.IMG_DIR
explosion_img = base_path + "explosion.gif" # image to be displayed when alien or defender is hit

class SharedScreen:
    def __init__(self):
        # creates game screen
        self.screen = Screen()
        self.screen.setup(1.0, 1.0)
        self.screen.bgcolor("black")
        self.screen.title('Space Invaders')
        self.screen.tracer(0)

        # Prevent resizing
        self.screen.cv._rootwindow.resizable(False, False) 
        # calculate game components sizes based on device's screen size
        self.canvas_side_pixels = int(min(self.screen.window_width(), self.screen.window_height()))
        # stores a black image representing a barrier damaged by bomb
        self.black_img = None 
        self.explosion_control = 1 # ensures explosion object available for use
        self.stop = False # stops the timers when set to True

        # create explosion image
        explosion_size = (int(self.canvas_side_pixels / c.GRID_COLUMNS * c.BARRIERS_WIDTH), int(self.canvas_side_pixels / c.GRID_COLUMNS * c.BARRIERS_WIDTH / c.IMG_GRID[1]))
        resize_explosion_file = resize_image(explosion_img, explosion_size)
        self.screen.register_shape(resize_explosion_file)
        self.explosion = Turtle()
        self.explosion.ht()
        self.explosion.shape(resize_explosion_file)
        self.explosion.goto(0, 0)

        # game shared references
        self.defender = None
        self.position_list = [] # maps all (x,y) pixel positions in the grid to move the turtle elements
        self.barrier_list = []  # list of all barriers
        self.alien_list = [[], []]  # Holds two lists of aliens which are identical except for the aliens' images. Alternating between the lists creates the animation
        self.pointer = 12 # variable holding the alien's top left position. 
        self.alien_bomb_list = []   # holds all bombs launched by aliens
        self.defender_bomb_list = [] # holds all bombs launched by defender
        self.alien_distance = int
        self.bomb_distance = int
        self.defender_distance = int
        self.barrier_part_distance_x = int
        self.barrier_part_distance_y = int
        self.alien_points = []
        self.points = 0
        self.lives = 3
        self.lives_list = []
                

    # class methods
    def check_bomb_hit(self):
        if self.pointer % 2 == 0:
            visible_aliens = self.alien_list[0]
        else:
            visible_aliens = self.alien_list[1]
        for bomb in self.defender_bomb_list:
            # check if bombs hit a shield
            self.check_shield_hit(bomb, self.defender_bomb_list)
            # check if bombs hit an alien
            for idx, alien in enumerate(visible_aliens):
                if alien != None:
                    if bomb.distance(alien.pos()) < (self.bomb_distance + self.alien_distance):
                        if self.explosion_control == 0:
                            bomb.bomb_pause = 1 # if explosion object is being used, bomb will be frozen until explosion available
                        else:   
                            alien.ht()
                            self.explode_target(alien.pos())
                            self.destroy_bomb(bomb, self.defender_bomb_list)
                            self.points += self.alien_points[idx]
                            self.alien_list[0][idx] = None  # substitute alien turtle object by None
                            self.alien_list[1][idx] = None  # substitute alien turtle object by None
            # move bom forward
            if not bomb.bomb_pause:
                bomb.forward(c.BOMB_SPEED)
            # check if bomb hit the top of screen
            if bomb.ycor() > self.canvas_side_pixels / 2:
                self.destroy_bomb(bomb, self.defender_bomb_list)
                     
        for bomb in self.alien_bomb_list:
            # check if bombs hit a shield
            self.check_shield_hit(bomb, self.alien_bomb_list)
            # check if bombs hit defender
            if bomb.distance(self.defender.pos()) < (self.bomb_distance + self.defender_distance):
                if self.explosion_control == 0:
                    bomb.bomb_pause = 1
                else:   
                    self.defender.ht()
                    self.explode_target(self.defender.pos())
                    self.destroy_bomb(bomb, self.alien_bomb_list)
                    self.lives_list[self.lives - 2].ht()
                    self.lives -= 1
                    self.lives_list.pop()
                    if self.lives == 0:
                        self.game_over()
                    else:
                        sleep(3)
                        self.defender.goto(self.defender.initial_position)
                        self.defender.st()
            # move bomn forward
            if not bomb.bomb_pause:
                bomb.forward(c.BOMB_SPEED)
            # check if bomb hit the bottom of screen
            if bomb.ycor() < -self.canvas_side_pixels / 2:
                self.destroy_bomb(bomb, self.alien_bomb_list)

        self.check_game_over(visible_aliens)
        
        if not self.stop:
            self.screen.ontimer(self.check_bomb_hit, 50)


    def check_shield_hit(self, bomb, bomb_list):
        # barrier_hit, if exists, is the barrier on the trajectory of a bomb, as selected when bomb was created
        # barrier_idx holds the index of the barrier sub-image hit based on the bomb coordinates
        if bomb.barrier_hit != None:
            part_hit_coords = bomb.barrier_hit['sub_img_coords'][bomb.barrier_idx]
            if abs(bomb.ycor() - part_hit_coords[1]) < (self.barrier_part_distance_y + self.bomb_distance):
                if self.explosion_control == 0:
                    bomb.bomb_pause = 1
                else:   
                    self.explode_target(part_hit_coords)
                    self.destroy_bomb(bomb, bomb_list)
                    self.update_image(bomb.barrier_hit)


    def check_game_over(self, visible_aliens):
        # checks for active alien
        active_aliens = [alien for alien in visible_aliens if alien != None]
        if len(active_aliens) == 0:
            self.game_over()

        # check if aliens hit the defender or landed
        defender_y_cor = self.defender.pos()
        for alien in active_aliens[::-1]:
            if alien.distance(defender_y_cor) < (self.alien_distance + self.defender_distance):
                self.game_over()
                break

        # checks if the aliens hit a barrier
        active_barrier_positions = []
        for barrier in self.barrier_list:
            active_barrier_sub_list = [coord for coord, idx in zip(barrier['sub_img_coords'], barrier['sub_img_idx']) if idx == 1]
            active_barrier_positions.extend(active_barrier_sub_list)
        
        for alien in active_aliens[::-1]:
            for pos in active_barrier_positions:
                if alien.distance(pos) < (self.alien_distance + self.barrier_part_distance_x):
                    self.game_over()
                    break

    
    def explode_target(self, coordinates):
        self.explosion_control = 0
        self.explosion.goto(coordinates[0], coordinates[1]) 
        self.explosion.st()
        # manages explosions appearance time
        if not self.stop:
            self.screen.ontimer(lambda: self.end_explosion(), 200)


    def end_explosion(self):
        # turn off explosion
        self.explosion.ht()
        self.explosion_control = 1


    def destroy_bomb(self, bomb, bomb_list):
        bomb_index = bomb_list.index(bomb)
        removed_bomb = bomb_list.pop(bomb_index)
        removed_bomb.ht()
          
    
    def update_image(self, barrier):
    # Reconstruct the full shield image from sub-images and update the shape
        # Create a new blank image
        img_width = int(c.BARRIERS_WIDTH * self.canvas_side_pixels // c.GRID_COLUMNS)
        img_height = img_width 
        new_img = Image.new("RGB", (img_width, img_height))

        # Paste sub-images into the reconstructed image
        for idx, sub_img in enumerate(barrier['sub_images']):
            row, col = divmod(idx, c.IMG_GRID[0])
            left = col * sub_img.size[0]
            top = row * sub_img.size[1]
            new_img.paste(sub_img, (left, top))

        # Save the new image and update the Turtle shape
        img_path = barrier['image']
        new_img.save(img_path)
        self.screen.register_shape(img_path)
        barrier['barrier'].shape(img_path)


    def game_over(self):
        # Display "GAME OVER" label
        label = Turtle()
        label.hideturtle()
        label.penup()
        label.color("red")
        label.goto(0, 50)
        label.write("GAME OVER", align="center", font=("Arial", 36, "bold"))

        # Display "Press any key to leave" message
        label.goto(0, -20)
        label.write("Press any key to leave", align="center", font=("Arial", 16, "normal"))
        setup_folder()
        self.stop = True
        self.screen.onkeypress(self.exit_game)
        self.screen.listen()


    # Define a function to close the game
    def exit_game(self):
        self.screen.bye()
        self.screen.clear()


def setup_folder():
    # image file organizer
    # Iterate over all files in the current directory
    for file_name in os.listdir(base_path):
        # Check if "delete" is in the file name
        if "delete" in file_name:
            file_path = os.path.join(base_path, file_name)
            # Delete the file
            try:
                os.remove(file_path)
                print(f"Deleted: {file_name}")
            except Exception as e:
                print(f"Error deleting {file_name}: {e}")


def resize_image(image_path, size):
    # receives the file name from alien_elements, resizes it, and registers the turtle shape
    # returns a modified file name containing the path to the resized image
    img = Image.open(image_path)
    img = img.resize(size, Image.NEAREST)
    img_name, extension = os.path.splitext(image_path)
    new_image_name = f'{img_name}_{size[0]}X{size[1]}_delete{extension}'
    img.save(new_image_name)
    return new_image_name



   