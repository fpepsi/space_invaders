IMG_DIR = '/images/' # directory holding game images
SCREEN_FREQUENCY = 20 # miliseconds between screen updates

# game gridline and element dimensions
GRID_LINES = 22
GRID_COLUMNS = 75

# each barrier is composed of an image grid which will be dinamically populated as the barriers are hit by aliens' shots
BARRIERS = 4    # number of barriers
BARRIERS_WIDTH = 8  # number of grid_columns occupied by barriers
BARRIER_LINE = 17   # line where barriers should be placed
IMG_GRID = (3, 3)   # each barrier object image will be split equally by a grid

 # alien sizes relative to grid - multiply these number by the number of pixels per column or line calculated below
# each alien + space occupies 5 grid_columns. 11 aliens occupy 55 grid_columns and the remaining 20 are space available to move 1 by 1
LINES_PER_ALIEN = 2 # number of lines occupied by an alien cell (image + spacing)
ALIEN_WIDTH = 3 # number of grid_columns occupied by an alien, including padding
SPACE_WIDTH = 1 # number of grid columns between aliens
ALIEN_SLOW = 750 # miliseconds between alien moves
ALIEN_FAST = 100 # miliseconds between alien moves

BOMB_SPEED = 8 # pixels per move
RELOAD_INTERVAL = 2000 # milisseconds

DEFENDER_WIDTH = 3 # defender width in screen columns units
DEFENDER_LINE = 19 # line where defender should be placed

CANVAS_LINE = 19
LIFES_LINE = 20