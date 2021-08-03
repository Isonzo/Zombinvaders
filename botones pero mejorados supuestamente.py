import pygame
from images import *
ancho_pantalla = 512
alto_pantalla = 480
cuadro_texto1 = pygame.Rect(20,200,190,60)
cuadro_texto2 = pygame.Rect(300,200,190,60)
pygame.font.init()
screen = pygame.display.set_mode((ancho_pantalla,alto_pantalla))
pygame.display.set_caption("BOTONES MARCA BRUH")
background = fondo
background2 = fondo2
pygame.mixer.init()
def fade(ancho,alto):
    fade = pygame.Surface((ancho,alto))
    fade.fill((0,0,0))
    for i in range(0,300):
        fade.set_alpha(i)
        screen.blit(fade,(0,0))
        pygame.display.update()
        pygame.time.delay(4)
def controles():
    trans = True
    while trans:
        screen.blit(fondo2,[0,0])
        pygame.draw.line(screen, (152, 255, 152), (256, 100), (256, 300), 10)
        texto3.draw()
        texto4.draw()
        controles1.draw()
        controles2.draw()
        if flechaiz1.draw():
            pygame.mixer.music.load("317754__jalastram__sfx-explosion-05.wav")
            pygame.mixer.music.play(1)
            fade(800,500)
            submenu()
        if flechader1.draw():
            pygame.mixer.music.load("317754__jalastram__sfx-explosion-05.wav")
            pygame.mixer.music.play(1)
            fade(800, 500)
            #funcion que lleva a los niveles
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                quit()
        pygame.display.update()
def submenu():
    texto1 = pygame.font.Font("pixel_maz.ttf", 70)
    usuario1 = ''
    usuario2 = ''
    salir = True
    active = False
    active2 = False
    while salir:
        screen.blit(background2,[0,0])
        pygame.draw.line(screen,(153,255,153),(256,100),(256,300),10)
        texto.draw()
        texto2.draw()
        if flechaiz1.draw():
            pygame.mixer.music.load("317754__jalastram__sfx-explosion-05.wav")
            pygame.mixer.music.play(1)
            fade(800,500)
            menu()
        if flechader1.draw():
            pygame.mixer.music.load("317754__jalastram__sfx-explosion-05.wav")
            pygame.mixer.music.play(1)
            fade(800,500)
            controles()
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                quit()
            if i.type == pygame.MOUSEBUTTONDOWN:
                if cuadro_texto1.collidepoint(i.pos):
                    active = True
                else:
                    active = False
            if i.type == pygame.KEYDOWN:
                if active == True:
                    if i.key == pygame.K_BACKSPACE:
                        usuario1 = usuario1[:-1]
                    else:
                        usuario1 += i.unicode
            if i.type == pygame.MOUSEBUTTONDOWN:
                if cuadro_texto2.collidepoint(i.pos):
                    active2 = True
                else:
                    active2 = False
            if i.type == pygame.KEYDOWN:
                if active2 == True:
                    if i.key == pygame.K_BACKSPACE:
                        usuario2 = usuario2[:-1]
                    else:
                        usuario2 += i.unicode
        pygame.draw.rect(screen,(153,255,153),cuadro_texto1,2)
        letra = texto1.render(usuario1,True,(255,255,255))
        screen.blit(letra,(cuadro_texto1.x +5, cuadro_texto1.y +5))
        pygame.draw.rect(screen, (153, 255, 153), cuadro_texto2, 2)
        letra2 = texto1.render(usuario2, True, (255, 255, 255))
        screen.blit(letra2, (cuadro_texto2.x + 5, cuadro_texto2.y + 5))
        pygame.display.update()

class Boton():
    def __init__(self,x,y,imagen,imagen2):
        self.imagen = imagen
        self.imagen2 = imagen2
        self.rect = self.imagen.get_rect()
        self.rect.topleft = (x, y)
        self.rect2 = self.imagen2.get_rect()
        self.rect2.topleft = (x, y)
        self.clicked = False
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            screen.blit(self.imagen2,(self.rect2.x,self.rect2.y))
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0 :
                self.clicked = False
        else:
            screen.blit(self.imagen,(self.rect.x, self.rect.y))
        return action
inicio = Boton(25,50,boton_inicio,boton_inicio2)
exit = Boton(25,250,boton_exit,boton_exit2)
highscore = Boton(25,150,boton_highscore,boton_highscore2)
flechaiz1 = Boton(0,365,flechaiz,flechaiz2)
flechader1 = Boton(410,365,flechader,flechader2)
texto = Boton(0,20,texto,texto)
texto2 = Boton(262,20,texto2,texto2)
texto3 = Boton(0,10,texto3,texto3)
texto4 = Boton(262,10,texto4,texto4)
controles1 = Boton(20,140,controles1,controles1)
controles2 = Boton(290,140,controles2,controles2)
def menu():
    loop = True
    pygame.mixer.music.load("1-01 Title Theme (Mono).mp3")
    pygame.mixer.music.play(100)
    while loop:
        screen.blit(background, [0,0])
        if inicio.draw():
            pygame.mixer.music.load("317754__jalastram__sfx-explosion-05.wav")
            pygame.mixer.music.play(1)
            fade(800,500)
            submenu()
        if exit.draw():
            quit()
            print("exit")
        highscore.draw()
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                loop = False
        pygame.display.update()
menu()