import pygame
import os
import random
from pygame.locals import *


class Game():
    def __init__(self):
        # Variaveis
        self.rodando, self.jogando = True, False  # vamos utilizar para o looping
        self.down_key, self.up_key, self.right_key, self.left_key, self.start_key = False, False, False, False, False
        self.shoot = False
        # Tela
        self.DISPLAY_W, self.DISPLAY_H = 1200, 700
        self.tela = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        pygame.display.set_caption("Fisrt game")

        # Taxa de atualização da tela
        self.clock = pygame.time.Clock()
        self.FPS = 30

        # Font
        pygame.font.init()
        self.fonte = pygame.font.Font('assets/fonte/gameovercre1.ttf', 40)

        # Carregando imagem dos INIMIGOS
        self.INIMIGO_VERMELHO = pygame.image.load(
            os.path.join("assets", "pixel_ship_red_small.png"))
        self.INIMIGO_VERDE = pygame.image.load(
            os.path.join("assets", "pixel_ship_green_small.png"))
        self.INIMIGO_AZUL = pygame.image.load(
            os.path.join("assets", "pixel_ship_blue_small.png"))
        # Carregando nave do PLAYER
        self.YELLOW_SPACE_SHIP = pygame.image.load(
            os.path.join("assets", "player.png"))
        # Carregando os LASERS
        self.RED_LASER = pygame.image.load(
            os.path.join("assets", "pixel_laser_red.png"))
        self.YELLOW_LASER = pygame.image.load(
            os.path.join("assets", "pixel_laser_yellow.png"))
        self.GREEN_LASER = pygame.image.load(
            os.path.join("assets", "pixel_laser_green.png"))
        self.BLUE_LASER = pygame.image.load(
            os.path.join("assets", "pixel_laser_blue.png"))
        # Carregando background
        self.BACKGROUND = pygame.transform.scale(pygame.image.load(
            os.path.join("assets", "background1.png")), (self.DISPLAY_W, self.DISPLAY_H))

        # Status de jogo
        self.nivel = 0
        self.vida = 5
        self.velocidade_player = 10
        self.inimigos_em_tela = []
        self.inimigos_por_fase = 5
        self.inimigo_vel = 1  
        self.laser_vel = 5

        # Posição do jogador
        self.pos_jogador_x = 40
        self.pos_jogador_y = 320
        

    def gameLoop(self):

        while self.jogando:
            self.clock.tick(self.FPS)

            self.drawWindow()
            
            self.checkEvents()

            # if self.start_key:
            #     self.jogando = False
            # if self.shoot:
            #     self.jogador.shoot()

            # Movimentação do jogador
            if self.up_key: # para cima
                self.pos_jogador_y -= self.velocidade_player
            if self.down_key: # para baixo
                self.pos_jogador_y += self.velocidade_player
            if self.right_key: # para direita
                self.pos_jogador_x += self.velocidade_player
            if self.left_key: # para esquerda
                self.pos_jogador_x -= self.velocidade_player
            
            # Atirando
            if self.shoot:
                print("Atirando")
                # self.jogador.shoot()]
        
            # self.jogador.move_lasers(self.laser_vel, self.tela)

            self.resetKeys()

    def drawWindow(self):
        # Objeto da nave do jogador
        self.jogador = self.Jogador(self.pos_jogador_x, self.pos_jogador_y)

        # Background
        self.tela.blit(self.BACKGROUND, (0, 0))


        # Desenhando o overlay do jogo
        vida_label = self.fonte.render(
            f"Vidas: {self.vida}", 1, (225, 225, 225))
        nivel_label = self.fonte.render(
            f"Nivel: {self.nivel}", 1, (225, 225, 225))


        if len(self.inimigos_em_tela) == 0:
            self.nivel += 1
            self.inimigo_vel += 1
            self.inimigos_por_fase += 5
            
            for i in range(self.inimigos_por_fase):
                # Nascimento aleatorio dos inimigos
                color_enemy = random.choice(["red", "blue", "green"])
                range_de_nascimento_x = random.randrange((self.DISPLAY_W + 50 ), 2400)
                range_de_nascimento_y = random.randrange(50, (self.DISPLAY_H - 50))
                inimigos= Game.Inimigos(id= i, x= range_de_nascimento_x, y= range_de_nascimento_y, color= color_enemy)
                self.inimigos_em_tela.append(inimigos)
        
        for inimigo in self.inimigos_em_tela[:]:
            inimigo.move(self.inimigo_vel)

            if inimigo.x + inimigo.get_width() < 0:
                self.vida -= 1
                self.inimigos_em_tela.remove(inimigo)

        for inimigos in self.inimigos_em_tela:
            inimigos.draw(self.tela)
        
        self.jogador.draw(self.tela)  # Coloca o jogador na tela

        self.tela.blit(vida_label, (10, 10))
        self.tela.blit(nivel_label, (self.DISPLAY_W -
                       nivel_label.get_width() - 10, 10))

        pygame.display.update()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rodando, self.jogando = False, False

        key = pygame.key.get_pressed()

        if key[pygame.K_a]: # Esquerda 
            self.left_key = True
        if key[pygame.K_d]: # Direita
            self.right_key = True
        if key[pygame.K_w]: # Cima
            self.up_key = True
        if key[pygame.K_s]: # Baixo
            self.down_key = True
        if key[pygame.K_SPACE]:
            self.shoot = True

    def resetKeys(self):
        self.down_key, self.up_key, self.right_key, self.left_key, self.start_key = False, False, False, False, False
        self.shoot = False
    

    class Players():
        def __init__(self, x, y, vida=100):
            self.x, self.y = x, y
            self.vida = vida
            self.lasers_em_tela = []
            # Imagens do player/inimigo em questão
            self.player_img = None
            self.player_laser = None
            # Tempo em que os inimigos aparecem na tela
            self.COOLDOWN = 30
            self.cooldown_counter = 0

        def draw(self, tela):
            tela.blit(self.player_img, (self.x, self.y))

            for laser in self.lasers_em_tela:
                laser.draw(tela)

        # def shoot(self):
        #     if self.cooldown_counter == 0:
        #         laser = Game.Laser(self.x, self.y, self.player_laser)
        #         self.lasers_em_tela.append(laser)
        #         self.cooldown_counter = 1

        # def shootCooldown(self):
        #     if self.cooldown_counter >= self.COOLDOWN:
        #         self.cooldown_counter = 0
        #     elif self.cooldown_counter > 0:
        #         self.cooldown_counter += 1

        # def move_lasers(self, vel, tela):
        #     self.shootCooldown()
        #     for laser in self.lasers_em_tela:
        #         laser.move(vel)
        #         laser.draw(tela)

        def get_width(self):
            return self.player_img.get_width()

        def get_height(self):
            return self.player_img.get_height()

    # class Laser():
    #     def __init__(self, x, y, img):
    #         self.x = x
    #         self.y = y
    #         self.img = img
    #         self.mask = pygame.mask.from_surface(self.img)

    #     def draw(self, tela):
    #         tela.blit(self.img, (self.x, self.y))

    #     def move(self, vel):
    #         self.x -= vel

    class Jogador(Players):
        def __init__(self, x, y, vida=100):
            self.vida = vida
            super().__init__(x, y, self.vida)

            img_player = Game()
            self.player_img = img_player.YELLOW_SPACE_SHIP
            self.player_laser = img_player.YELLOW_LASER
            self.mask = pygame.mask.from_surface(self.player_img)
            self.max_life = vida

        def lifebar(self, tela):
            vida = self.vida
            max_life = self.max_life
            pos_vida_vermelha = (
                self.x, self.y + self.player_img.get_height() + 10, self.player_img.get_width(), 10)
            pos_vida_verde = (self.x, self.y + self.player_img.get_height() + 10,
                              self.player_img.get_width() * (vida/max_life), 10)

            pygame.draw.rect(tela, (255, 0, 0), pos_vida_vermelha)
            pygame.draw.rect(tela, (0, 255, 0), pos_vida_verde)

        def draw(self, tela):
            super().draw(tela=tela)
            self.lifebar(tela=tela)

    class Inimigos(Players):
        def __init__(self,id , x, y, color, vida=100):
            super().__init__(x, y, vida=vida)
            
            # Imagens dos inimigos
            imgs = Game()
            ENEMY_COLOR = {
                "red" : (imgs.INIMIGO_VERMELHO, imgs.RED_LASER),
                "green" : (imgs.INIMIGO_VERDE, imgs.GREEN_LASER),
                "blue" : (imgs.INIMIGO_AZUL, imgs.BLUE_LASER) 
            }

            self.player_img, self.player_laser = ENEMY_COLOR[color]
            self.mask = pygame.mask.from_surface(self.player_img)       

        def move(self, vel):
            self.x -= vel
        
            
