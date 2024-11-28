import pygame
import random  # Import necesario para randint
from funciones import *
from colores import *
from constantes import *
import pygame.mixer as mixer
import csv
import sys
from sonidos import *

def jugar() -> None:
    """
    Ejecuta la lógica principal del juego de preguntas y respuestas utilizando Pygame.

    La función controla el flujo del juego, incluyendo la selección de preguntas, el manejo de respuestas,
    la gestión del temporizador, y la interacción del usuario. Tambien, guarda los resultados del jugador
    en el archivo csv de ranking al finalizar.

    Args:
        None

    Returns:
        None
    """

    # Carga de la matriz de preguntas
    matriz_preguntas = crear_matriz("preguntas.csv")
    lista_preguntadas = []

    # Carga de la matriz configuración
    matriz_configuracion = crear_matriz("configuracion.csv")

    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    # Configuración inicial
    fuente = pygame.font.Font("assets/BebasNeue-Regular.ttf", 30)
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Jugando")

    # Variables de estado
    puntos = 0
    puntos_por_pregunta_acertada = int(matriz_configuracion[0][0])  
    respuestas_acertadas = 0
    vidas = int(matriz_configuracion[0][1]) 
    tiempo_por_pregunta = int(matriz_configuracion[0][2])  
    tiempo_total = 0
    bandera = True
    pregunta_actual = None
    respuestas_actuales = []
    respuesta_correcta = None
    usuario = ""

    diccionario_jugador = {
        "usuario": usuario,
        "puntos": puntos,
        "respuestas correctas": respuestas_acertadas,
        "tiempo total": tiempo_total,
    }

    # Temporizador para las preguntas (en segundos)
    tiempo_restante = tiempo_por_pregunta
    tiempo_anterior = pygame.time.get_ticks()  # Guarda el tiempo al inicio de cada ciclo

    # Bucle principal del juego
    while bandera:  # Mientras queden vidas
        if pregunta_actual is None  and len(lista_preguntadas) < len(matriz_preguntas):
            pregunta_actual, respuestas_actuales, respuesta_correcta = seleccionar_pregunta(matriz_preguntas, lista_preguntadas)
            tiempo_restante = tiempo_por_pregunta
            tiempo_anterior = pygame.time.get_ticks()  # Reiniciar el temporizador con la nueva pregunta
        elif len(lista_preguntadas) >= len(matriz_preguntas):  # Todas las preguntas han sido contestadas
        # Se terminó el juego, sin más preguntas
            bandera = True
            break
            
            
        # Captura eventos
        lista_eventos = pygame.event.get()
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                bandera = False
                vidas = 0
                break

            if vidas > 0:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    # Captura la posición del clic
                    mouse_pos = pygame.mouse.get_pos()

                    # Definir rectángulos
                    rectangulos = {
                        1: rectangulo_respuesta_1,
                        2: rectangulo_respuesta_2,
                        3: rectangulo_respuesta_3,
                        4: rectangulo_respuesta_4,
                    }

                    # Validar clic en los rectángulos
                    respuesta = validar_rectangulo(mouse_pos, rectangulos)

                    # Si se seleccionó una respuesta, validar si es correcta
                    if respuesta is not None:
                        if respuesta == respuesta_correcta:
                            print("¡Respuesta correcta!")
                            puntos += puntos_por_pregunta_acertada
                            respuestas_acertadas += 1
                            reproducir_correcto()
                        else:
                            print("Respuesta incorrecta.")
                            vidas -= 1
                            reproducir_incorrecto()

                        # Reiniciar para mostrar una nueva pregunta
                        pregunta_actual = None
                    
            elif vidas <= 0:
                escribiendo_nombre = True  # Activar escritura del nombre
                if evento.type == pygame.TEXTINPUT and escribiendo_nombre:
                    usuario += evento.text  # Agregar el texto ingresado
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_BACKSPACE and len(usuario) > 0:
                        usuario = usuario[:-1]  # Borrar el último carácter

        if vidas > 0:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - tiempo_anterior >= 1000:  
                tiempo_restante -= 1  
                tiempo_total += 1
                print(tiempo_total)
                tiempo_anterior = tiempo_actual 

        # Si se acabó el tiempo, descontamos una vida y mostramos la siguiente pregunta
        if tiempo_restante <= 0:
            print("Se acabó el tiempo!")
            vidas -= 1
            pregunta_actual = None
            tiempo_restante = tiempo_por_pregunta  # Reiniciar el temporizador

        # Dibujar la interfaz
        pantalla.fill(ANTIQUEWHITE3)
        if vidas > 0:
            minutos = tiempo_total // 60  # División entera para obtener minutos
            """"
            Usamos la división entera (//) para calcular cuántos minutos completos hay en el total de segundos.

            Usamos el módulo (%) para obtener los segundos restantes después de dividir el total de segundos en minutos completos.
            """

            segundos = tiempo_total % 60  # Módulo para obtener los segundos restantes

            # Formatear minutos y segundos para que siempre tengan dos dígitos
            minutos_formateados = f"0{minutos}" if minutos < 10 else str(minutos)
            segundos_formateados = f"0{segundos}" if segundos < 10 else str(segundos)
            tiempo_formateado = f"{minutos_formateados}:{segundos_formateados}"

            # Rectángulo de la pregunta
            rectangulo_pregunta = pygame.draw.rect(pantalla, BEIGE, (50, 20, ANCHO_RECTANGULO_PREGUNTA, ALTO_RECTANGULO_PREGUNTA))

            # Rectángulos de las respuestas
            rectangulo_respuesta_1 = pygame.draw.rect(pantalla, BEIGE, (150, 100, ANCHO_RECTANGULO_RESPUESTA, ALTO_RECTANGULO_RESPUESTA))
            rectangulo_respuesta_2 = pygame.draw.rect(pantalla, BEIGE, (150, 200, ANCHO_RECTANGULO_RESPUESTA, ALTO_RECTANGULO_RESPUESTA))
            rectangulo_respuesta_3 = pygame.draw.rect(pantalla, BEIGE, (150, 300, ANCHO_RECTANGULO_RESPUESTA, ALTO_RECTANGULO_RESPUESTA))
            rectangulo_respuesta_4 = pygame.draw.rect(pantalla, BEIGE, (150, 400, ANCHO_RECTANGULO_RESPUESTA, ALTO_RECTANGULO_RESPUESTA))

            # Dibujar texto de la pregunta
            if pregunta_actual:
                texto_pregunta, coordenadas_pregunta = centrar_texto(pregunta_actual, fuente, BLACK, rectangulo_pregunta)
                pantalla.blit(texto_pregunta, coordenadas_pregunta)

            # Dibujar texto de las respuestas
            rectangulos_respuestas = [
                rectangulo_respuesta_1,
                rectangulo_respuesta_2,
                rectangulo_respuesta_3,
                rectangulo_respuesta_4,
            ]

            for i in range(len(respuestas_actuales)):  # Iterar usando índices
                texto_respuesta, coordenadas_respuesta = centrar_texto(respuestas_actuales[i], fuente, BLACK, rectangulos_respuestas[i])
                pantalla.blit(texto_respuesta, coordenadas_respuesta)

            # Dibujar el tiempo restante
            tiempo_texto = fuente.render(f"Tiempo restante: {tiempo_restante} s", True, BLACK)
            pantalla.blit(tiempo_texto, (0,550))

        else:
            pantalla.fill(BLACK)

            imagen_perdiste = pygame.image.load("assets/GAME_OVER3.png")
            sonido_reproducido = False  

            if not sonido_reproducido:  # Solo se reproduce si aún no se ha hecho
                reproducir_sonido_gameover()
                sonido_reproducido = True
            
            pantalla.blit(imagen_perdiste, (120, 0, ANCHO_VENTANA, ALTO_VENTANA))
            
            escribiendo_nombre = True
            while escribiendo_nombre:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        bandera = False
                        escribiendo_nombre = False  # Salir también del bucle de escritura
                    elif evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_ESCAPE:
                            bandera = False  # Salir del juego
                            escribiendo_nombre = False  # Salir de este bucle
                        elif evento.key == pygame.K_BACKSPACE and len(usuario) > 0:
                            usuario = usuario[:-1]  # Borrar último carácter
                        elif evento.key == pygame.K_RETURN and usuario.strip() != "":
                            escribiendo_nombre = False  # Salir de este bucle si el nombre no está vacío
                            bandera = False
                    elif evento.type == pygame.TEXTINPUT:
                        usuario += evento.text  # Agregar texto ingresado

                # Dibujar pantalla mientras escribe
                pantalla.fill(BLACK)
                pantalla.blit(imagen_perdiste, (120, 0, ANCHO_VENTANA, ALTO_VENTANA))

                # Mostrar rectángulo para ingresar el nombre
                rectangulo_nombre = pygame.draw.rect(pantalla, YELLOW1, (150, 400, ANCHO_RECTANGULO_RESPUESTA, ALTO_RECTANGULO_RESPUESTA))
                texto_ingrese_nombre = fuente.render("Ingrese su nombre:", True, WHITE)
                pantalla.blit(texto_ingrese_nombre, (150, 360))

                # Mostrar el texto ingresado
                texto_usuario = fuente.render(usuario, True, BLACK)
                pantalla.blit(texto_usuario, (rectangulo_nombre.x + 10, rectangulo_nombre.y + 10))
                pygame.display.flip()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    bandera = False

        # Actualizar pantalla
        pygame.display.flip()
        pygame.display.update()

    diccionario_jugador['usuario'] = usuario
    diccionario_jugador['puntos'] = puntos
    diccionario_jugador['respuestas correctas'] = respuestas_acertadas
    diccionario_jugador['tiempo total'] = tiempo_formateado

    guardar_top10(diccionario_jugador,"ranking.csv")

    pygame.display.flip()
    
    return