#Storleken på spelets fösnter
WIN_WIDTH = 1280
WIN_HEIGHT = 660

#Storleken på urklippningar
TILESIZE = 64
SPRITESIZE = 64

#Hur många gånger per sekund skärmen ska uppdateras
FPS = 60

#De olika lagrerna som saker sak ritas ut på
ATK_LAYER = 5
PLAYER_LAYER = 4
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

#Hur snabbt man rör sig
PLAYER_SPEED = 3
ENEMY_SPEED = 2

#Färger
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Kartan, B = Block, . = Ground, E = Enemy, P = Player, V = Void
tilemap = [
    'BBBBBBBBBBBBBBBBBBBB',
    'B..................B',
    'B..........E.......B',
    'B...BBB......E.....B',
    'B.........P........BVVVVVVVBBBBBBBBBBBBB',
    'B..................BVVVVVVVB...........B',
    'B..................BVVVVVVVB...........B',
    'B.....BBB..........BVVVVVVVB.......E...B',
    'B.......B....E.....BVVVVVVVB....E......B',
    'B...E...B..........BVVVVVVVB...........B',
    'B..................BVVVVVVVB.E..BBBBBBBB',
    'B..................BBBBBBBBB....B',
    'B....E..........E...............B',
    'B..........................E....B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]