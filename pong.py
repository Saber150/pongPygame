import pygame as pyg, sys, random

# Classe para objetos player e Oponente
class Mob:
    def __init__(self, speed, forma):
        self.speed = speed
        self.forma = forma
# Fim da classe Jogador.

class Player(Mob):
    def __init__(self, speed, forma, score):
        super().__init__(speed, forma)
        self.score = score

    def player_animation(self):
        self.forma.y += self.speed
        if self.forma.top <= 0:
            self.forma.top = 0
        if self.forma.bottom >= altura_tela:
            self.forma.bottom = altura_tela

# Fim da classe Player

class Oponente(Mob):
    
    def __init__(self, speed, forma, score):
        super().__init__(speed, forma)
        self.score = score
    
    def oponente_ai(self):
        if self.forma.top < ball.forma.y:
            self.forma.top += self.speed
        if self.forma.bottom > ball.forma.y:
            self.forma.bottom -= self.speed
        if self.forma.top <= 10 or self.forma.bottom >= altura_tela:
            self.speed *= -1

#Fim da classe Oponente

# Classe para o objeto ball
class Bola(Mob):
    def __init__(self, speed_x, speed_y, forma):
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.forma = forma
    
    def ball_restart(self, score_time):
        # Centraliza a bola
        self.forma.center = (largura_tela/2, altura_tela/2)

        tempo_atual = pyg.time.get_ticks()  

        tempo = tempo_atual - score_time

        hud = game_font.render("Inicio em: ", True, light_grey)
        tela.blit(hud, ((largura_tela/2 -80, altura_tela / 2 + 60)))

        if tempo < 1000:
            contador = game_font.render("3", True, light_grey)
            tela.blit(contador, ((largura_tela/2 + 80, altura_tela /2 + 60)))
        
        if tempo < 2000 and tempo > 1000:
            contador = game_font.render("2", True, light_grey)
            tela.blit(contador, ((largura_tela/2 + 80, altura_tela /2 + 60)))
        
        if tempo < 3000 and tempo > 2000:
            contador = game_font.render("1", True, light_grey)
            tela.blit(contador, ((largura_tela/2 + 80, altura_tela /2 + 60)))

        if tempo_atual - score_time < 3000:
            self.speed_x, self.speed_y = 0,0 
        else:
            # Decide se a direcao de saida de forma aleatoria
            self.speed_y = 7 * random.choice((1,-1))
            self.speed_x = 7 * random.choice((1,-1))
            # Seta o score_time para None para evitar erros
            score_time = None

        return score_time
    def movimentoBola(self, score_time):

        self.forma.x += self.speed_x
        self.forma.y += self.speed_y

        # Direcoes da bola, se acertar o topo inverte o valor de velocidade em y
        if self.forma.top <= 0 or self.forma.bottom >= altura_tela:
            self.speed_y *= -1

        # Se acertar a lateral esquerda ele reinicia a bola para o centro e aumenta o score do player ou oponente
        if self.forma.left <= 0: 
                player.score += 1
                score_time = pyg.time.get_ticks()
        if self.forma.right >= largura_tela:
                oponente.score += 1
                score_time = pyg.time.get_ticks()
        # Se entrar em colisao com o player ou com o oponente inverte a velocidade em x
        if self.forma.colliderect(player.forma) or self.forma.colliderect(oponente.forma):
            self.speed_x *= -1
        
        return score_time

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

# Variaveis texto
player_score = 0
oponente_score = 0
game_font = pyg.font.Font("freesansbold.ttf", 32)

# Objetos, Bola, Jogador
ball = Bola(direcao_x, direcao_y, pyg.Rect(largura_tela/2 - 10, altura_tela/2 - 10, 20, 20))
player = Player(0, pyg.Rect(largura_tela - 20, altura_tela/2 - 70, 10, 140), player_score)
oponente = Oponente(7, pyg.Rect(10, altura_tela/2 - 70, 10, 140), oponente_score)

bg_color = pyg.Color('grey12')
light_grey = (200, 200, 200)

# Score Timer
score_time = True


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

    score_time = ball.movimentoBola(score_time)
    
    # Visuals
    tela.fill(bg_color)
    pyg.draw.rect(tela, light_grey, player.forma)
    pyg.draw.rect(tela, light_grey, oponente.forma)
    pyg.draw.ellipse(tela, light_grey, ball.forma)
    pyg.draw.aaline(tela, light_grey, (largura_tela/2,0), (largura_tela/2, altura_tela))

    # Mostrando o Score do Player
    player_text = game_font.render(f"{player.score}", True, light_grey)
    tela.blit(player_text, ((largura_tela/2 + 16, altura_tela/2)))

    # Mostrando o Score do oponente
    oponente_text = game_font.render(f"{oponente.score}", True, light_grey)
    tela.blit(oponente_text, ((largura_tela/2 - 32, altura_tela/2)))
    
    if score_time:
        score_time = ball.ball_restart(score_time)
        

    # Atualizando a janela a 60 frames por segundo
    pyg.display.flip()
    clock.tick(60)

