import constants as c
from turtle import Turtle

class Bombs(Turtle):
    def __init__(self, resources, ship, pos):
        super().__init__()
        self.resources = resources
        self.screen = self.resources.screen
        self.ht()
        self.shape("square")
        self.shapesize(stretch_wid=0.3, stretch_len=1.5)  # Lengthened shape
        self.penup()
        self.goto(pos)
        self.ship = ship  # Type of ship: 'alien' or 'defender'
        self.barrier_hit = None
        self.barrier_idx = None
        self.resources.bomb_distance = 5 # adjusted based on turtle standard sizes
        self.bomb_pause = 0
        # Set specific attributes based on the ship type
        if ship == 'alien':
            self.fillcolor("red")  # Color for alien bombs
            self.setheading(270)  # Point down

        elif ship == 'defender':
            self.fillcolor("blue")  # Color for defender bombs
            self.setheading(90)  # Point up
        else:
            raise ValueError("Invalid ship type. Must be 'alien' or 'defender'.")
        
        # this function searches for barrier parts which will be destroyed by the bomb object
        # if a barrier will be on the way, the function will update the sub-images list so the bomb is promptly updated when hit by the bomb
        # the image is only reconstructed when the bomb hits the barrier
        self.update_barrier_crop_parts(ship)
        # initiate movement
        self.st()


    def update_barrier_crop_parts(self, ship):
        target_barrier = [barrier for barrier in self.resources.barrier_list if abs(self.xcor() - barrier['barrier'].xcor()) < (self.resources.bomb_distance + self.resources.barrier_distance)]
        #  check for active barrier crops (barrier['sub_img_idx'] == 1) and change them to zero if within hit distance
        if target_barrier:
            list_len = len(target_barrier[0]['sub_img_coords'])
            if ship == 'alien':
                list = target_barrier[0]['sub_img_coords']
            elif ship == 'defender':
                list = reversed(target_barrier[0]['sub_img_coords'])
            # if bomb x coordinates equal barrier crop parts coordinates, those crop parts must go black
            # for alien bombs, the list must be iterated from its zero position
            # for defender bombs, the list must be iterated in reverse, and indexes adjusted accordingly
            for idx, item in enumerate(list):
                if ship == 'alien':
                        adj_idx = idx
                elif ship == 'defender':
                    adj_idx = list_len - idx - 1
                if abs(self.xcor() - item[0]) < self.resources.barrier_part_distance_x and target_barrier[0]['sub_img_idx'][adj_idx] == 1:
                    target_barrier[0]['sub_images'][adj_idx] = self.resources.black_img 
                    target_barrier[0]['sub_img_idx'][adj_idx] = 0 
                    self.barrier_hit = target_barrier[0]
                    self.barrier_idx = adj_idx
                    break



    




