import sys
from visuales import *
import pygame
import json
from random import choice, randint, shuffle
import re


# Premios
premios = [100,200,300,500,1000,2000,4000,8000,15000,30000,50000,100000,250000,500000,1000000]



def crear_menu() -> bool:
    """
    Crea el menú principal del juego.

    Retorna:
    bool: Verdadero si el juego debe comenzar, de lo contrario no retorna.
    
    """
    
    musica_menu = sonidos("sonidos\Quien_Quiere_Ser_Millonario.mp3")

    MENU = crear_ventana(icono, "Menu",(900,500))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.Sound.stop(musica_menu)
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                if rectangulo_empezar.collidepoint(x, y):
                    pygame.mixer.Sound.stop(musica_menu)
                    return True
        
        MENU.blit(imagen_fondo, [0,0])
        rectangulo_empezar = MENU.blit(imagen_start, [10, 400])
        
        pygame.display.update()
        
        
        

def cargar_preguntas(path, encoding="utf8") -> dict:
    """
    Carga preguntas desde un archivo JSON y las devuelve como un diccionario.

    Parámetros:
    ruta_archivo: La ruta al archivo JSON.
    encoding: La codificación del archivo ("utf8").

    Retorna:
    dict: Un diccionario con las preguntas cargadas.
    
    """
    with open(path, "r", encoding=encoding) as archivo:
        preguntas = json.load(archivo)
    
    return preguntas        


def mostrar_pantalla_inicio(pantalla: pygame.Surface, color: tuple, pregunta: dict, premios: list, i: int):
    """
    Esta función muestra la pantalla con la pregunta, opciones y premios actuales.

    Parámetros:
    pantalla: La superficie de Pygame donde se dibujará.
    color: El color del rectángulo.
    pregunta: El diccionario con la pregunta y opciones.
    premio: La lista de premios.
    i: El índice del premio actual.

    """



    dibujar_rectangulo(pantalla, color, 100, 250, 600, 30, 0) # pregunta
    dibujar_rectangulo(pantalla, color, 100, 350, 200, 30, 0)
    dibujar_rectangulo(pantalla, color, 600, 350, 200, 30, 0)
    dibujar_rectangulo(pantalla, color, 100, 450, 200, 30, 0)
    dibujar_rectangulo(pantalla, color, 600, 450, 200, 30, 0)
    mostrar_opciones_preguntas(pantalla, pregunta["opciones"], pregunta)
    #mostrar_premios(pantalla, premios[i], 20, 300)

    #Mientras que el indice sea menor a 15. lo muestra
    if i < len(premios):
        mostrar_premios(pantalla, premios[i], 20, 300)
    else:
        print(f"Índice {i} fuera de rango para la lista de premios.")



def mostrar_mensaje(pantalla: pygame.Surface, mensaje: str, pos_x: int, pos_y: int, color: tuple, tamaño: int, fuente: str) -> None: #Si no defino la pantalla como pygame no me deja aplicar el blit   
    """
    Muestra un mensaje en la pantalla.

    Parámetros:
    pantalla: La superficie de Pygame donde se va a dibujar.
    mensaje: El mensaje a mostrar.
    pos_x: La posición x del mensaje.
    pos_y: La posición y del mensaje.
    color: El color del texto.
    tamaño: El tamaño de la fuente.
    fuente: El tipo de fuente.
    """
    fuente = pygame.font.SysFont(fuente, tamaño)
    mensaje = fuente.render(mensaje,  0 , color)

    pantalla.blit(mensaje, (pos_x, pos_y))


    

def mostrar_rectangulo_temporal(pantalla: pygame.Surface, color: tuple, x: int, y: int, width: int, height: int, grosor: int, tiempo_inicio: int, duracion: int, mensaje="") -> bool:
    """
    Muestra un rectángulo en la pantalla temporalmente.

    Parámetros:
    pantalla: La superficie de Pygame donde se dibujará.
    color: El color del rectángulo en RGB.
    x: La posición x del rectángulo.
    y: La posición y del rectángulo.
    width: El ancho del rectángulo.
    height: La altura del rectángulo.
    grosor: El grosor del borde del rectángulo.
    tiempo_inicio: El tiempo inicial en milisegundos.
    duracion: La duración en milisegundos.

    Retorna:
    bool: Verdadero si el rectángulo debe seguir mostrándose, de lo contrario, devuelve falso.
    """
    tiempo_actual = pygame.time.get_ticks()
    mostrar_recangulo = tiempo_actual - tiempo_inicio < duracion
    if mostrar_recangulo:
        dibujar_rectangulo(pantalla, color, x, y, width, height, grosor)
        if mensaje:
            mostrar_mensaje(pantalla, mensaje, x + 10, y + 10, NEGRO, 20, "Arial Black")
        
    return mostrar_recangulo
    

def mostrar_opciones_preguntas(pantalla: pygame.Surface, opciones: list, pregunta: dict) -> None:
    """
    Muestra las opciones de la pregunta en la pantalla.

    Parámetros:
    pantalla: La superficie de Pygame donde se dibuja el texto.
    opcion: texto de la opción a mostrar
    pregunta: El diccionario con la pregunta y opciones.
    
    x, y: coordenadas donde se coloca el texto en la pantalla
    
    """
    mostrar_mensaje(pantalla, pregunta["pregunta"], 100, 250, NEGRO, 15, "Arial Black")

    posiciones_de_respuestas = [(100, 350), (600, 350), (100, 450), (600, 450)]
    for opcion, (x, y) in zip(opciones, posiciones_de_respuestas):
        mostrar_mensaje(pantalla, opcion, x, y, BLANCO, 15, "Arial Black")

def mostrar_premios(pantalla: pygame.Surface, valor_premio: int, x: int, y: int) -> None:
    """
    Muestra la lista de premios en la pantalla.

    Parámetros:
    pantalla: La superficie de Pygame donde se dibujará.
    valor_premio: El valor del premio actual.
    x: La posición x de la lista de premios.
    y: La posición y de la lista de premios.
    """    
    for premio in premios:
        premio = str(premio)
        if valor_premio == int(premio):
            color_texto = ROJO
        else:
            color_texto = BLANCO
        
        mostrar_mensaje(pantalla, f"{premio}" , x, y, color_texto, 20, "Arial Black")
        y -= 20


#MODIFICAR ESTA FUNCIÓN QUE RETORNA DOS VECES, TIENE QUE RETORNAR UNA SOLA VEZ
def seleccionar_los_click_de_respuesta(event: pygame.event.Event, rectangulos_respuestas: list) -> int:
    """
    Determina cuál respuesta ha sido seleccionada con un click.

    Parámetros:
    event (pygame.event.Event): El evento de Pygame.
    rectangulos_respuestas (list): La lista de rectángulos de respuestas.

    Retorna:
    int: El índice de la respuesta seleccionada (0, 1, 2, 3).
    """
    for i in range(len(rectangulos_respuestas)):
        rectangulo = rectangulos_respuestas[i]
        
        # Verificar si el punto del evento de click está dentro del rectángulo
        if rectangulo.collidepoint(event.pos):
            return i  


def obtener_ultimo_premio(premios: list, i_actual: int) -> str:
    """
    Obtiene el último premio ganado.

    Parámetros:
    premios: La lista de premios.
    i_actual: El índice actual.

    Retorna:
    str: El valor del último premio ganado.
    """
    if i_actual > 0:
        ultimo_premio = premios[i_actual - 1]
    else:
        ultimo_premio = "$0"
    
    return ultimo_premio




def actualizar_posiciones_de_respuestas(pregunta_actual: dict) -> dict:
    """
    Actualiza las posiciones de las respuestas en la pantalla.

    Parámetros:
    pregunta_actual (dict): El diccionario con la pregunta y opciones.

    Retorna:
    dict: Un diccionario con las posiciones de cada respuesta.
    """
    dict_de_posiciones_de_preguntas = {
        pregunta_actual["opciones"][0]: (100, 350),
        pregunta_actual["opciones"][1]: (600, 350),
        pregunta_actual["opciones"][2]: (100, 450),
        pregunta_actual["opciones"][3]: (600, 450)
    }
    return dict_de_posiciones_de_preguntas






def gestionar_tiempo(tiempo_inicial: int, duracion_maxima: int) -> int:
    """
    Gestiona el tiempo restante para responder.

    Parámetros:
    tiempo_inicial: El tiempo inicial en milisegundos.
    duracion_maxima: La duración máxima en milisegundos.

    Retorna:
    int: El tiempo restante en milisegundos.
    """
    tiempo_actual = pygame.time.get_ticks()
    tiempo_restante = max(tiempo_inicial - tiempo_actual, 0)
    return tiempo_restante



#Archivo CSV

def guardar_partida(premio:int):
    """
    Guarda el nombre y el premio del jugador.
    Exepcion = Por si el archivo no se encuentra
    
    Parametro = El premio que gano el jugador
    """
    
    try:
        jugador = cargar_nombre_premio(premio)
        
        with open("partidas.csv", "a", encoding="UTF8") as archivo:
            mensaje = (f"El jugador:  {jugador["nombre"]}, Gano un total de: ${jugador["dinero_acumulado"]} \n")
            archivo.write(mensaje)
    except FileNotFoundError:
        print("Error el archivo no existe")


def cargar_nombre_premio(premio:int):
    """
    Carga el nombre y el premio del jugador.
    Parametro = El puntaje que logro el jugador
    
    Retorno = El Jugador con el premio
    """
    nombre_ingresado = input(f"Fin. Terminaste el juego, ganaste {premio}! \n Ingrese su nombre para guardarlo en la tabla de puntaciones: ")
    jugador = {}
    if nombre_ingresado != None and len(nombre_ingresado) != 0:
        if type(nombre_ingresado) == str:
            nombre_ingresado = re.sub("/", " ", nombre_ingresado)
            nombre_ingresado = nombre_ingresado.strip()
            jugador["nombre"] = nombre_ingresado
    else:
        jugador["nombre"] = "incognito"
    jugador["dinero_acumulado"] = premio
    return jugador

jugador = {
    "nombre": " ",
    "dinero_acumulado":0,
}