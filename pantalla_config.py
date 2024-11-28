import pygame
import csv
import sys
from funciones import *
from colores import *
from constantes import *
import pygame.mixer as mixer
import os  # Para verificar si el archivo existe

def configuracion() -> None:
    """
    Permite al usuario modificar configuraciones del juego como la vida, el tiempo, los puntos por respuesta correcta
    y agregar nuevas preguntas, todo a traves de una ventana en Pygame. Esta misma funciona a traves de clicks
    en los rectangulos y escribiendo lo que se desea modificar o agregar.

    Args:
        None

    Returns:
        None
    """
    
    bandera = True

    ruta_csv = "configuracion.csv"
    ruta_preguntas = "preguntas.csv"
    config = cargar_configuracion(ruta_csv)  # Cargar configuración desde el archivo

    pygame.init()
    pygame.font.init()

    fuente = pygame.font.Font("assets/BebasNeue-Regular.ttf", 30)
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Configuracion")

    escribiendo = False  # Para verificar si se está escribiendo
    atributo_seleccionado = None  # Atributo actual seleccionado (vidas, puntos, tiempo)
    entrada_texto = ""  # Valor ingresado por el usuario

    # Para agregar una pregunta
    agregar_pregunta_modo = False
    pregunta_datos = {}
    claves_pregunta = ["pregunta", "respuesta1", "respuesta2", "respuesta3", "respuesta4", "indice respuesta correcta"]
    indice_clave_actual = 0  # Para rastrear qué clave se está ingresando actualmente

    # Definir los rectángulos donde se pueden hacer clic
    rectangulo_vidas = pygame.Rect(150, 100, ANCHO_RECTANGULO_RESPUESTA, ALTO_RECTANGULO_RESPUESTA)
    rectangulo_puntos = pygame.Rect(150, 200, ANCHO_RECTANGULO_RESPUESTA, ALTO_RECTANGULO_RESPUESTA)
    rectangulo_tiempo = pygame.Rect(150, 300, ANCHO_RECTANGULO_RESPUESTA, ALTO_RECTANGULO_RESPUESTA)
    rectangulo_preguntas = pygame.Rect(150, 400, ANCHO_RECTANGULO_RESPUESTA, ALTO_RECTANGULO_RESPUESTA)

    while bandera:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                bandera = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if rectangulo_vidas.collidepoint(mouse_pos):
                    escribiendo = True
                    atributo_seleccionado = "vidas"
                    entrada_texto = ""  # Limpiar entrada
                elif rectangulo_puntos.collidepoint(mouse_pos):
                    escribiendo = True
                    atributo_seleccionado = "puntos"
                    entrada_texto = ""
                elif rectangulo_tiempo.collidepoint(mouse_pos):
                    escribiendo = True
                    atributo_seleccionado = "tiempo"
                    entrada_texto = ""
                elif rectangulo_preguntas.collidepoint(mouse_pos):
                    agregar_pregunta_modo = True
                    pregunta_datos = {}
                    indice_clave_actual = 0
                    entrada_texto = ""
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    bandera = False

            if escribiendo and evento.type == pygame.TEXTINPUT:
                if entrada_texto == "" or atributo_seleccionado != "indice respuesta correcta":
                    entrada_texto += evento.text

            if escribiendo and evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE and len(entrada_texto) > 0:
                    entrada_texto = entrada_texto[:-1]
                elif evento.key == pygame.K_RETURN and entrada_texto:
                    config[atributo_seleccionado] = int(entrada_texto)
                    guardar_configuracion(ruta_csv, config)
                    escribiendo = False
                    atributo_seleccionado = None
                    entrada_texto = ""

            if agregar_pregunta_modo and evento.type == pygame.TEXTINPUT:
                entrada_texto += evento.text

            if agregar_pregunta_modo and evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE and len(entrada_texto) > 0:
                    entrada_texto = entrada_texto[:-1]
                elif evento.key == pygame.K_RETURN:
                    clave_actual = claves_pregunta[indice_clave_actual]
                    pregunta_datos[clave_actual] = entrada_texto
                    entrada_texto = ""
                    indice_clave_actual += 1

                    # Comprobar si ya se ingresaron todos los datos
                    if indice_clave_actual >= len(claves_pregunta):
                        agregar_pregunta(pregunta_datos, ruta_preguntas)
                        agregar_pregunta_modo = False
                        pregunta_datos = {}
                        indice_clave_actual = 0

        # Dibujar elementos en pantalla
        pantalla.fill(ANTIQUEWHITE)

        # Dibujar los rectángulos y texto de vidas, puntos y tiempo
        pygame.draw.rect(pantalla, PLUM2, rectangulo_vidas)
        texto_vidas, coordenadas_vidas = centrar_texto(f"VIDAS: {config['vidas']}", fuente, BLACK, rectangulo_vidas)
        pantalla.blit(texto_vidas, coordenadas_vidas)

        pygame.draw.rect(pantalla, PLUM2, rectangulo_puntos)
        texto_puntos, coordenadas_puntos = centrar_texto(f"PUNTOS: {config['puntos']}", fuente, BLACK, rectangulo_puntos)
        pantalla.blit(texto_puntos, coordenadas_puntos)

        pygame.draw.rect(pantalla, PLUM2, rectangulo_tiempo)
        texto_tiempo, coordenadas_tiempo = centrar_texto(f"TIEMPO: {config['tiempo']}", fuente, BLACK, rectangulo_tiempo)
        pantalla.blit(texto_tiempo, coordenadas_tiempo)

        pygame.draw.rect(pantalla, PLUM2, rectangulo_preguntas)
        texto_preguntas, coordenadas_preguntas = centrar_texto("AÑADIR PREGUNTA", fuente, BLACK, rectangulo_preguntas)
        pantalla.blit(texto_preguntas, coordenadas_preguntas)

        if escribiendo and atributo_seleccionado:
            texto_ingreso = fuente.render(f"Editando {atributo_seleccionado}: {entrada_texto}", True, BLACK)
            pantalla.blit(texto_ingreso, (150, 500))

        if agregar_pregunta_modo:
            clave_actual = claves_pregunta[indice_clave_actual]
            texto_ingreso = fuente.render(f"Ingrese {clave_actual}: {entrada_texto}", True, BLACK)
            pantalla.blit(texto_ingreso, (150, 500))

        pygame.display.flip()
