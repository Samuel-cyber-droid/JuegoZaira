import pygame
import constantes
from personaje import Personaje
from weapon import Weapon
from textos import DamageText
import os

# funcion para escalar las imagenes
def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (w*scale, h*scale))
    return nueva_imagen

# funcion para contar elementos
def contar_elementos(directorio):
    return len(os.listdir(directorio))

# funcion para listar nombres elementos
def nombre_carpertas(directorio):
    return os.listdir(directorio)

pygame.init()

# fuentes
font = pygame.font.Font("assets//fonts//GravityBold8.ttf", 10)

# ventana
ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))

# titulo de ventana
pygame.display.set_caption("Juego")

# importacion de imagenes
# personaje
animaciones = []
for i in range(7):
    img = pygame.image.load(f"assets//image//characters//player//Player_{i}.png").convert_alpha()
    
    img = escalar_img(img, constantes.SCALA_PERSONAJE)
    animaciones.append(img)

#enemigos
directorio_enemigos = "assets//image//characters//enemies"
tipo_enemigos = nombre_carpertas(directorio_enemigos)
animaciones_enemigos = []
for eni in tipo_enemigos:
    lista_temp = []
    ruta_temp = f"assets//image//characters//enemies//{eni}"
    num_animaciones = contar_elementos(ruta_temp)
    for i in range(num_animaciones):
        img_enemigo = pygame.image.load(f"{ruta_temp}//{eni}_{i + 1}.png").convert_alpha()
        img_enemigo = escalar_img(img_enemigo, constantes.SCALA_ENEMIGO)
        lista_temp.append(img_enemigo)
    animaciones_enemigos.append(lista_temp)


# arma
image_pistola = pygame.image.load("assets//image//weapons//gun.png").convert_alpha()
image_pistola = escalar_img(image_pistola, constantes.SCALA_ARMA)

# balas
image_balas = pygame.image.load("assets//image//weapons//bala.png")
image_balas = escalar_img(image_balas, constantes.SCALA_BALA)

# creacion del personaje
jugador = Personaje(50, 50, animaciones, 100)

# creacion de enemigo
goblin = Personaje(400, 300, animaciones_enemigos[0], 100)
soldier = Personaje(200, 200, animaciones_enemigos[1], 100)
goblin_2 = Personaje(100, 250, animaciones_enemigos[0], 100)

# crear lista de enemigos
lista_enemigos = []
lista_enemigos.append(goblin)
lista_enemigos.append(goblin_2)
lista_enemigos.append(soldier)


# creacion de arma
pistola = Weapon(image_pistola, image_balas)

# crear un grupo de balas
grupo_balas = pygame.sprite.Group()
grupo_damage_text = pygame.sprite.Group()


# definir las variables de movimiento
mover_arriba = False
mover_abajo = False
mover_derecha = False
mover_izquierda = False

# controlar el framerate
reloj = pygame.time.Clock()

run = True

while run == True:



    # controlar el framerate
    reloj.tick(constantes.FPS)
    ventana.fill(constantes.COLOR_BG)

    # calcular el movimiento del jugador
    delta_x = 0
    delta_y = 0

    if mover_derecha == True:
        delta_x = constantes.VELOCIDAD_MOVIMIENTO
    if mover_izquierda == True:
        delta_x = constantes.VELOCIDAD_MOVIMIENTO
    if mover_arriba == True:
        delta_y = constantes.VELOCIDAD_MOVIMIENTO
    if mover_abajo == True:
        delta_y = constantes.VELOCIDAD_MOVIMIENTO

    # actualizar la posicion del jugador
    jugador.movimiento(delta_x, delta_y)

    # actualizar estado de jugador
    jugador.update()

    # actualizar estado de enemigo
    for ene in lista_enemigos:
        ene.update()

    # actualizar estado de arma
    bala = pistola.update(jugador)
    if bala:
        grupo_balas.add(bala)
    for bala in grupo_balas:
        damage, pos_damage = bala.update(lista_enemigos)
        if damage:
            dt = DamageText(pos_damage.centerx, pos_damage.centery, str(damage), font, constantes.COLOR)
            grupo_damage_text.add(dt)

    # actualizar damage text
    grupo_damage_text.update()

    # dibujar arma
    pistola.dibujar(ventana)

    #dibujo de jugador
    jugador.dibujar(ventana)

    # dibujar damage text
    grupo_damage_text.draw(ventana)

    # dibujar enemigo
    for ene in lista_enemigos:
        ene.dibujar(ventana)

    # dibujar balas
    for bala in grupo_balas:
        bala.dibujar(ventana)

    # cerrar ventana
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_s:
                mover_abajo = True

        # cuando se suelta la tecla
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_d:
                mover_derecha = False
            if event.key == pygame.K_w:
                mover_arriba = False
            if event.key == pygame.K_s:
                mover_abajo = False

    pygame.display.update()

pygame.quit()