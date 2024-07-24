import sys
from visuales import *
import pygame
import json
from random import choice, randint, shuffle

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

def aplicar_comodin_llamada(pantalla: pygame.Surface, respuesta_correcta: str) -> None:
    """
    Aplica el comodín llamada, mostrando la respuesta correcta como recomendación de una persona ficticia.

    Parámetros:
    pantalla (pygame.Surface): La superficie de Pygame donde se dibujará.
    respuesta_correcta (str): La respuesta correcta.
    """  
    mensaje = f"PEPITO: No estoy seguro pero para mí es la respuesta es {respuesta_correcta}"
    mostrar_mensaje(pantalla, mensaje, 100, 300, BLANCO, 20, "Arial Black")
    pygame.display.update()
    pygame.time.wait(3000)  


def aplicar_comodin_50_50(opciones: list, respuesta_correcta: str) -> list:
    """
    Aplica el comodín 50/50, eliminando dos respuestas incorrectas y dejan una respuesta correcta con otra incorrecta.

    Parámetros:
    opciones: La lista de opciones de respuesta.
    respuesta_correcta: La respuesta correcta.

    Retorna:
    list: La lista de opciones de respuesta actualizada.
    """
    incorrectas = []

    for opcion in opciones:
        if opcion != respuesta_correcta:
            incorrectas.append(opcion)
    
    if len(incorrectas) >= 2:
        incorrectas_a_eliminar = []
        
        while len(incorrectas_a_eliminar) < 2:
            incorrecta = choice(incorrectas)
            if incorrecta not in incorrectas_a_eliminar:
                incorrectas_a_eliminar.append(incorrecta)
    
        for incorrecta in incorrectas_a_eliminar:
            opciones.remove(incorrecta)
    
    return opciones


def aplicar_comodin_publico(opciones: list, respuesta_correcta: str) -> list:
    """
    Aplica el comodín "público" generando porcentajes sobre cuáles son las respuestas correctas.

    Parámetros:
    opciones: La lista de opciones de respuesta.
    respuesta_correcta: La respuesta correcta.

    Retorna:
    list: Una lista con los porcentajes de cada respuesta en el mismo orden que las opciones.
    """
    porcentajes = {}

    incorrectas = []
    for opcion in opciones:
        if opcion != respuesta_correcta:
            incorrectas.append(opcion)

    porcentajes[respuesta_correcta] = 60

    if len(incorrectas) >= 2:
        porcentajes[incorrectas[0]] = 30
        porcentajes[incorrectas[1]] = 5
        porcentajes[incorrectas[2]] = 5

    return porcentajes



def mostrar_porcentajes_publico(pantalla: pygame.Surface, porcentajes: dict, posiciones: dict) -> None:
    """
    Muestra los porcentajes sobre cuáles son las respuestas correctas.

    Parámetros:
    pantalla: La superficie de Pygame donde se dibujará.
    porcentajes: Un diccionario con los porcentajes de cada respuesta.
    posiciones: Un diccionario con las posiciones de cada respuesta.
    """
    for opcion, porcentaje in porcentajes.items():
        if opcion in posiciones:
            x, y = posiciones[opcion]
            mensaje = (f"{porcentaje}%")
            mostrar_mensaje(pantalla, mensaje, x + 100, y - 30, AZUL, 20, "Arial Black")

