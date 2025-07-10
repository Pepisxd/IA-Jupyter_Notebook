import random
import os
import re


ruta_archivo = "/home/pepis/Descargas/resultado.txt"



def cargar_ejercicios(ruta_archivo):
    """
    Lee ejercicios desde un archivo con formato:
    [dificultad]  [tema]  enunciado
    separados por tabulaciones, y elimina los corchetes.
    """
    ejercicios = []
    mapeo_dificultad = {
        "principiante": 1,
        "intermedio": 2,
        "avanzado": 3
    }

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            next(f)  # Saltar encabezado

            for linea in f:
                partes = linea.strip().split("\t", 2)
                if len(partes) == 3:
                    dificultad_str = partes[0].strip("[]").lower()
                    tema = partes[1].strip("[]")
                    problema = partes[2]

                    dificultad_num = mapeo_dificultad.get(dificultad_str, -1)
                    if dificultad_num != -1:
                        ejercicios.append({
                            "dificultad_str": dificultad_str,
                            "dificultad_num": dificultad_num,
                            "tema": tema,
                            "problema": problema
                        })
                    else:
                        print(f"Advertencia: dificultad desconocida '{dificultad_str}' en línea: {linea.strip()}")
                else:
                    print(f"Advertencia: línea mal formateada ignorada: {linea.strip()}")
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta_archivo}' no fue encontrado.")

    return ejercicios, mapeo_dificultad


def seleccionar_ejercicio(ejercicios_cargados, dificultad_deseada_num, mapeo_dificultad):
    """
    Simula las 'Capas Ocultas' para seleccionar el ejercicio.
    Implementa la lógica para encontrar un ejercicio de la dificultad deseada.
    """
    ejercicios_filtrados = [
        ej for ej in ejercicios_cargados if ej["dificultad_num"] == dificultad_deseada_num
    ]

    if ejercicios_filtrados:
        # Si hay ejercicios de la dificultad exacta, elige uno aleatoriamente
        return random.choice(ejercicios_filtrados)
    else:
        # Lógica de fallback: Si no hay de la dificultad exacta, busca cercanos.
        # Esto es una forma simple de "adaptación" de nuestra "IA".
        print(f"No se encontraron ejercicios de dificultad exacta. Buscando dificultad cercana...")
        dificultades_cercanas = []
        if dificultad_deseada_num > 0:
            dificultades_cercanas.append(dificultad_deseada_num - 1) # Dificultad menor
        if dificultad_deseada_num < max(mapeo_dificultad.values()):
            dificultades_cercanas.append(dificultad_deseada_num + 1) # Dificultad mayor

        ejercicios_cercanos = []
        for d_num in dificultades_cercanas:
            ejercicios_cercanos.extend([ej for ej in ejercicios_cargados if ej["dificultad_num"] == d_num])

        if ejercicios_cercanos:
            return random.choice(ejercicios_cercanos)
        else:
            return None # No se encontraron ejercicios

def mostrar_ejercicio(ejercicio):
    """
    Simula la 'Capa de Salida' presentando el ejercicio al usuario.
    """
    if ejercicio:
        print("\n--- ¡Tu Ejercicio Generado por la IA! ---")
        print(f"Dificultad: {ejercicio['dificultad_str']}")
        print(f"Tema: {ejercicio['tema']}")
        print(f"Problema: {ejercicio['problema']}")
        print("---------------------------------------")
    else:
        print("\nLo siento, no pude generar un ejercicio con la dificultad solicitada.")

# --- Flujo principal en tu Jupyter Notebook ---

# 1. Cargar los ejercicios (simulando la Capa de Entrada)
ejercicios_disponibles, mapeo_dificultad_global = cargar_ejercicios(ruta_archivo)

if not ejercicios_disponibles:
    print("No hay ejercicios para procesar. Asegúrate de que 'ejercicios.txt' exista y esté bien formateado.")
else:
    # Mostrar opciones al usuario
    print("Dificultades disponibles:")
    for dificultad_str, dificultad_num in mapeo_dificultad_global.items():
        print(f"- {dificultad_str} (código: {dificultad_num})")

    # 2. Obtener la dificultad deseada por el usuario
    while True:
        try:
            opcion_dificultad = input("Ingresa el código numérico de la dificultad deseada (1=principiante, 2=intermedio, 3=avanzado): ")
            dificultad_usuario_num = int(opcion_dificultad)
            if dificultad_usuario_num in mapeo_dificultad_global.values():
                break
            else:
                print("Código de dificultad no válido. Inténtalo de nuevo.")
        except ValueError:
            print("Entrada no válida. Por favor, ingresa un número.")

    # 3. Seleccionar y mostrar el ejercicio (simulando Capas Ocultas y de Salida)
    ejercicio_elegido = seleccionar_ejercicio(ejercicios_disponibles, dificultad_usuario_num, mapeo_dificultad_global)
    mostrar_ejercicio(ejercicio_elegido)