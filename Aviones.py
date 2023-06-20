#se importa pygame, random, os
import pygame
import random
import os

#se inicia pygame y el mixer de sonido
pygame.init()
pygame.mixer.init()

#se cargan los sonidos
sonido_fondo = pygame.mixer.Sound("Juego Aviones/sonidos/fondo.mp3")
caida_bomba=pygame.mixer.Sound("Juego Aviones/sonidos/caida_bomba.mp3")
explosion_bomba=pygame.mixer.Sound("Juego Aviones/sonidos/explosion.mp3")
sonido_misil=pygame.mixer.Sound("Juego Aviones/sonidos/sonido_misil.mp3")
game_over=pygame.mixer.Sound("Juego Aviones/sonidos/game_over.mp3")

#se reproduce la musica de fondo en bucle infinito
pygame.mixer.Sound.play(sonido_fondo, -1)

#ancho y alto de pantalla
pantalla_ancho=900
pantalla_alto=600

#se crea la pantalla
pantalla=pygame.display.set_mode((pantalla_ancho,pantalla_alto))

#titulo a la pantalla
pygame.display.set_caption("Air Combat")
icono=pygame.image.load("Juego Aviones/icono.png")
pygame.display.set_icon(icono)

#se cargan imagenes de explosiones y se crea animacion de explosion con 
#diccionario y 4 tamaños diferentes
carpeta_juego=os.path.dirname(__file__)
explosiones=os.path.join(carpeta_juego,"explosiones")
animacion_explosion={'t1':[],'t2':[],'t3':[],'t4':[]}
for x in range(1,9):
    archivo_explosiones=f'explosion{x:01d}.png'
    imagenes=pygame.image.load(os.path.join(explosiones,archivo_explosiones))
    imagenes_t1=pygame.transform.scale(imagenes,(50,50))
    animacion_explosion['t1'].append(imagenes_t1)
    imagenes_t2=pygame.transform.scale(imagenes,(70,70))
    animacion_explosion['t2'].append(imagenes_t2)
    imagenes_t3=pygame.transform.scale(imagenes,(90,90))
    animacion_explosion['t3'].append(imagenes_t3)
    imagenes_t4=pygame.transform.scale(imagenes,(110,110))
    animacion_explosion['t4'].append(imagenes_t4)

#carga de fondos y metodo para dibujarlos
fondo1=pygame.image.load(os.path.join(carpeta_juego,"fondo1.jpg"))
fondo2=pygame.image.load(os.path.join(carpeta_juego,"fondo2.png"))
def dibujar_fondo(fondo):
    fondo_escala=pygame.transform.scale(fondo,(pantalla_ancho,pantalla_alto))
    pantalla.blit(fondo_escala,(0,0))

#fotogramas por segundo
reloj=pygame.time.Clock()
FPS=60

#colores
negro=(10,10,10)
amarillo=(255,255,0)
rojo=(255,0,0)
blanco=(255,255,255)

#fuente de textos y metodo para mostrar en pantalla
aldhabi=pygame.font.match_font('Aldhabi')
def muestra_texto(pantalla,fuente,texto,color,dimensiones,x,y):
	tipo_letra=pygame.font.Font(fuente,dimensiones)
	superficie=tipo_letra.render(texto,True,color)
	rectangulo=superficie.get_rect()
	rectangulo.center = (x, y)
	pantalla.blit(superficie,rectangulo)

principio=pygame.image.load("Juego Aviones/F16.jpg")
def pantalla_principal():  
    dibujar_fondo(principio)
    muestra_texto(pantalla,aldhabi,"AIR COMBAT",amarillo,66, pantalla_ancho // 2, pantalla_alto // 4)
    muestra_texto(pantalla,aldhabi,"AIR COMBAT",rojo,65, pantalla_ancho // 2, pantalla_alto // 4)
    muestra_texto(pantalla,aldhabi,"Pulse una tecla para empezar",rojo,20,pantalla_ancho //2,pantalla_alto* 3/4)  
    pygame.display.flip()
    esperar= True
    while esperar:
        reloj.tick(60)
        for event in pygame.event.get(): 
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type==pygame.KEYUP:
                esperar=False

#barra de salud de jugador
def barra_hp(pantalla,x,y,hp,color):
    largo=100
    ancho=15
    calculo_barra=int((hp/100)*largo)
    borde=pygame.Rect(x,y,largo,ancho)
    rectangulo=pygame.Rect(x,y,calculo_barra,ancho)
    pygame.draw.rect(pantalla,color,borde,3)
    pygame.draw.rect(pantalla,color,rectangulo)
    
#barra de salud de enemigo
def barra_hp_enemigo(pantalla,x,y,hp,hp2,color):
    largo=50
    ancho=15
    calculo_barra=int((hp/hp2)*largo)
    borde=pygame.Rect(x,y,largo,ancho)
    rectangulo=pygame.Rect(x,y,calculo_barra,ancho)
    pygame.draw.rect(pantalla,color,borde,3)
    pygame.draw.rect(pantalla,color,rectangulo)

#clase jugador
class Barco_Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #se carga imagen, posicion, velocidad, cadencia de disparos,
        #vidas y hp
        self.image=pygame.image.load("Juego Aviones/barco_jugador/barco_der.png")
        self.rect=self.image.get_rect()
        self.velocidad_x=0
        self.cadencia_disparo=1000
        self.ultimo_disparo=pygame.time.get_ticks()
        self.vidas=3
        self.hp=100
        self.radius=65
        #las coordenadas x e y se dan despues del radio para trabajar colisiones
        self.rect.x=300
        self.rect.y=450
    def update(self):
        #movimientos
        self.velocidad_x=0
        teclas=pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.x -=3
            self.image=pygame.image.load("Juego Aviones/barco_jugador/barco_izq.png")
        if teclas[pygame.K_RIGHT]:
            self.rect.x +=3 
            self.image=pygame.image.load("Juego Aviones/barco_jugador/barco_der.png")
        if teclas[pygame.K_UP]:
            self.rect.y -=3
        if teclas[pygame.K_DOWN]:
            self.rect.y +=3
        #si se presiona espacio se dispara con 1 seg. entre disparos
        if teclas[pygame.K_SPACE]:
            disparo=pygame.time.get_ticks()
            if disparo- self.ultimo_disparo>self.cadencia_disparo:
                jugador.disparo()
                pygame.mixer.Sound.play(sonido_misil)
                self.ultimo_disparo=disparo
        #limites de pantalla
        if self.rect.left<0:
            self.rect.left=0
        if self.rect.right>pantalla_ancho:
            self.rect.right=pantalla_ancho
        if self.rect.bottom>pantalla_alto-10:
            self.rect.bottom=pantalla_alto-10
        if self.rect.top<pantalla_alto-190:
            self.rect.top=pantalla_alto-190
        #se actualiza la posicion
        self.rect.x += self.velocidad_x
    #se instancia un objeto bala con las coordenadas del barco y se lo añade
    #al grupo de sprites
    def disparo(self):
        bala=Disparos_Jugador(self.rect.centerx,self.rect.top)
        balas_jugador.add(bala)
        
#3 clases de aviones enemigos
class Avion_Enemigo1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #se cargan imagenes con posiciones aleatorias, velocidades, cadencias y
        #hp diferentes
        self.image=pygame.image.load("Juego Aviones/aviones_enemigos/avion_enemigo_ataque1.png")
        self.rect=self.image.get_rect()
        self.rect.x=1000
        self.rect.y=random.randrange(0,300)
        self.velocidad_x=random.randrange(3,5)
        self.cadencia_disparo=2000
        self.ultimo_disparo=pygame.time.get_ticks()
        self.hp=10
    def update(self):
        #si sale de la pantalla se resetea
        self.rect.x -= self.velocidad_x
        if self.rect.left<-200:
            self.rect.x=1000
            self.rect.y=random.randrange(0,300)
            self.velocidad_x=random.randrange(3,5)
        #disparos enemigos
        disparo=pygame.time.get_ticks()
        if disparo- self.ultimo_disparo>self.cadencia_disparo:
                enemigo1.disparo()
                pygame.mixer.Sound.play(caida_bomba)
                self.ultimo_disparo=disparo
    def disparo(self):
        bala=Disparos_Enemigo_Izquierda(self.rect.centerx,self.rect.bottom)
        balas_enemigo.add(bala)

class Avion_Enemigo2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("Juego Aviones/aviones_enemigos/avion_enemigo_ataque2.png")
        self.rect=self.image.get_rect()
        self.rect.x=1000
        self.rect.y=random.randrange(0,250)
        self.velocidad_x=random.randrange(6,8)
        self.cadencia_disparo=1500
        self.ultimo_disparo=pygame.time.get_ticks()
        self.hp=15
    def update(self):
        self.rect.x -= self.velocidad_x
        if self.rect.right<0:
            self.rect.x=1000
            self.rect.y=random.randrange(0,250)
            self.velocidad_x=random.randrange(6,8)
        disparo=pygame.time.get_ticks()
        if disparo- self.ultimo_disparo>self.cadencia_disparo:
                enemigo2.disparo()
                pygame.mixer.Sound.play(caida_bomba)
                self.ultimo_disparo=disparo
    def disparo(self):
        bala=Disparos_Enemigo_Izquierda(self.rect.centerx,self.rect.bottom)
        balas_enemigo.add(bala)

class Avion_Enemigo3(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("Juego Aviones/aviones_enemigos/avion_enemigo_ataque3.png")
        self.rect=self.image.get_rect()
        self.rect.x=-200
        self.rect.y=random.randrange(0,200)
        self.velocidad_x=random.randrange(9,11)
        self.cadencia_disparo=1000
        self.ultimo_disparo=pygame.time.get_ticks()
        self.hp=20
    def update(self):
        self.rect.x += self.velocidad_x
        if self.rect.right>pantalla_ancho+200:
            self.rect.x=-200
            self.rect.y=random.randrange(0,200)
            self.velocidad_x=random.randrange(9,11)
        disparo=pygame.time.get_ticks()
        if disparo- self.ultimo_disparo>self.cadencia_disparo:
                enemigo3.disparo()
                pygame.mixer.Sound.play(caida_bomba)
                self.ultimo_disparo=disparo
    def disparo(self):
        bala=Disparos_Enemigo_Derecha(self.rect.centerx,self.rect.bottom)
        balas_enemigo.add(bala)

#clase disparos jugador, se carga imagen, se dan las posiciones dinamicas y
#cuando sale de pantalla, se elimina, lo mismo con disparos enemigos
class Disparos_Jugador(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load("Juego Aviones/misiles/misil_jugador.png")
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
    def update(self):
        self.rect.y -=5
        if self.rect.top<-50:
            self.kill()

class Disparos_Enemigo_Derecha(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load("Juego Aviones/misiles/misil_enemigo_der.png")
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
    def update(self):
        self.rect.y +=5
        if self.rect.top>pantalla_alto:
            self.kill()

class Disparos_Enemigo_Izquierda(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load("Juego Aviones/misiles/misil_enemigo_izq.png")
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
    def update(self):
        self.rect.y +=5
        if self.rect.top>pantalla_alto:
            self.kill()

#clase explosiones
class Explosiones(pygame.sprite.Sprite):
    def __init__(self,centro,dimensiones,fotogramas):
        #se carga la animacion de la explosion, se dan dimensiones,
        #posicion y fotogramas
        pygame.sprite.Sprite.__init__(self)
        self.dimensiones=dimensiones
        self.image=animacion_explosion[self.dimensiones][0]
        self.rect=self.image.get_rect()  
        self.rect.center=centro  
        self.fotograma=0
        self.frecuencia_fotograma=fotogramas
        self.actualizacion=pygame.time.get_ticks()
    def update(self):
        explosion=pygame.time.get_ticks()
        if explosion - self.actualizacion > self.frecuencia_fotograma:
            self.actualizacion=explosion
            self.fotograma +=1
            if self.fotograma == len(animacion_explosion[self.dimensiones]):
                self.kill()
            else:
                centro=self.rect.center
                self.image=animacion_explosion[self.dimensiones][self.fotograma]
                self.rect= self.image.get_rect()
                self.rect.center=centro  

#se cargan imagenes
imagen_vida=pygame.image.load("Juego Aviones/barco_jugador/barco_der.png")
cruz=pygame.image.load("Juego Aviones/cruz_roja.png")
escudo=pygame.image.load("Juego Aviones/escudo.png")
emergencia=pygame.image.load("Juego Aviones/emergencia.png")

#variable de puntos y contador de sonido al perder
puntos=0
contador_sonido_perder=0

#variables booleanas de juego y dibujar barras de vida
dibujar_barra=True
jugar=True 
pantalla_inicio=True
contador=0

while jugar:
    if pantalla_inicio:
        pantalla_principal()
        pantalla_inicio=False
        #se crean grupos y se instancian objetos

        barco_jugador= pygame.sprite.Group()
        avion_enemigo1= pygame.sprite.Group()
        avion_enemigo2= pygame.sprite.Group()
        avion_enemigo3= pygame.sprite.Group()
        balas_jugador=pygame.sprite.Group()
        balas_enemigo=pygame.sprite.Group()
        explosion=pygame.sprite.Group()

        jugador=Barco_Jugador()
        barco_jugador.add(jugador)
        enemigo1=Avion_Enemigo1()
        avion_enemigo1.add(enemigo1)
        enemigo2=Avion_Enemigo2()
        avion_enemigo2.add(enemigo2)
        enemigo3=Avion_Enemigo3()
        avion_enemigo3.add(enemigo3)
        #reloj
    reloj.tick(FPS)
    
        #primer fondo
    dibujar_fondo(fondo1)
    
        #colisiones
    colision_balas_jugador=pygame.sprite.groupcollide(barco_jugador,balas_enemigo,False,True,pygame.sprite.collide_circle)
    colision_balas_enemigo1=pygame.sprite.groupcollide(avion_enemigo1,balas_jugador,False,True)
    colision_balas_enemigo2=pygame.sprite.groupcollide(avion_enemigo2,balas_jugador,False,True)
    colision_balas_enemigo3=pygame.sprite.groupcollide(avion_enemigo3,balas_jugador,False,True)
    
    #explosiones de tamaño aleatorio, sonido y descuento de hp
    explosion_aleatoria=random.randrange(1,4)
    
    if colision_balas_jugador:
        explota=Explosiones(jugador.rect.center,f't{explosion_aleatoria}',random.randrange(35,50)) 
        explosion.add(explota)
        pygame.mixer.Sound.play(explosion_bomba)
        jugador.hp -=10
        
    if colision_balas_enemigo1:
        explota=Explosiones(enemigo1.rect.center,f't{explosion_aleatoria}',random.randrange(35,50)) 
        explosion.add(explota)
        pygame.mixer.Sound.play(explosion_bomba)
        enemigo1.hp -=5
    if enemigo1.hp <=0:
        enemigo1.rect.x=1000
        enemigo1.rect.y=random.randrange(0,350)
        puntos +=10
        enemigo1.hp=10

    if colision_balas_enemigo2:
        explota=Explosiones(enemigo2.rect.center,f't{explosion_aleatoria}',random.randrange(35,50)) 
        explosion.add(explota)
        pygame.mixer.Sound.play(explosion_bomba)
        enemigo2.hp -=5
    if enemigo2.hp <=0:
        enemigo2.rect.x=1000
        enemigo2.rect.y=random.randrange(0,350)
        puntos +=20
        enemigo2.hp=15

    if colision_balas_enemigo3:
        explota=Explosiones(enemigo3.rect.center,f't{explosion_aleatoria}',random.randrange(35,50)) 
        explosion.add(explota)
        pygame.mixer.Sound.play(explosion_bomba)
        enemigo3.hp -=5
    if enemigo3.hp <=0:
        enemigo3.rect.x=1000
        enemigo3.rect.y=random.randrange(0,350)
        puntos +=50
        enemigo3.hp=20

    #actualizacion de objetos
    barco_jugador.update()

    avion_enemigo1.update()
    avion_enemigo2.update()
    avion_enemigo3.update()

    balas_jugador.update()
    balas_enemigo.update()
    explosion.update()
    
    #se dibujan objetos
    barco_jugador.draw(pantalla)
    avion_enemigo1.draw(pantalla)
    avion_enemigo2.draw(pantalla)
    avion_enemigo3.draw(pantalla)
    balas_jugador.draw(pantalla)
    balas_enemigo.draw(pantalla)
    explosion.draw(pantalla)
    
    #si el jugador no muere, se dibujan barras de vida y vidas del jugador
    if dibujar_barra==True:
        barra_hp(pantalla,jugador.rect.centerx-40,jugador.rect.bottom-15,jugador.hp,amarillo)
        barra_hp_enemigo(pantalla,enemigo1.rect.centerx-15,enemigo1.rect.bottom,enemigo1.hp,10,rojo)
        barra_hp_enemigo(pantalla,enemigo2.rect.centerx-20,enemigo2.rect.bottom,enemigo2.hp,15,rojo)
        barra_hp_enemigo(pantalla,enemigo3.rect.centerx-20,enemigo3.rect.bottom,enemigo3.hp,20,rojo)
        vida_1=pantalla.blit(pygame.transform.scale(imagen_vida,(25,25)),(pantalla_ancho-150,pantalla_alto-100))
        vida_2=pantalla.blit(pygame.transform.scale(imagen_vida,(25,25)),(pantalla_ancho-100,pantalla_alto-100))
        vida_3=pantalla.blit(pygame.transform.scale(imagen_vida,(25,25)),(pantalla_ancho-50,pantalla_alto-100))
        muestra_texto(pantalla,aldhabi,"Puntos: " + str(puntos),negro,50,pantalla_ancho-105,pantalla_alto-50)
        if jugador.hp>30:
            pantalla.blit(pygame.transform.scale(escudo,(25,25)),(jugador.rect.centerx-40,jugador.rect.bottom-15))
        else:
            pantalla.blit(pygame.transform.scale(emergencia,(25,25)),(jugador.rect.centerx-40,jugador.rect.bottom-15))
    else:
        #si no, se dibuja el segundo fondo y se reproduce sonido "game over"
        dibujar_fondo(fondo2)  
        muestra_texto(pantalla,aldhabi,"Puntos: " + str(puntos),blanco,50,pantalla_ancho-105,pantalla_alto-50)
        contador +=1
        if contador_sonido_perder<1 and contador ==50:
            pygame.mixer.Sound.play(game_over)
            contador_sonido_perder +=1
    
    #descuento de vidas cuando el hp llega a 0 y reseteo del jugador
    if jugador.hp<=0 and jugador.vidas==3:
        jugador.kill()
        jugador=Barco_Jugador()
        barco_jugador.add(jugador)
        jugador.vidas=2
    if jugador.vidas==2:
        if jugador.hp<=0:
            jugador.kill()
            jugador=Barco_Jugador()
            barco_jugador.add(jugador)
            jugador.vidas=1
        if dibujar_barra==True:
            muerte_1=pantalla.blit(pygame.transform.scale(cruz,(25,25)),(pantalla_ancho-150,pantalla_alto-95))
    if jugador.vidas==1:
        if jugador.hp<=0:
            jugador.kill()
            jugador=Barco_Jugador()
            barco_jugador.add(jugador)
            jugador.vidas=0
        if dibujar_barra==True:
            muerte_1=pantalla.blit(pygame.transform.scale(cruz,(25,25)),(pantalla_ancho-150,pantalla_alto-95))       
            muerte_2=pantalla.blit(pygame.transform.scale(cruz,(25,25)),(pantalla_ancho-100,pantalla_alto-95))
    if jugador.vidas==0:
        #cuando se terminan las vidas, se eliminan los enemigos
        if jugador.hp<=0:
            jugador.kill()
            dibujar_barra=False
            enemigo1.kill()
            enemigo2.kill()
            enemigo3.kill()
        if dibujar_barra==True:
            muerte_1=pantalla.blit(pygame.transform.scale(cruz,(25,25)),(pantalla_ancho-150,pantalla_alto-95))       
            muerte_2=pantalla.blit(pygame.transform.scale(cruz,(25,25)),(pantalla_ancho-100,pantalla_alto-95))
            muerte_3=pantalla.blit(pygame.transform.scale(cruz,(25,25)),(pantalla_ancho-50,pantalla_alto-100))
    
    #limite para la barra de vida
    if jugador.hp<0:
        jugador.hp=0
    
    #busqueda de evento para salir del juego
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            jugar=False

    #actualizacion de pantalla
    pygame.display.flip()

#se sale del juego
pygame.quit()