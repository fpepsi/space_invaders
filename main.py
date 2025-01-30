from shared import setup_folder, SharedScreen
from aliens import AlienManager
from barriers import Barriers
from defender import Defender
from score import GameVariables
import turtle
from constants import SCREEN_FREQUENCY


class SpaceInvaders():
    def __init__(self):
        # initialize game
        setup_folder()
        self.resources = SharedScreen()
        self.alien = AlienManager(self.resources)
        self.barrier = Barriers(self.resources)      
        self.defender = Defender(self.resources)  
        self.score = GameVariables(self.resources) 
        self.barrier.show_barriers()
        # initiates the game screen and score refresh loops
        self.update_screen()
        self.alien.alien_move()
        self.resources.check_bomb_hit()


    def update_screen(self):
        self.score.update_score()
        self.resources.screen.update()
        self.resources.screen.ontimer(self.update_screen, SCREEN_FREQUENCY)
        
        
# Run the game
if __name__ == "__main__":
    SI = SpaceInvaders()


turtle.done()