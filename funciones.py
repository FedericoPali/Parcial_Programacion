import csv
import random
import os
import pygame
import sys

def crear_rectangulo(pantalla: pygame.Surface, color: tuple, x: int, y: int, ancho: int, alto: int) -> pygame.Rect:
    """Crea un rectángulo en la pantalla con los parámetros especificados.

    Args:
        pantalla (pygame.Surface): La pantalla en la cual se va a mostrar el rectángulo.
        color (tuple): Color del rectángulo (formato RGB).
        x (int): Posición x del rectángulo.
        y (int): Posición y del rectángulo.
        ancho (int): Ancho del rectángulo.
        alto (int): Alto del rectángulo.

    Returns:
        pygame.Rect: Objeto que representa el rectángulo dibujado.
    """

    return pygame.draw.rect(pantalla, color, (x, y, ancho, alto))

def centrar_texto(texto: str, fuente, color: tuple, forma: pygame.Rect) -> tuple:
    """
    Centra un texto dentro de una forma dada.

    Args:
        texto (str): El texto que se desea centrar.
        fuente (pygame.font.Font): Fuente utilizada para renderizar el texto.
        color (tuple): Color del texto en formato RGB.
        forma (pygame.Rect): Forma en la cual se centrará el texto.

    Returns:
        tuple: Una tupla que contiene la superficie renderizada del texto (`pygame.Surface`) 
        y el rectángulo centrado (`pygame.Rect`).
    """

    superficie_texto = fuente.render(texto, True, color)
    coordenadas_centro = superficie_texto.get_rect(center=forma.center)
    return superficie_texto, coordenadas_centro

def seleccionar_pregunta(matriz_preguntas: list, lista_preguntadas: list) -> tuple:
    """
    Selecciona una pregunta al azar de una matriz, asegurando que no se repita.

    Args:
        matriz_preguntas (list): Matriz de preguntas, donde cada fila contiene una pregunta, 
        sus opciones y la respuesta correcta.
        lista_preguntadas (list): Lista de preguntas ya realizadas para evitar repeticiones.

    Returns:
        tuple: Una tupla con la pregunta (str), las opciones (list) y el índice de la respuesta correcta (int).
    """

    while True:
        indice_random = random.randint(0, len(matriz_preguntas) - 1)
        pregunta = matriz_preguntas[indice_random][0]

        # Verificar si la pregunta ya se realizó
        if pregunta not in lista_preguntadas:
            lista_preguntadas.append(pregunta)  # Marcar como preguntada
            opciones = matriz_preguntas[indice_random][1:5]  # Las 4 respuestas
            correcta = int(matriz_preguntas[indice_random][-1])  # Índice de la respuesta correcta
            return pregunta, opciones, correcta

def validar_rectangulo(mouse_pos: tuple, rectangulos: dict) -> int:
    """
    Verifica en qué rectángulo ocurrió un clic basado en la posición del mouse.

    Args:
        mouse_pos (tuple): Coordenadas del mouse al hacer clic (x, y).
        rectangulos (dict): Diccionario con los rectángulos (`pygame.Rect`) como valores 
        y sus índices como claves.

    Returns:
        int: Índice del rectángulo donde ocurrió el clic, o `None` si no hubo colisión.
    """

    for indice, rect in rectangulos.items():
        if rect.collidepoint(mouse_pos):
            return indice
    return None
    
def crear_matriz(csv_a_transformar: str) -> list:
    """
    Lee un archivo CSV y lo convierte en una lista de listas, excluyendo el encabezado.

    Args:
        csv_a_transformar (str): Ruta al archivo CSV.

    Returns:
        list: Matriz que contiene los datos del archivo CSV (sin el encabezado).
    """

    matriz = []
    with open(csv_a_transformar, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)  
        encabezado = False
        for fila in lector:
            if not encabezado:  
                encabezado = True
                continue
            matriz.append(fila)
    return matriz

def mostrar_matriz(matriz: list) -> None:
    """
    Muestra en consola los datos de una matriz, con elementos separados por '|'.

    Args:
        matriz (list): Matriz de datos a mostrar.

    Returns:
        None
    """

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(matriz[i][j], end = " | ")
        print("")

def validar_respuesta(respuesta: int, respuesta_correcta: int) -> bool:
    """
    Verifica si una respuesta proporcionada es correcta.

    Args:
        respuesta (int): Respuesta seleccionada.
        respuesta_correcta (int): Respuesta correcta esperada.

    Returns:
        bool: `True` si la respuesta es correcta, `False` en caso contrario.
    """

    retorno = False

    if respuesta == respuesta_correcta:
        retorno = True

    return retorno

def cargar_configuracion(ruta_csv: str) -> dict:
    """
    Carga la configuración inicial desde un archivo CSV.

    Args:
        ruta_csv (str): Ruta al archivo de configuración.

    Returns:
        dict: Diccionario con los valores de configuración ('puntos', 'vidas', 'tiempo').
    """

    if not os.path.exists(ruta_csv):  # Verifica si el archivo existe
        print(f"El archivo {ruta_csv} no existe.")
        sys.exit()  # Termina el programa si no se encuentra el archivo

    with open(ruta_csv, mode="r") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            return {  
                "puntos": int(fila["puntos"]),
                "vidas": int(fila["vidas"]),
                "tiempo": int(fila["tiempo"])
            }
    
    print(f"No se pudieron leer los datos del archivo {ruta_csv}.")
    sys.exit()  # Terminar el programa si no se pueden leer los datos

def guardar_configuracion(ruta_csv: str, configuracion: dict) -> None:
    """
    Guarda los valores de configuración en un archivo CSV.

    Args:
        ruta_csv (str): Ruta al archivo de configuración.
        configuracion (dict): Diccionario con los valores a guardar ('puntos', 'vidas', 'tiempo').

    Returns:
        None
    """

    if not os.path.exists(ruta_csv):  # Verifica si el archivo existe
        print(f"El archivo {ruta_csv} no existe.")
        sys.exit()  # Termina el programa si no se encuentra el archivo

    with open(ruta_csv, mode="r") as archivo:
        lector = csv.DictReader(archivo)
        filas = list(lector)  # Leer todo el contenido

    # Modificar la fila con la nueva configuración
    for fila in filas:
        fila["puntos"] = configuracion["puntos"]
        fila["vidas"] = configuracion["vidas"]
        fila["tiempo"] = configuracion["tiempo"]

    # Sobrescribir el archivo con los cambios
    with open(ruta_csv, mode="w", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=["puntos", "vidas", "tiempo"])
        escritor.writeheader()  # Escribir el encabezado
        escritor.writerows(filas)  # Escribir las filas con los nuevos valores

def jugar_codeado(preguntas: list, tiempo_limite: int = 60, puntos_por_respuesta: int = 1, vidas: int = 3) -> dict:
    """
    Implementa la lógica principal del juego, manejando preguntas, respuestas y puntuación.

    Args:
        preguntas (list): Lista de preguntas, cada una con sus opciones y respuesta correcta.
        tiempo_limite (int, optional): Tiempo límite para responder. Default: 60.
        puntos_por_respuesta (int, optional): Puntos otorgados por cada respuesta correcta. Default: 1.
        vidas (int, optional): Número inicial de vidas. Default: 3.

    Returns:
        dict: Diccionario con los resultados del jugador ('usuario', 'respuestas correctas').
    """

    puntos = 0
    lista_preguntadas = []
    respuesta_acertada = 0
    while vidas > 0:
        # Seleccionar una pregunta al azar
        indice_random = random.randint(0, len(preguntas) - 1)
        pregunta_a_realizar = preguntas[indice_random][0]

        # Verificamos que la pregunta no se haya preguntado antes
        while pregunta_a_realizar in lista_preguntadas:
            indice_random = random.randint(0, len(preguntas) - 1)
            pregunta_a_realizar = preguntas[indice_random][0]

        # Agregar la pregunta a la lista de preguntas ya realizadas
        lista_preguntadas.append(pregunta_a_realizar)

        # Mostrar la pregunta
        print(pregunta_a_realizar)
        for i in range(1, len(preguntas[indice_random]) - 1):  # Opciones están antes de la respuesta
            print(f"{i}: {preguntas[indice_random][i]}")
        
        # Obtener la respuesta correcta (último elemento del sublistado)
        respuesta_correcta = int(preguntas[indice_random][-1])  

        # Pedir respuesta al usuario
        respuesta_usuario = int(input("Cual es la respuesta?: "))
        
        # Validar respuesta
        respuesta_validada = validar_respuesta(respuesta_usuario, respuesta_correcta)
        
        if respuesta_validada == True:
            respuesta_acertada += 1
            puntos += puntos_por_respuesta
        else:
            vidas -= 1
            print(f"Total de vidas restantes: {vidas}")
    
    print("Juego terminado")
    nombre_jugador = input("Introduzca su nombre para el score: ")
    print(f"Jugador: {nombre_jugador} \nRespuestas correctas: {respuesta_acertada}")

    
    diccionario_jugador = {
        "usuario": nombre_jugador,
        "respuestas correctas": respuesta_acertada
    }
    
    return diccionario_jugador

def guardar_top10(diccionario: dict, path: str) -> None:
    """
    Guarda o actualiza el ranking de los 10 mejores jugadores en un archivo CSV.

    Args:
        diccionario (dict): Diccionario con la información del jugador ('usuario', 'respuestas correctas', 'tiempo total').
        path (str): Ruta al archivo CSV donde se almacenará el ranking.

    Returns:
        None
    """

    # Definir el encabezado
    encabezado = ["Usuario", "Respuestas correctas", "Tiempo total"]

    # Leer datos existentes del archivo
    datos = []
    
    # Verificar si el archivo existe
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            primera_fila = True  # Variable para identificar si estamos en la primera fila (encabezado)
            for fila in lector:
                if primera_fila:
                    primera_fila = False  # Ignoramos el encabezado
                    continue
                
                # Asegurar que la fila tiene 2 elementos y que la segunda columna es un número
                if len(fila) == 3 and fila[1].isdigit():  # Verificar si las respuestas correctas son numéricas
                    datos.append([fila[0], int(fila[1]),fila[2]])

    # Agregar el nuevo jugador al ranking
    nuevo_usuario = [diccionario["usuario"], diccionario["respuestas correctas"], diccionario["tiempo total"]]
    datos.append(nuevo_usuario)

    # Ordenar los datos en orden descendente por respuestas correctas
    for i in range(len(datos)):
        for j in range(0, len(datos) - i - 1):
            if datos[j][1] < datos[j + 1][1]:  # Comparar las respuestas correctas
                datos[j], datos[j + 1] = datos[j + 1], datos[j]

    # Limitar a los 10 mejores jugadores
    top10 = datos[:10]

    # Escribir el encabezado y los 10 mejores en el archivo
    with open(path, 'w', encoding='utf-8') as archivo:
        archivo.write(','.join(encabezado) + '\n')  # Escribir encabezado
        for fila in top10:
            archivo.write(','.join(map(str, fila)) + '\n')


def agregar_pregunta(diccionario: dict, path: str) -> None:
    """
    Agrega una nueva pregunta al archivo CSV. Si el archivo no existe, lo crea con el encabezado adecuado.

    Args:
        diccionario (dict): Diccionario con los datos de la nueva pregunta:
        ('pregunta', 'respuesta1', 'respuesta2', 'respuesta3', 'respuesta4', 
        'indice respuesta correcta').
        path (str): Ruta al archivo CSV donde se guardará la pregunta.

    Returns:
        None
    """
    # Encabezado esperado
    encabezado = ["pregunta", "respuesta1", "respuesta2", "respuesta3", "respuesta4", "indice respuesta correcta"]

    # Verificar si el archivo existe
    existe_archivo = os.path.exists(path)

    # Validar que el diccionario tiene todas las claves necesarias
    claves_necesarias = ["pregunta", "respuesta1", "respuesta2", "respuesta3", "respuesta4", "indice respuesta correcta"]
    for clave in claves_necesarias:
        if clave not in diccionario:
            print(f"Error: falta la clave '{clave}' en el diccionario.")
            return

    # Validar que el índice de la respuesta correcta es un número entre 1 y 4
    indice_correcto = diccionario["indice respuesta correcta"]
    if not str(indice_correcto).isdigit():
        print("Error: el índice de la respuesta correcta debe ser un número.")
        return
    indice_correcto = int(indice_correcto)
    if indice_correcto < 1 or indice_correcto > 4:
        print("Error: el índice de la respuesta correcta debe estar entre 1 y 4.")
        return

    # Escribir la pregunta en el archivo
    with open(path, 'a', encoding='utf-8', newline='') as archivo:
        escritor = csv.writer(archivo)

        # Si el archivo no existe, escribir el encabezado
        if not existe_archivo:
            escritor.writerow(encabezado)

        # Agregar la nueva pregunta
        nueva_pregunta = [
            diccionario["pregunta"],
            diccionario["respuesta1"],
            diccionario["respuesta2"],
            diccionario["respuesta3"],
            diccionario["respuesta4"],
            diccionario["indice respuesta correcta"],
        ]
        escritor.writerow(nueva_pregunta)
        print("Pregunta agregada correctamente.")


