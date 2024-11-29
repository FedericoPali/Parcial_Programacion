import pygame
from funciones import *
from colores import *
from constantes import *
import pygame.mixer as mixer
import csv
import sys

def ranking() -> None:
    """
    Muestra una ventana con el ranking de los 10 mejores jugadores usando Pygame.

    La función lee una matriz de un archivo CSV con los datos del ranking, los muestra en una ventana Pygame,
    y asigna una corona al jugador en la primera posición.

    Args:
        None

    Returns:
        None
    """

    top_1 = False
    ANCHO_RANKING = 450
    ALTO_RANKING = 40
    matriz_ranking = crear_matriz("ranking.csv")

    pygame.init()
    pygame.font.init()

    fuente = pygame.font.Font("assets/BebasNeue-Regular.ttf", 20)
    fuente_encabezado = pygame.font.Font("assets/Pixelmania.ttf", 25)

    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Ranking")
    imagen_coronita = pygame.image.load("assets/coronita.png")
    imagen_coronita = pygame.transform.scale(imagen_coronita,(20,30))
    bandera = True

    while bandera:
        lista_eventos = pygame.event.get()
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                bandera = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    bandera = False

        pantalla.fill(ANTIQUEWHITE)
        rectangulo_encabezado = crear_rectangulo(pantalla, GRAY80,0, 0, ANCHO_VENTANA, ALTO_RANKING)
        rectangulos_ranking = []

        for i in range(len(matriz_ranking)):  
            y = 50 + i * 50  
            rectangulo = crear_rectangulo(pantalla, GRAY80, 165, y, ANCHO_RANKING, ALTO_RANKING)
            rectangulos_ranking.append(rectangulo)

            texto_encabezado = "TOP 10"
            encabezado, coordenadas_encabezado = centrar_texto(texto_encabezado, fuente_encabezado, BLACK, rectangulo_encabezado)
            pantalla.blit(encabezado, coordenadas_encabezado)

        for i in range(len(matriz_ranking)):
            if top_1 == False:
                texto = f"{matriz_ranking[i][0]} || {matriz_ranking[i][1]} || {matriz_ranking[i][2]}"
                top_1 = True
            else:
                texto = f"{matriz_ranking[i][0]} || {matriz_ranking[i][1]} || {matriz_ranking[i][2]}"  
                usuario, coordenadas = centrar_texto(texto, fuente, BLACK, rectangulos_ranking[i])  
                pantalla.blit(usuario, coordenadas)
        
        pantalla.blit(imagen_coronita,(290,55))

        pygame.display.flip()
    
    return
