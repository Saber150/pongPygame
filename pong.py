import pygame as pyg, sys, random

# Classe para objetos player e Oponente
class Jogador:
    def __init__(self, speed, forma):
        self.speed = speed
        self.forma = forma
    def player_animation(self):
        self.forma.y += self.speed
        if self.forma.top <= 0:
            self.forma.top = 0
        if self.forma.bottom >= altura_tela:
            self.forma.bottom = altura_tela

    def oponente_ai(self):
        if self.forma.top < ball.forma.y:
            self.forma.top += self.speed
        if self.forma.bottom > ball.forma.y:
            self.forma.bottom -= self.speed
        if self.forma.top <= 10 or self.forma.bottom >= altura_tela:
            self.speed *= -1

# Fim da classe Jogador.

# Classe para o objeto ball
class Bola:
    def __init__(self, speed_x, speed_y, forma):
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.forma = forma
    
    def ball_restart(self):
        # Centraliza a bola
        self.forma.center = (largura_tela/2, altura_tela/2)
        # Decide se a direcao de saida de forma aleatoria
        self.speed_y *= random.choice((1,-1))
        self.speed_x *= random.choice((1,-1))

    def movimentoBola(self):

        self.forma.x += self.speed_x
        self.forma.y += self.speed_y

        # Direcoes da bola, se acertar o topo inverte o valor de velocidade em y
        if self.forma.top <= 0 or self.forma.bottom >= altura_tela:
            self.speed_y *= -1

        # Se acertar a lateral esquerda ele reinicia a bola para o centro
        if self.forma.left <= 0 or self.forma.right >= largura_tela:
            self.ball_restart()

        # Se entrar em colisao com o player ou com o oponente inverte a velocidade em x
        if self.forma.colliderect(player.forma) or self.forma.colliderect(oponente.forma):
            self.speed_x *= -1

# Fim da classe Bola

# Setup
pyg.init()
clock = pyg.time.Clock()

# Criando a janela com pygame
# Proporcoes, largura e altura

largura_tela = 1280
altura_tela = 720

# Tela é criada
tela = pyg.display.set_mode((largura_tela, altura_tela))

# Adiciona o nome "Pong" a tela
pyg.display.set_caption('Pong')

direcao_x = random.choice((7,-7))
direcao_y = random.choice((7,-7))

# Objetos, self, Jogador
ball = Bola(direcao_x, direcao_y, pyg.Rect(largura_tela/2 - 10, altura_tela/2 - 10, 20, 20))
player = Jogador(0, pyg.Rect(largura_tela - 20, altura_tela/2 - 70, 10, 140))
oponente = Jogador(7, pyg.Rect(10, altura_tela/2 - 70, 10, 140))

bg_color = pyg.Color('grey12')
light_grey = (200, 200, 200)

while True:
    # Entrada para encerrar o programa caso fechar a janela
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            sys.exit()
        
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_ESCAPE:
                pyg.quit()
                sys.exit()

        if event.type == pyg.KEYDOWN:

            # Movimentacao Player
            if event.key == pyg.K_DOWN:
                player.speed += 7
            if event.key == pyg.K_UP:
                player.speed -= 7

        if event.type == pyg.KEYUP:

            # Movimentacao Player
            if event.key == pyg.K_DOWN:
                player.speed -= 7
            if event.key == pyg.K_UP:
                player.speed += 7

    player.player_animation()
    oponente.oponente_ai()

    ball.movimentoBola()
    
    # Visuals
    tela.fill(bg_color)
    pyg.draw.rect(tela, light_grey, player.forma)
    pyg.draw.rect(tela, light_grey, oponente.forma)
    pyg.draw.ellipse(tela, light_grey, ball.forma)
    pyg.draw.aaline(tela, light_grey, (largura_tela/2,0), (largura_tela/2, altura_tela))

    # Atualizando a janela a 60 frames por segundo
    pyg.display.flip()
    clock.tick(60)

