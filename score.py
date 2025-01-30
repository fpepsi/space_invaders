import constants as c
from turtle import Turtle

class GameVariables():
    def __init__(self, resources):
        self.resources = resources
        self.score = Turtle()
        self.life_display = Turtle()

        # initialize scoreboard
        self.score.ht()
        self.score.penup()
        self.score.color('white')
        self.score.goto(self.resources.position_list[1])

        # screen bottom line
        position = c.CANVAS_LINE * c.GRID_COLUMNS
        x = self.resources.position_list[position][0]
        y = self.resources.position_list[position][1] - self.resources.canvas_side_pixels / c.GRID_LINES // 2
        line = Turtle()
        line.penup()
        line.ht()
        line.color('blue')
        line.goto(x, y)
        line.pendown()
        line.fd(self.resources.canvas_side_pixels)

        # initialize life display
        initial_pos = c.LIFES_LINE * c.GRID_COLUMNS + c.DEFENDER_WIDTH
        for i in range(self.resources.lives - 1):
            life = Turtle()
            life.ht()
            life.penup()
            shape = self.resources.defender.shape()
            life.shape(shape)
            position = initial_pos + i * 2 * c.DEFENDER_WIDTH
            life.goto( self.resources.position_list[position])
            life.st()
            self.resources.lives_list.append(life)

    
    def update_score(self):
        self.score.clear()
        self.text = f'Score = {self.resources.points} points'
        self.score.write(self.text, align='center', font=('Arial', 18, 'bold'))

    



        