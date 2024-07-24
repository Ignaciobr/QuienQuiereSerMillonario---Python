import pygame


pygame.mixer.init()
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
VERDE_OSCURO = (0, 100, 0)
AZUL_CLARO = (0, 150, 255)
VIOLETA_CLARO = (90,30,218)




icono = pygame.image.load(r"img\Who-wants-to-be-a-millionaire-winners.webp")

imagen_50_50 = pygame.image.load(r"img\comodin_de_50_y_50.webp")
imagen_50_50 = pygame.transform.scale(imagen_50_50, (100, 100))

imagen_publico = pygame.image.load(r"img\comodin_de_publico.webp")
imagen_publico = pygame.transform.scale(imagen_publico, (100,100))

imagen_llamada = pygame.image.load(r"img\comodin_de_llamada.webp")
imagen_llamada = pygame.transform.scale(imagen_llamada, (100,100))

imagen_fondo = pygame.image.load(r"img\fondo_de_presentacion_del_juego.webp")
imagen_fondo = pygame.transform.scale(imagen_fondo, (900,500))

imagen_preguntas = pygame.image.load(r"img\fondo_preguntas.png")
imagen_preguntas = pygame.transform.scale(imagen_preguntas, (900,500))

imagen_start = pygame.image.load(r"img\start.png")
imagen_start = pygame.transform.scale(imagen_start, (200,100))


def crear_ventana(icono: pygame.Surface, titulo: str, tamaño: tuple) -> pygame.Surface:
    """
    Crea una ventana de Pygame.

    Parámetros:
    icono: La superficie del icono de la ventana.
    titulo: El título de la ventana.
    tamaño: Un tuple que contiene el ancho y el alto de la ventana.

    Retorna:
    pygame.Surface: La superficie de la ventana creada.
    """
    ventana = pygame.display.set_mode(tamaño) 
    pygame.display.set_caption(titulo) 
    pygame.display.set_icon(icono)

    return ventana
    

def dibujar_rectangulo(pantalla: pygame.Surface, color, x, y, width, height, grosor):
    """
    Dibuja un rectangulo en la pantalla

    Args:
        pantalla (pygame.Surface): Pantalla del juego
        color (tupla): Un color
        x (int): Posicion del eje x
        y (int): posicion del eje y
        width (int): Ancho del rectangulo
        height (int): Alto del rectangulo
        grosor (int): Grosor del rectangulo

    Returns:
        Retorna el rectangulo
    """
    rectangulo = pygame.Rect(x, y, width, height)
    pygame.draw.rect(pantalla, color, rectangulo, grosor)
    return rectangulo


def sonidos(path:str):
    """
    
    Funcion para cargar el sonido

    Parametros :
    path : pantalla
    """
    sonido = pygame.mixer.Sound(path)
    sonido.set_volume(0.1)
    sonido.play(-1)
    return sonido