import pygame
import constantes
import math
import random

class Weapon():
    def __init__(self, image, image_bala):
        self.image_bala = image_bala
        self.image_original = image
        self.angulo = 0
        self.image = pygame.transform.rotate(self.image_original, self.angulo)
        self.forma = self.image.get_rect()
        self.disparar = False
        self.ultimo_disparo = pygame.time.get_ticks()

    def update(self, personaje):
        disparo_cooldown = constantes.COOLDOWN_BALAS
        bala = None

        self.forma.center = personaje.forma.center
        
        if personaje.flip == False:
            self.forma.x = self.forma.x + personaje.forma.width/2
            self.rotar_arma(False)
        if personaje.flip == True:
            self.forma.x = self.forma.x - personaje.forma.width/2
            self.rotar_arma(True)

        # pistola-mouse
        mouse_pos = pygame.mouse.get_pos()
        distancia_x = mouse_pos[0] - self.forma.centerx
        distancia_y = -(mouse_pos[1] - self.forma.centery)
        self.angulo = math.degrees(math.atan2(distancia_y, distancia_x))

        # detectar clicks
        if pygame.mouse.get_pressed()[0] == True and self.disparar == False and (pygame.time.get_ticks() - self.ultimo_disparo >= disparo_cooldown):
            bala = Bullet(self.image_bala, self.forma.centerx, self.forma.centery, self.angulo)
            self.disparar = True
            self.ultimo_disparo = pygame.time.get_ticks()
        #resetrear el click
        if pygame.mouse.get_pressed()[0] == False:
            self.disparar = False
        return bala

    def rotar_arma(self, rotar):
        if rotar == True:
            imagen_flip = pygame.transform.flip(self.image_original, True, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
        else:
            imagen_flip = pygame.transform.flip(self.image_original, False, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)

    def dibujar(self, interfaz):
        self.imagen = pygame.transform.rotate(self.imagen, self.angulo)

        interfaz.blit(self.image, self.forma)
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = image
        self.angulo = angle
        self.image = pygame.transform.rotate(self.image_original, self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # calcular el movimiento de la bala
        self.delta_x = math.cos(math.radians(self.angulo)) * constantes.VELOCIDAD_BALA
        self.delta_y = -(math.sin(math.radians(self.angulo)) * constantes.VELOCIDAD_BALA)

    def update(self, lista_enemigos):
        damage = 0
        pos_damage = None
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y

        # ver si la bala se salio de la pantalla
        if self.rect.right < 0 or self.rect.left > constantes.ANCHO_VENTANA or self.rect.bottom < 0 or self.rect.top > constantes.ALTO_VENTANA:
            self.kill()

        # verificar si hay colicion
        for enemigo in lista_enemigos:
            if enemigo.forma.colliderect(self.rect):
                damage = 15 + random.randint(-7, 7)
                pos_damage = enemigo.forma
                enemigo.energia -= damage
                self.kill()
                break
        return damage, pos_damage
    
    def dibujar(self, interfaz):
        interfaz.blit(self.image, (self.rect.centerx, self.rect.centery - int(self.image.get_height())))