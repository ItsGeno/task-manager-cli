import json
import shutil

booleanos = {True: "[X]", False: "[ ]"}

archivo = "tareas.json"

class TareaNoEncontradaError(Exception):
    pass

class TareaCompletada(Exception):
    pass

class TareaVaciaError(Exception):
    pass

def agregar_tarea(lista, nombre):
    if not nombre.strip():
        raise TareaVaciaError("El nombre de la tarea no puede estar vacío.")
    tarea = {
        "nombre": nombre.strip(),
        "completada": False
    }
    lista.append(tarea)


def listar_tareas(lista):
    print("\nLista de tareas:")
    if not lista:
        print("No hay tareas en la lista.")
        return
    for i, tarea in enumerate(lista, start=1):
        estado = booleanos[tarea["completada"]]
        print(f"{i}. {tarea['nombre']} - {estado}") 

def completar_tarea(lista, numero):
    if numero < 1 or numero > len(lista):
        raise TareaNoEncontradaError(numero)
    if lista[numero - 1]["completada"]: 
        raise TareaCompletada(numero)
    lista[numero - 1]["completada"] = True

def guardar_tareas(lista, archivo):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=4)

def cargar_tareas(archivo):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        shutil.copy(archivo, archivo + ".bak")
        print(f"Error: El archivo de tareas está corrupto. Se guardo una copia {archivo}.bak y se iniciará con una lista vacía.")
        return []
    except FileNotFoundError:
        return []

def main():
    tareas=cargar_tareas(archivo)

    while True:
        print("\nOpciones:")
        print("1. Agregar tarea")
        print("2. Listar tareas")
        print("3. Completar tarea")
        print("4. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            nombre_tarea = input("Ingrese el nombre de la tarea: ").strip()
            try:
                agregar_tarea(tareas, nombre_tarea)
                guardar_tareas(tareas, archivo)
                print(f"Tarea '{nombre_tarea}' agregada.")
            except TareaVaciaError as e:
                print(f"Error: {e} intenta de nuevo")

        elif opcion == "2":
            listar_tareas(tareas)
        elif opcion == "3":
            try:
                numero_tarea = int(input("Ingrese el número de la tarea a completar: "))
                completar_tarea(tareas, numero_tarea)
                guardar_tareas(tareas, archivo)
                print(f"Tarea número {numero_tarea} completada.")
            except ValueError:
                print("Error: Debe ingresar un número válido.")
            except TareaNoEncontradaError as e:
                print(f"Error: la tarea {e} no existe")
            except TareaCompletada as e:
                print(f"Error: la tarea {e} ya está completada")
        elif opcion == "4":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()