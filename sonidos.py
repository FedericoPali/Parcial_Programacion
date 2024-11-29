import pygame
pygame.mixer.init()

def cargar_sonido(ruta: str, volumen: float = 0.5) -> pygame.mixer.Sound:
    """
    Carga un archivo de sonido y ajusta su volumen.

    Args:
        ruta (str): Ruta al archivo de sonido que se desea cargar.
        volumen (float, optional): Volumen del sonido (rango de 0.0 a 1.0). Default: 0.5.

    Returns:
        pygame.mixer.Sound: Objeto de sonido cargado y configurado.
    """

    sonido = pygame.mixer.Sound(ruta)
    sonido.set_volume(volumen)  # Ajustar volumen del sonido
    return sonido

def reproducir_correcto() -> None:
    """
    Reproduce el efecto de sonido cuando la respuesta es correcta.

    Args:
        None

    Returns:
        None
    """

    sonido_correcto.play()

def reproducir_incorrecto() -> None:
    """
    Reproduce el efecto de sonido cuando la respuesta es incorrecta.

    Args:
        None

    Returns:
        None
    """

    sonido_incorrecto.play()

def reproducir_sonido_gameover() -> None:
    """
    Reproduce el efecto de sonido cuando se llega al fin del juego, si el jugador pierde sus vidas.

    Args:
        None

    Returns:
        None
    """

    game_over_sonido.play()

def reproducir_sonido_winner() -> None:
    """
    Reproduce el efecto de sonido cuando se llega al fin del juego, si el ganador acaba con las preguntas.

    Args:
        None

    Returns:
        None
    """
    winner_sonido.play()

sonido_correcto = cargar_sonido("sonidos/correcto.mp3", volumen = 0.3)
sonido_incorrecto = cargar_sonido("sonidos/incorrecto.mp3", volumen = 0.3)
game_over_sonido = cargar_sonido("sonidos/game over.mp3", volumen = 0.3)
winner_sonido = cargar_sonido("sonidos/ganador.mp3", volumen = 0.3)