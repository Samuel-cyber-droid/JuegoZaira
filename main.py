import pygame # type: ignore
import constantes
from personaje import Personaje
from weapon import Weapon
from textos import DamageText
import os
from items import Item


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

pygame.mixer.init()

# fuentes
font = pygame.font.Font("assets//fonts//GravityBold8.ttf", 10)
font_inicio = pygame.font.Font("assets//fonts//GravityBold8.ttf", 30)
font_titulo = pygame.font.Font("assets//fonts//GravityBold8.ttf", 60)


#botones de inicio
boton_jugar = pygame.Rect(constantes.ANCHO_VENTANA / 2 - 100, constantes.ALTO_VENTANA / 2 - 50, 200, 50)
boton_salir = pygame.Rect(constantes.ANCHO_VENTANA / 2 - 100, constantes.ALTO_VENTANA / 2 + 50, 200, 50)
text_boton_jugar = font_inicio.render("Jugar", True, constantes.COLOR_NEGRO)
text_boton_salir = font_inicio.render("Salir", True, constantes.COLOR_BLANCO)

# panatalla inicio
def pantalla_inicio():
    ventana.fill(constantes.COLOR_INICIO)
    dibujar_texto("Zaira Bros", font_titulo, constantes.COLOR_BLANCO, constantes.ANCHO_VENTANA / 2 - 200, constantes.ALTO_VENTANA / 2 - 200)
    pygame.draw.rect(ventana, constantes.COLOR, boton_jugar)
    pygame.draw.rect(ventana, constantes.COLOR, boton_salir)
    ventana.blit(text_boton_jugar, (boton_jugar.x + 50, boton_jugar.y + 10))
    ventana.blit(text_boton_salir, (boton_salir.x + 70, boton_salir.y + 10))


#energia
corazon_vacion = pygame.image.load("assets//image//items//heart.png")
corazon_vacion = escalar_img(corazon_vacion, constantes.SCALAR_CORAZON)
corazon_mitad = pygame.image.load("assets//image//items//heartmid.png")
corazon_mitad = escalar_img(corazon_mitad, constantes.SCALAR_CORAZON)
corazon_lleno = pygame.image.load("assets//image//items//heartfull.png")
corazon_lleno = escalar_img(corazon_lleno, constantes.SCALAR_CORAZON)

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

# cargar imagenes items
posicion_roja = pygame.image.load("assets//image//items//potion.png")
posicion_roja = escalar_img(posicion_roja, 1)

# cargar imagenes monedas
coin_image = []
ruta_img = "assets//image//items//coin"
num_coins_image = contar_elementos(ruta_img)
for i in range(num_coins_image):
    img = pygame.image.load(f"assets//image//items//coin//coin_{i + 1}.png")
    img = escalar_img(img, 1)
    coin_image.append(img)

def dibujar_texto(texto, fuente, color, x, y):
    img = fuente.render(texto, True, color)
    ventana.blit(img, (x, y))

def vida_jugador():
    for i in range(4):
        if jugador.energia >= ((i + 1)* 25):
            ventana.blit(corazon_lleno, (5 + i * 50, 5)) 

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

# crear grupo de items
grupo_items = pygame.sprite.Group()

coin = Item(350, 25, 0, coin_image)
potion = Item(380, 55, 1, [posicion_roja])

grupo_items.add(coin)
grupo_items.add(potion)

# definir las variables de movimiento
mover_arriba = False
mover_abajo = False
mover_derecha = False
mover_izquierda = False

# controlar el framerate
reloj = pygame.time.Clock()

pygame.mixer.music.load("assets//sounds//CriticalTheme.wav")
pygame.mixer.music.play(-1)

sonido_disparo = pygame.mixer.Sound("assets//sounds//disparo.wav")

mostrar_inicio = True
run = True
while run == True:

    if mostrar_inicio:
        pantalla_inicio()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    mostrar_inicio = False
                if boton_salir.collidepoint(event.pos):
                    run = False
    else:
        # controlar el framerate
        reloj.tick(constantes.FPS)
        ventana.fill(constantes.COLOR_BG)

        # calcular el movimiento del jugador
        delta_x = 0
        delta_y = 0

        if mover_derecha == True:
            delta_x = constantes.VELOCIDAD_MOVIMIENTO
        if mover_izquierda == True:
            delta_x = -constantes.VELOCIDAD_MOVIMIENTO
        if mover_arriba == True:
            delta_y = -constantes.VELOCIDAD_MOVIMIENTO
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
            sonido_disparo.play()
        for bala in grupo_balas:
            damage, pos_damage = bala.update(lista_enemigos)
            if damage:
                dt = DamageText(pos_damage.centerx, pos_damage.centery, str(damage), font, constantes.COLOR)
                grupo_damage_text.add(dt)

        #dibujar textos
        dibujar_texto(f"Score: {jugador.score}", font, (255, 255, 0), 700, 5)

        # actualizar damage text
        grupo_damage_text.update()

        # actualizar items
        grupo_items.update(jugador)

        # dibujar items
        grupo_items.draw(ventana)

        # dibujar energia
        vida_jugador()

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