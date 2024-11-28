import pygame
import pantalla_juego
import pantalla_ranking
import pantalla_config
from funciones import *
from colores import *
from constantes import *

pygame.mixer.init()
pygame.init()
pantalla = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
Título = pygame.display.set_caption("Mi Juego")
bandera = True
pygame.font.init()

fuente = pygame.font.Font("assets/Pixelmania.ttf", 20)
imagen_fondo = pygame.image.load("assets/preguntados_fondo.png")
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_VENTANA, ALTO_VENTANA))

el_globo = pygame.image.load("assets/globito.png")
el_globo = pygame.transform.scale(el_globo,(20,30))

# Cargar imágenes
el_globo = pygame.image.load("assets/globito.png")
el_globo = pygame.transform.scale(el_globo, (20, 30))

estado_actual = "principal"  
bandera = True

# Bucle principal
while bandera:
    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            bandera = False
    
    if estado_actual == "principal":
        pantalla.fill(ANTIQUEWHITE)

        rectangulo_globo = pygame.draw.rect(pantalla, ANTIQUEWHITE, (0, 0, 20, 30))
        pantalla.blit(imagen_fondo, (0,0))

        # Dibujar botones
        rectangulo_jugar = pygame.draw.rect(pantalla, PLUM2, (150, 200, ANCHO_RECTANGULO_RESPUESTA, ALTO_RECTANGULO_RESPUESTA))
        texto_jugar, coordenadas_jugar = centrar_texto("JUGAR", fuente, BLACK, rectangulo_jugar)
        pantalla.blit(texto_jugar, coordenadas_jugar)

        rectangulo_ranking = pygame.draw.rect(pantalla, PLUM2, (150, 300, ANCHO_RECTANGULO_RESPUESTA, ALTO_RECTANGULO_RESPUESTA))
        texto_ranking, coordenadas_ranking = centrar_texto("RANKING", fuente, BLACK, rectangulo_ranking)
        pantalla.blit(texto_ranking, coordenadas_ranking)

        pantalla.blit(el_globo, (0, 0))

        rectangulo_configuracion = pygame.draw.rect(pantalla, PLUM2, (150,400,ANCHO_RECTANGULO_RESPUESTA,ALTO_RECTANGULO_RESPUESTA))
        texto_configuracion, coordenadas_config = centrar_texto("CONFIGURACION", fuente, BLACK, rectangulo_configuracion)
        pantalla.blit(texto_configuracion,coordenadas_config)
        
        # Detectar clics en botones
        for evento in lista_eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if rectangulo_jugar.collidepoint(mouse_pos):
                    estado_actual = "juego"  # Cambiar a la pantalla de juego
                elif rectangulo_ranking.collidepoint(mouse_pos):
                    estado_actual = "ranking"  # Cambiar a la pantalla de ranking
                elif rectangulo_globo.collidepoint(mouse_pos):
                    print("¡Aguante el globo!")
                elif rectangulo_configuracion.collidepoint(mouse_pos):
                    estado_actual = "configuracion"

    elif estado_actual == "juego":
        # Llama a la función de juego y espera su retorno
        pantalla_juego.jugar()
        estado_actual = "principal"  # Regresa al menú principal

    elif estado_actual == "ranking":
        # Llama a la función de ranking y espera su retorno
        pantalla_ranking.ranking()
        estado_actual = "principal"  # Regresa al menú principal

    elif estado_actual == "configuracion":

        pantalla_config.configuracion()
        estado_actual = "principal"

    pygame.display.update()

pygame.quit()