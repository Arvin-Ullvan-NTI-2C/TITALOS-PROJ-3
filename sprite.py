
# Importerar pygame så programemt vet vilket språk som används, allting från config.py dokumentet, matte och random modulen så att programmet kan göra funktioner som finns i respektive modul
import pygame
from config import *
import math
import random 

# Klass som håller koll på alla mins spritesheets, så att de kan klippas ut och ritas ut på skärmen.
class Spritesheet:
    # Gör så att den tar rätt fil och konverterar det till ett ytkompatibelt format för att kunna skriva ut det snabbare
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    # Skriver en yta från spritesheeten som man lagt in som man bestämt koordinaterna på sheeten och höjd och längd på klippningen, dessa skrivs sedan ut, och tar bort det svarta tomrum som skapas runt om själva karaktären
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)

        return sprite
    
    # Samma som ovanstående men tar inte bort det svarta tomrummet då denna är tillför att skapa "void" boxar som är utanför borderserna men innuti arrayerna som skapar kartan.
    def get_sprite_void(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        return sprite

    # Samma som get_sprite() men har använt en sepparat för attack för att kunna se dens hitbox som är annorlunda än karaktärens.
    def get_sprite_atk(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit (self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)

        return sprite

# Håller koll på allting angående själva spelaren, som position, om den lever, eller animation.
class Player(pygame.sprite.Sprite):

    # Skapar alla grund variabler så som start position, vilka sprite gruppe den är del av, vilket lager den ska ritas ut på, vilket spritesheet som ska användas, hitboxens position, vilka grupper av sprites den är med i, riktningen den kollar åt.
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * SPRITESIZE
        self.y = y * SPRITESIZE
        self.width = SPRITESIZE
        self.height = SPRITESIZE

        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (16, 16))


        self.rect = self.image.get_rect()
        self.rect.center = WIN_WIDTH/2, WIN_HEIGHT/2
        self.rect.x = self.x
        self.rect.y = self.y

    # Håller koll så att saker som, position, animationer, kollision med fiende, och kollision med block updateras hela tiden, så att om en ändring händer händer det direkt. Till exempel om karaktären tar ett steg åt höger ska en ny sprite ritas ut på den positionen.
    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    # Gör så att positionen ändras beroende på vilken knapp som trycks, gör även så att alla sprites förflyttas i motsatt riktning vilket gör så att kameran följer karaktären. Sätter även vilken riktning som karaktären går mot, upp, ner , höger, vänster.
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
        if keys[pygame.K_a]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_d]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_w]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_s]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
        
    # Kollar om karaktären kolliderar med en fiende rektangel, och då försvinner karaktären och spelet slutar.
    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits: 
            self.kill()
            self.game.playing = False

    # Kollar om karaktären kolliderar med borders, om den gör det ska den inte kunna gå längre åt det hållet, gör också så att kameran stannar om karaktären stannar.
    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED
                    self.rect.y = hits[0].rect.bottom

    #Gör en array av de urklippta bilderna till animationer och spelar animationer till korresponderande riktning av karaktären
    def animate(self):
        up_animations = [self.game.character_spritesheet.get_sprite(0, 512, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(64, 512, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(128, 512, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(192, 512, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(256, 512, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(320, 512, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(384, 512, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(448, 512, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(512, 512, self.width, self.height)]
        
        left_animations=[self.game.character_spritesheet.get_sprite(0, 576, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(64, 576, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(128, 576, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(192, 576, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(256, 576, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(320, 576, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(384, 576, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(448, 576, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(512, 576, self.width, self.height)]
        
        down_animations = [self.game.character_spritesheet.get_sprite(0, 640, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(64, 640, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(128, 640, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(192, 640, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(256, 640, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(320, 640, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(384, 640, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(448, 640, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(512, 640, self.width, self.height)]

        right_animations =[self.game.character_spritesheet.get_sprite(0, 704, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(64, 704, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(128, 704, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(192, 704, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(256, 704, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(320, 704, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(384, 704, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(448, 704, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(512, 704, self.width, self.height),]

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 640, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= 9:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 512, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= 9:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 704, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= 9:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 576, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= 9:
                    self.animation_loop = 1

# Klassen för fienderna, håller koll på position, animationer, och om den kolliderar med något.
class Enemy(pygame.sprite.Sprite):

    #Initialiserar alla variabler som behövs, såsom lagret den ska ritas ut på, storleken på urklippningen, hur långt den får gå, vilka grupper av sprites den är med i, riktningen den kollar åt.
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * SPRITESIZE
        self.y = y * SPRITESIZE
        self.width = SPRITESIZE
        self.height = SPRITESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right', 'up', 'down'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(30, 60)

        self.image = self.game.enemy_spritesheet.get_sprite(38, 1640, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    # Håller koll så att saker som, position, animationer, och kollision med block updateras hela tiden, så att om en ändring händer händer det direkt. Till exempel om den tar ett steg åt höger ska då en ny sprite skrivas ut på den positionen.
    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        

        self.x_change = 0
        self.y_change = 0
    
    #Kollar om den kolliderar med ett block, gör den det ska den stanna.
    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
    
    # Håller koll på position och kollar vilken riktning den går åt, slumpar även vilken riktning den ska ta efter att den gått dens satta längd åt ett håll.  
    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['right', 'up', 'down', 'left'])

        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['left', 'up', 'down', 'right'])
        
        if self.facing == 'down':
            self.y_change += ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['left', 'up', 'right', 'down'])
        
        if self.facing == 'up':
            self.y_change -= ENEMY_SPEED 
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['right', 'left', 'down', 'up'])
    
    #Gör en array av de urklippta bilderna till animationer och spelar animationer till korresponderande riktning av karaktären
    def animate(self):
        up_animations = [self.game.enemy_spritesheet.get_sprite(32, 1376, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(160, 1376, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(288, 1376, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(416, 1376, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(544, 1376, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(672, 1376, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(800, 1376, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(928, 1376, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(1056, 1376, self.width, self.height)]
        
        left_animations=[self.game.enemy_spritesheet.get_sprite(32, 1504, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(160, 1504, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(288, 1504, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(416, 1504, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(544, 1504, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(672, 1504, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(800, 1504, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(928, 1504, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(1056, 1504, self.width, self.height)]
        
        down_animations = [self.game.enemy_spritesheet.get_sprite(32, 1632, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(160, 1632, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(288, 1632, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(416, 1632, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(544, 1632, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(672, 1632, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(800, 1632, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(928, 1632, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(1056, 1632, self.width, self.height)]

        right_animations =[self.game.enemy_spritesheet.get_sprite(32, 1760, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(160, 1760, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(288, 1760, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(416, 1760, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(544, 1760, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(672, 1760, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(800, 1760, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(928, 1760, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(1056, 1760, self.width, self.height)]
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(32, 1632, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= 9:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(32, 1376, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= 9:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(32, 1760, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= 9:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(32, 1504, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= 9:
                    self.animation_loop = 1


# Håller koll på vart block ska placeras
class Block(pygame.sprite.Sprite):

    #Kollar positionen, lagret den ritas ut på, och storleken på blocken.
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(32, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

#Samma som Block klassen
class Void(pygame.sprite.Sprite):
    #Samma som Block klassen
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.void_spritesheet.get_sprite_void(190, 120, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# Samma som Block klassen
class Ground(pygame.sprite.Sprite):
    #Samma som Block klassen
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64, 64, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x 
        self.rect.y = self.y

# ritar ut en knapp och kollar om den blir tryckt på
class Button:

    #Initsialerar variabler som, vilken font, vad som ska stå, position, storlek, och färg.
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('ARCADECLASSIC.TTF', fontsize)
        self.content = content
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x 
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center = (self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    #Kollar om muspekaren är på knappens hitbox och sedan om man trycker så kör den spelet.
    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

#Håller koll på allting som har med attacken att göra, som position, animation, hitbox, kollision
class Atk(pygame.sprite.Sprite):

    #Initsialiserar alla variabler så som, position, lager sm den ska ritas ut på, vilka grupper av sprites den är med i, riktningen den kollar åt.
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ATK_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = SPRITESIZE
        self.height = SPRITESIZE
        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'
        self.animation_loop = 0
        self.enemies = 10
        self.image = self.game.character_spritesheet.get_sprite_atk(64, 1409, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x - 32
        self.rect.y = self.y - 16

        

    # updaterar all information i funktionerna som körs
    def update(self):
        self.animate()
        self.collide()

    #Kollar om attack animationen kolliderar med en fiende, om den gör det ska fienden tas bort
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)
        
    #Klipper ut bilder och lägger till i arrayer som sedan körs när spelaren kollar mot korresponderande riktning, tar sedan bort spriten när animationen körts.
    def animate(self):
        direction = self.game.player.facing

        up_animations = [self.game.character_spritesheet.get_sprite_atk(32, 1392, 144, 144),
                         self.game.character_spritesheet.get_sprite_atk(224, 1392, 144, 144),
                         self.game.character_spritesheet.get_sprite_atk(416, 1392, 144, 144),
                         self.game.character_spritesheet.get_sprite_atk(608, 1392, 144, 144),
                         self.game.character_spritesheet.get_sprite_atk(800, 1392, 144, 144),
                         self.game.character_spritesheet.get_sprite_atk(992, 1392, 144, 144)]
        
        left_animations=[self.game.character_spritesheet.get_sprite_atk(32, 1584, 160, 144),
                         self.game.character_spritesheet.get_sprite_atk(224, 1584, 160, 144),
                         self.game.character_spritesheet.get_sprite_atk(416, 1584, 160, 144),
                         self.game.character_spritesheet.get_sprite_atk(608, 1584, 160, 144),
                         self.game.character_spritesheet.get_sprite_atk(800, 1584, 160, 144),
                         self.game.character_spritesheet.get_sprite_atk(992, 1584, 160, 144)]
        
        down_animations = [self.game.character_spritesheet.get_sprite_atk(32, 1776, 144, 144),
                           self.game.character_spritesheet.get_sprite_atk(224, 1776, 144, 144),
                           self.game.character_spritesheet.get_sprite_atk(416, 1776, 144, 144),
                           self.game.character_spritesheet.get_sprite_atk(608, 1776, 144, 144),
                           self.game.character_spritesheet.get_sprite_atk(800, 1776, 144, 144),
                           self.game.character_spritesheet.get_sprite_atk(992, 1776, 144, 144)]

        right_animations =[self.game.character_spritesheet.get_sprite_atk(32, 1968, 144, 144),
                           self.game.character_spritesheet.get_sprite_atk(224, 1968, 144, 144),
                           self.game.character_spritesheet.get_sprite_atk(416, 1968, 144, 144),
                           self.game.character_spritesheet.get_sprite_atk(608, 1968, 144, 144),
                           self.game.character_spritesheet.get_sprite_atk(800, 1968, 144, 144),
                           self.game.character_spritesheet.get_sprite_atk(992, 1968, 144, 144)]

        if direction == 'up':
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.2
            if self.animation_loop >= 6:
                self.kill()
        if direction == 'down':
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.2
            if self.animation_loop >= 6:
                self.kill()
        if direction == 'left':
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.2
            if self.animation_loop >= 6:
                self.kill()
        if direction == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.2
            if self.animation_loop >= 6:
                self.kill()