import os
import bombs as b
import constants as c
from turtle import Turtle
from random import choice
from shared import resize_image

# variable holder work folder for image files management
base_path = os.path.dirname(os.path.abspath(__file__)) + c.IMG_DIR

class AlienManager():
    # alien attributes
    aliens_per_line = 11  # number of aliens per line. this number will be used together with alien elements 'number' to define number of alien lines
    alien_elements = {
        'A1': {'number': 11, 'points': 30, 'shape': ['ika.gif', 'ikab.gif']},
        'A2': {'number': 22, 'points': 20, 'shape': ['kani.gif', 'kanib.gif']},
        'A3': {'number': 22, 'points': 10, 'shape': ['kura.gif', 'kurab.gif']}
    }   # shows the population number of each type of alien, their points worth, and their image file names
        # 'number' must be a multiple of aliens per line
    
    def __init__(self, resources):
        self.resources = resources
        self.screen = resources.screen
        self.leftmost_screen_coord = None
        self.rightmost_screen_coord = None
        self.direction = 1           # 1 aliens move right, -1 move left
        self.screen_edge = False
        self.initial_aliens = 0
        self.active_aliens = int

        # initialize aliens grid
        self.initialize_grid()


    def initialize_grid(self):
        # setup alien image size
        alien_pix_col = self.resources.canvas_side_pixels // c.GRID_COLUMNS
        alien_pix_line = self.resources.canvas_side_pixels // c.GRID_LINES
        img_width = int(c.ALIEN_WIDTH * alien_pix_col)
        img_height = img_width  # alien images will be squared 
        self.resources.alien_distance = img_width // 2 # distance be used to detect collision

        # dinamically fill out position list with all possible coordinates and sets 
        initial_x =  (-c.GRID_COLUMNS // 2 + c.SPACE_WIDTH) * alien_pix_col
        initial_y = (c.GRID_LINES // 2) * alien_pix_line - alien_pix_line
        for line in range(0, c.GRID_LINES):
            for column in range(0, c.GRID_COLUMNS):
                x = initial_x + column * alien_pix_col
                y = initial_y - line * alien_pix_line
                self.resources.position_list.append((x, y))
        # records the screen sides x coordinates 
        self.leftmost_screen_coord = self.resources.position_list[0][0]
        self.rightmost_screen_coord = self.resources.position_list[c.GRID_COLUMNS - c.ALIEN_WIDTH - c.SPACE_WIDTH][0]

        # populate the aliens lists 0 and 1 with turtle objects. The lists differ by each alien's shape
        for key, value in self.alien_elements.items():
            lines = value['number'] // self.aliens_per_line
            for i in range(lines):
                for j in range(0, self.aliens_per_line):
                    self.resources.alien_points.append(value['points'])
                    self.initial_aliens += 1
                    for k in range(0, 2):
                        alien = Turtle()
                        alien.ht()
                        alien.penup()
                        file_name = base_path + value['shape'][k]
                        img_file = resize_image(file_name, (img_width, img_height))
                        self.screen.register_shape(img_file)
                        alien.shape(img_file)
                        self.resources.alien_list[k].append(alien)
        
        self.show_aliens()
        self.alien_shoot()
        
        self.acceleration = (c.ALIEN_FAST - c.ALIEN_SLOW) // (self.initial_aliens - 1)

        self.screen.update()
        

    def alien_move(self):
        # each time this function is called, it advances the pointer to position_list so all aliens move 1 position
        # the pointer will advance a full line and change direction any time the outer aliens reach a screen side
        # test if aliens reached a side
        if self.resources.pointer % 2 == 0:
            visible_aliens = self.resources.alien_list[0]
        else:
            visible_aliens = self.resources.alien_list[1]
        if self.screen_edge:
            # this flag is originally set to False as aliens should move on a line direction
            # later on, this function will check when an alien reaches an edge, and if so the alien will move down 2 lines and the flag will change
            # the chang inflag ensures the alien goes back to a lateral movement on the next round
            self.resources.pointer += self.direction
            self.screen_edge = False
        else:
            for alien in visible_aliens:
                # check if any alien is at edge position
                if alien != None:
                    if alien.xcor() == self.leftmost_screen_coord or alien.xcor() == self.rightmost_screen_coord:
                        # if any alien at the edges, a flag will be set and move pattern will change
                        self.screen_edge = True
                        break       
            if self.screen_edge:
                # when an alien reaches the edges, the pointer advances to the following line and direction changes
                # self.screen_edge remains unchanged so on the next round the alien moves to the side instead of lower
                self.resources.pointer += c.GRID_COLUMNS
                self.direction *= -1
            else:
                # if not, pointer continues advancing one way
                self.resources.pointer += self.direction

        self.show_aliens()
        alien_speed = c.ALIEN_SLOW + self.resources.alien_list[0].count(None) * self.acceleration
        if not self.resources.stop:
            self.screen.ontimer(self.alien_move, alien_speed)   


    def show_aliens(self):
        # each alien has 2 positions which images are stored in 2 lists inside alien_list
        # alien_list lists alternate visibility in order to show animation
        # aliens from the currently visible alien list will be displayed one position ahead from the ones in the previous visible list
        # the pointer points to the position of the top-left most alien in position_list 
        if self.resources.pointer % 2 == 0:
            visible_aliens = self.resources.alien_list[0]
            invisible_aliens = self.resources.alien_list[1]
        else:
            visible_aliens = self.resources.alien_list[1]
            invisible_aliens = self.resources.alien_list[0]

        pos = self.resources.pointer
        i = 0
        step = c.ALIEN_WIDTH + c.SPACE_WIDTH

        for alien in visible_aliens:
            if alien != None:
                alien.goto(self.resources.position_list[pos + i * step])
                alien.st()
            # logic to map alien_list elements 
            if i == self.aliens_per_line - 1:
                pos += c.LINES_PER_ALIEN * c.GRID_COLUMNS  # skips one line so an alien fits 2 lines
                i = 0
            else:
                i += 1

        for alien in invisible_aliens:
            if alien != None:
                alien.ht() 


    def alien_shoot(self):
        # randomly selects an alien which position is used to shoot
        if self.resources.pointer % 2 == 0:
            visible_aliens = self.resources.alien_list[0]
        else:
            visible_aliens = self.resources.alien_list[1]
        if len(self.resources.alien_bomb_list) > 3:
            pass
        else:
            chosen_alien = False
            while not chosen_alien:
                attack_alien = choice(visible_aliens)
                if attack_alien != None:
                    chosen_alien = True
            new_bomb = b.Bombs(self.resources, 'alien', attack_alien.pos())
            self.resources.alien_bomb_list.append(new_bomb)
        if not self.resources.stop:
            self.screen.ontimer(self.alien_shoot, c.RELOAD_INTERVAL)      


      
            

