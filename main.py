# Knights Quest 
# Arvin Ullván
# 15-05-2024

# Importerar pygame så att VSCode förstår språket jag skriver i, allting från både sprite.py dokumentet och config.py dokumentet, och system så att allting kan köras korrekt.
import pygame
from sprite import *
from config import *
import sys

#Spelets klass, gör så att spelet körs och så att huvudfunktionerna körs när de ska och att spelet slutar att köras när det ska
class Game:

    #Grund funktionen, här bestäms saker som att pygame startas, bestämmer hur stort fönster man spelar med, font, sätter up fps, och initierar alla spritesheets och bilder som används
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('ARCADECLASSIC.TTF', 32)

        self.character_spritesheet = Spritesheet('img/Crusader.png')
        self.terrain_spritesheet = Spritesheet('img/Full.png')
        self.enemy_spritesheet = Spritesheet('img/Goblin1.png')
        self.void_spritesheet = Spritesheet('img/void.png')
        self.intro_background = pygame.image.load('./img/Castle2.jpg')
        self.gameover_background = pygame.image.load('./img/gameover.jpg')

    #Tar in en lista av arrays som är skapad i Config.py och sedan går igenom alla raderna av arrays och sedan kollumnerna inuti dessa arays och kollar om någon av if satserna stämmer, gör någon av dem det körs klasserna de är länkade till och skapar då en 64 x 64 block av respektive grej. Om ingen av dessa stämmer så körs Ground(). 
    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
                if column == "E":
                    Enemy(self, j, i)
                if column == "V":
                    Void(self, j, i)

    # Sätter igång själva spelet, och gör nya grupp listor av alla sprites och kör map skapar funktionen.
    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.player = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    # Updaterar alla sprites, om de rör på sig eller om de försvinner.
    def update(self):
        self.all_sprites.update()

    #Ritar ut en svart skärm som bakgrund och ritar sedan ut alla sprites i de olika grupp listorna och uådaterar skrämen beroende på antalet frames.
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
            
        pygame.display.update()

    # Håller koll på event, klickar man ner programmet stängs det av, klcikar man på mellanslags kanppen körs attack klassen i Config.py.
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Atk(self, self.player.rect.x, self.player.rect.y)
            
    # Kör funktionerna som ska köras medans spelet är igång.
    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()            

        self.gameover()

        
           

    # Funktion som ska rita upp en game over skärm där man kan trycka på en knapp som startar om spelet. Just nu ritas ingenting upp men knappen går att trycka på för att starta om spelet.
    def gameover(self):

        text = self.font.render('Quest Failed', True, RED)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))
        

        restart_button = Button(560, 200, 100, 50, WHITE, BLACK, 'Retry', 32)

        
        del self.all_sprites
        self.screen.blit(self.gameover_background, (0,0))
            
        self.screen.blit(text, text_rect)
            
        self.screen.blit(restart_button.image, restart_button.rect)
        while self.running:
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.clock.tick(FPS)
            pygame.display.update


    # Ritar upp en skärm innan själva spelet startar där en bild och en titel ritas upp, samt en knapp som man trycker på för att starta spelet. Skriver även in variabler till en knapp som körs i sprite.py dokumentet
    def intro_screen(self):
        intro = True

        title = self.font.render('Knights Quest', True, BLACK)
        title_rect = title.get_rect(x=10, y=10)

        play_button = Button(560, 200, 100, 50, WHITE, BLACK, 'Play', 32)

        while intro: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


# Så att allting körs i rätt ordning och sedan när man stängt av gameover skärmen stängs fönstret ned.
g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.gameover

pygame.quit()
sys.exit()