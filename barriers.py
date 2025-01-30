import os
import constants as c
from turtle import Turtle
from PIL import Image
from shared import resize_image

# variable holder work folder for image files management
base_path = os.path.dirname(os.path.abspath(__file__)) + c.IMG_DIR

class Barriers():
    def __init__(self, resources):
        super().__init__()
        # barriers variables
        self.resources = resources
        self.screen = self.resources.screen
        self.position_list = self.resources.position_list # holds all positions in the game grid
        self.black_img = None # placeholder for the image which will substitute the part of a barrier hit by a bomb
        # barrier objects attributes
        # each barrier is represented by a dictionary containing (a) a turtle object and accessory elements:
        # (b) barrier image (c) list of barrier cropped sub_images, (d) list of barrier cropped sub_images coordinates and 
        # (e) list of sub_images indexes ( 1 or 0 )
        self.create_barriers()


    def create_barriers(self):
        # creates the barrier objects

        # uses position_list to calculate barriers objects centered positions on game screen
        space_btw_barrier = (c.GRID_COLUMNS - c.BARRIERS * c.BARRIERS_WIDTH) // (c.BARRIERS + 1)
        line_pointer = c.BARRIER_LINE * c.GRID_COLUMNS
        start_pos = line_pointer + space_btw_barrier + c.BARRIERS_WIDTH // 2 

        # uses reference image to create initial barriers image file on reference size
        barrier_pix_col = self.resources.canvas_side_pixels // c.GRID_COLUMNS
        self.img_width = int(c.BARRIERS_WIDTH * barrier_pix_col)
        self.img_height = self.img_width  # barrier images will be squared 
        self.resources.barrier_distance = self.img_width // 2

        file_name = base_path + 'barrier.gif'  # this is the reference image for all barriers
        resized_img = resize_image(file_name, (self.img_width, self.img_height))
        self.screen.register_shape(resized_img)

        # create individual barreir objects
        for i in range(c.BARRIERS):
            barrier_data = {}
            barrier = Turtle()
            barrier.penup()
            barrier.ht()
            # populate barrier list with each barrier object and accessory data
            barrier_data['barrier'] = barrier
            # barrier position
            position = self.position_list[start_pos + i * (space_btw_barrier + c.BARRIERS_WIDTH)]
            barrier.goto(position)
            # barrier image
            barrier_image = Image.open(resized_img).copy()  # opens reference image
            file_name = base_path + f'barrier_{i}_img.gif'
            barrier_image.save(file_name, format="GIF")  # saves the copy as a new object 
            self.screen.register_shape(file_name)
            barrier_data['image'] = file_name
            barrier_data['barrier'].shape(file_name)
            # alien sub-images and respective positions
            self.crop_images(barrier_data, resized_img)
            self.resources.barrier_list.append(barrier_data)
        
        self.show_barriers()


    def crop_images(self, barrier_data, image):
        sub_images = []
        sub_img_coords = []
        sub_img_idx = []
        part_width = self.img_width // c.IMG_GRID[0]
        part_height = self.img_height // c.IMG_GRID[1]
        self.resources.barrier_part_distance_x = part_width // 2
        self.resources.barrier_part_distance_y = part_height // 2

        # Crop the image into parts which will be replaced with black images when hit by bombs
        for i in range(c.IMG_GRID[1]):  # Rows
            for j in range(c.IMG_GRID[0]):  # Columns
                left = j * part_width
                top = i * part_height
                right = left + part_width
                bottom = top + part_height

                # Crop and store sub-images
                part = Image.open(image).crop((left, top, right, bottom))
                sub_images.append(part)

                # Calculate center coordinate for this sub-image and stores it on sub_img_coords list
                center_x = barrier_data['barrier'].xcor() - self.img_width // 2 + left + part_width // 2
                center_y = barrier_data['barrier'].ycor() + self.img_height // 2 - top - part_height // 2
                sub_img_coords.append((center_x, center_y))

                # each sub_image will have a corresponding index on another list. 
                # the index value is '1' if the sub_image was not hit by a bomb, or '0' otherwise
                sub_img_idx.append(1)

        # store data
        barrier_data['sub_images'] = sub_images
        barrier_data['sub_img_coords'] = sub_img_coords
        barrier_data['sub_img_idx'] = sub_img_idx

        # creates the black image to replace parts of barrier hit by bombs
        file_name = base_path + f'black_img.gif'
        resized_new_img = resize_image(file_name,(part_width, part_height))
        self.screen.register_shape(resized_new_img)
        self.resources.black_img = Image.open(resized_new_img).copy()
        

    def show_barriers(self):
        for barrier in self.resources.barrier_list:
            barrier['barrier'].st()

