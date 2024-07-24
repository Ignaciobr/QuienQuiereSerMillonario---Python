import pygame
from funciones import *
from visuales import * 
from comodines import *

pygame.init()

empezar = crear_menu()

clock = pygame.time.Clock()
PANTALLA = pygame.display.set_mode((900,500))
pygame.display.set_caption("Quien quiere ser millonario?")
pygame.display.set_icon(icono)

sonidos("sonidos\cancion_fondo_preguntas.mp3")

preguntas = cargar_preguntas("preguntas.json") 
shuffle(preguntas)
i = 0
pregunta_actual = preguntas[i] #Selecciona la primera pregunta para el comodin 50/50


tiempo_inicio = pygame.time.get_ticks() + 30 * 1000  # Tiempo inicial de 30 segundos por pregunta
duracion = 0
mostrar_rectangulo = False
seleccion_realizada = False
mostrar_porcentajes = False
mostrar_llamada = False


comodines = {
    "50-50": "se puede usar",
    "publico": "se puede usar",
    "llamada": "se puede usar"
}


rectangulo_respuesta_1 = dibujar_rectangulo(PANTALLA, BLANCO, 100, 350, 200, 50, 0)
rectangulo_respuesta_2 = dibujar_rectangulo(PANTALLA, BLANCO, 600, 350, 200, 50, 0)
rectangulo_respuesta_3 = dibujar_rectangulo(PANTALLA, BLANCO, 100, 450, 200, 50, 0)
rectangulo_respuesta_4 = dibujar_rectangulo(PANTALLA, BLANCO, 600, 450, 200, 50, 0)


rectangulos_respuestas = [
    rectangulo_respuesta_1,
    rectangulo_respuesta_2,
    rectangulo_respuesta_3,
    rectangulo_respuesta_4,
]

posiciones_de_respuestas = actualizar_posiciones_de_respuestas(pregunta_actual)

while empezar :
    PANTALLA.blit(imagen_preguntas, [0,0])
    
    tiempo_actual = pygame.time.get_ticks()

    tiempo_restante = gestionar_tiempo(tiempo_inicio, 30 * 1000)
    tiempo_segundos = tiempo_restante // 1000  # transformar  segundos a enteros
    tiempo_str = (f"Tiempo restante: {tiempo_segundos} s")

    if i < len(premios):
        mostrar_pantalla_inicio(PANTALLA, VIOLETA_CLARO, pregunta_actual, premios, i)
    
    
    if comodines["50-50"] == "se puede usar":
        PANTALLA.blit(imagen_50_50, [800,10])
    if comodines["publico"] == "se puede usar":
        PANTALLA.blit(imagen_publico, [650,10])
    if comodines["llamada"] == "se puede usar":
        PANTALLA.blit(imagen_llamada, [500,10])
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            empezar = False
            guardar_partida(obtener_ultimo_premio(premios, i))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not seleccion_realizada:
            
            x, y = pygame.mouse.get_pos()
            click_en_las_respuestas = seleccionar_los_click_de_respuesta(event, rectangulos_respuestas)
            
            if click_en_las_respuestas is not None:
                seleccion_realizada = True

                if pregunta_actual["opciones"][click_en_las_respuestas] == pregunta_actual["respuesta_correcta"]:
                    print("Respuesta correcta!")
                    mensaje_rectangulo = "¡ACERTASTE!"
                    tiempo_rectangulo = pygame.time.get_ticks()
                    i += 1
                    #Verifica que el i(que aumenta de a 1 por pregunta, sea menor al len de premios que es 15 y a su vez verifica que I no sea mayor a 15)
                    #16 porque el maximo de premios son 15
                    if i < len(premios) and i < 16:
                        pregunta_actual = preguntas[i]
                        #print(f"{premios[i]}")                       
                        #print(f"{i}")                       
                        posiciones_de_respuestas = actualizar_posiciones_de_respuestas(pregunta_actual)
                        tiempo_inicio = pygame.time.get_ticks() + 30 * 1000  # Reiniciar tiempo para nueva pregunta
                        mostrar_rectangulo = True
                        seleccion_realizada = False #La resetea para cada pregunta
                    else: 
                            print("Ganaste 1,000,000!")
                            ultimo_premio = obtener_ultimo_premio(premios, i)
                            guardar_partida(ultimo_premio)
                            pygame.time.wait(2000)  # Espera para que el jugador vea el mensaje
                            empezar = False
                else:
                    mensaje_rectangulo = "¡FALLASTE!"
                    ultimo_premio = obtener_ultimo_premio(premios, i)
                    print(f"Respuesta incorrecta. Ganaste {ultimo_premio}")
                    guardar_partida(ultimo_premio)
                    pygame.time.wait(2000)
                    empezar = False





            if comodines["50-50"] == "se puede usar" and imagen_50_50.get_rect(topleft=(800,10)).collidepoint(x, y):
                pregunta_actual["opciones"] = aplicar_comodin_50_50(pregunta_actual["opciones"], pregunta_actual["respuesta_correcta"])               
                comodines["50-50"] = "usado"
                print("Se pudo usar el comodín 50/50.")
                

            if comodines["publico"] == "se puede usar" and imagen_publico.get_rect(topleft=(650,10)).collidepoint(x, y):
                porcentajes_publico = aplicar_comodin_publico(pregunta_actual["opciones"], pregunta_actual["respuesta_correcta"])
                mostrar_porcentajes = True
                comodines["publico"] = "usado"
                print("Se pudo usar el comodín público.")



            if comodines["llamada"] == "se puede usar" and imagen_llamada.get_rect(topleft=(500,10)).collidepoint(x, y):
                aplicar_comodin_llamada(PANTALLA, pregunta_actual["respuesta_correcta"])
                comodines["llamada"] = "usado"
                print("Se pudo usar el comodín de llamada.")
                

        #advertencia de tiempo
    if 10 <= int(tiempo_segundos) <= 15:
        mensaje = (f"Le quedan {tiempo_segundos} segundos para responder!")
        dibujar_rectangulo(PANTALLA, ROJO, 135, 125, 410, 40,0)
        mostrar_mensaje(PANTALLA, mensaje, 142, 130, BLANCO, 18, "Arial Black")

    mostrar_mensaje(PANTALLA, tiempo_str, 200, 10, ROJO, 18, "Arial Black")
    if tiempo_restante <= 0:
        print("¡Tiempo agotado!")
        guardar_partida(obtener_ultimo_premio(premios, i))
        empezar = False



    #Si son True, significa que lo apretaron y entonces se imprime el mensaje en la pantalla
    if mostrar_porcentajes:
        mostrar_porcentajes_publico(PANTALLA, porcentajes_publico, posiciones_de_respuestas)
        
    
    if mostrar_rectangulo:
        if pygame.time.get_ticks() - tiempo_rectangulo < 300:
            dibujar_rectangulo(PANTALLA, BLANCO, 340, 100, 200, 50, 0)
            mostrar_mensaje(PANTALLA, mensaje_rectangulo, 350, 110, NEGRO, 24, "Arial Black")
        else:
            mostrar_rectangulo = False
    


    pygame.display.update()
    clock.tick(15)

pygame.quit()


