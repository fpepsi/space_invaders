import os
import constants as c
import bombs as b
from turtle import Turtle
from shared import resize_image

# variable holder work folder for image files management
base_path = os.path.dirname(os.path.abspath(__file__)) + c.IMG_DIR

class Defender(Turtle):
    def __init__(self, resources):
        super().__init__()
        self.resources = resources
        self.position_list = self.resources.position_list # holds all positions in the game grid
        self.ht()
        self.penup()

        # dinamically initialized attributes
        # defender shape
        file_name = base_path + 'defender.gif'
        defender_pix_col = self.resources.canvas_side_pixels // c.GRID_COLUMNS * 0.8
        img_width = int(c.DEFENDER_WIDTH * defender_pix_col)
        img_height = img_width  # defender image will be squared
        img_file = resize_image(file_name, (img_width, img_height))
        self.screen.register_shape(img_file)
        self.shape(img_file)
        # share defender distance with SharedScreen
        self.resources.defender_distance = img_width // 2 # distance be used to detect collision
        #defender initial position
        line_pointer = c.DEFENDER_LINE * c.GRID_COLUMNS
        start_pos = line_pointer + c.GRID_COLUMNS // 2
        self.initial_position = self.position_list[start_pos]
        self.goto(self.initial_position)
        self.st()

        # determines mouse gap and binds mouse to defender
        self.mouse_gap = self.resources.screen.window_width() // 2
        self.left_scr_limit = (- self.resources.canvas_side_pixels + img_width) // 2
        self.right_scr_limit = (self.resources.canvas_side_pixels - img_width) // 2
        self.screen.cv.bind('<Motion>', self.defender_move)
        self.screen.cv.bind('<Button-1>', self.defender_shoot)

        # shares defender object with "SharedScreen" object
        self.resources.defender = self


    def defender_move(self, event):
        mouse_adj_x = event.x - self.mouse_gap
        if mouse_adj_x < self.left_scr_limit:
            x = self.left_scr_limit
        elif mouse_adj_x > self.right_scr_limit:
            x = self.right_scr_limit
        else:
            x = mouse_adj_x
        self.goto(x, self.initial_position[1])

    
    def defender_shoot(self, event):
        new_bomb = b.Bombs(self.resources, 'defender', self.pos())
        self.resources.defender_bomb_list.append(new_bomb)








