'''Sistema de gestion de tareas de mediana complejidad donde puedo agregar las tareas con su respectivo nombre, id, descripcion y estado. Tambien puedo ver la lista de tareas, actualizar el estado de una tarea y eliminar una tarea. Donde toda esta informacion se guarda en un archivo JSON para su posterior uso.'''

# Agregar librerias necesarias
import json 
import os
from typing import List, Dict, Any
from dataclasses import dataclass


class FileHandler:
    def __init__(self, path):
        self.path = path

    def read(self):
        if not os.path.exists(self.path):
            return []
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def write(self, data):
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

@dataclass
class Task:
    id: int
    name: str
    description: str
    status: str = 'pendiente'

class TaskManager:
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.tasks: List[Task] = []
        self._load_tasks()

    def _load_tasks(self):
        try:
            data = self.file_handler.read()
            if data:
                self.tasks = [Task(**t) for t in data]
            else:
                self.tasks = []
        except Exception:
            self.tasks = []

    def _save(self):
        try:
            self.file_handler.write([t.__dict__ for t in self.tasks])
        except Exception:
            pass

    def add_task(self, name: str, description: str):
        next_id = max((t.id for t in self.tasks), default=0) + 1
        task = Task(next_id, name, description, 'pendiente')
        self.tasks.append(task)
        self._save()

    def get_tasks(self):
        return self.tasks

    def update_task_status(self, task_id: int, new_status: str) -> bool:
        for t in self.tasks:
            if t.id == task_id:
                t.status = new_status
                self._save()
                return True
        return False

    def delete_task(self, task_id: int) -> bool:
        for i, t in enumerate(self.tasks):
            if t.id == task_id:
                del self.tasks[i]
                self._save()
                return True
        return False
def main():
    file_path = 'tasks.json'
    file_handler = FileHandler(file_path)
    task_manager = TaskManager(file_handler)

    while True:
        print("\n--- Task Manager ---")
        print("1. Agregar Tarea")
        print("2. Ver Tareas")
        print("3. Actualizar Estado de Tarea")
        print("4. Eliminar Tarea")
        print("5. Salir")

        choice = input("Seleccione una opcion: ")

        if choice == '1':
            name = input("Nombre de la tarea: ")
            description = input("Descripcion de la tarea: ")
            task_manager.add_task(name, description)
            print("Tarea agregada exitosamente.")

        elif choice == '2':
            tasks = task_manager.get_tasks()
            if not tasks:
                print("No hay tareas disponibles.")
            else:
                for task in tasks:
                    print(f"ID: {task.id}, Nombre: {task.name}, Descripcion: {task.description}, Estado: {task.status}")

        elif choice == '3':
            task_id = int(input("Ingrese el ID de la tarea a actualizar: "))
            new_status = input("Ingrese el nuevo estado (pendiente/en progreso/completada): ")
            if task_manager.update_task_status(task_id, new_status):
                print("Estado de la tarea actualizado exitosamente.")
            else:
                print("Tarea no encontrada.")

        elif choice == '4':
            task_id = int(input("Ingrese el ID de la tarea a eliminar: "))
            if task_manager.delete_task(task_id):
                print("Tarea eliminada exitosamente.")
            else:
                print("Tarea no encontrada.")

        elif choice == '5':
            print("Saliendo del Task Manager.")
            break

        else:
            print("Opcion invalida. Por favor intente de nuevo.")

if __name__ == "__main__":
    main()      