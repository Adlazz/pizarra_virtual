"""
Gestor de tareas para el Pizarrón Digital
"""
from typing import Dict, List, Optional
import time


class TaskManager:
    """Maneja la lógica de las tareas"""

    @staticmethod
    def crear_tarea(texto: str) -> Dict:
        """
        Crea una nueva tarea

        Args:
            texto: Texto de la tarea

        Returns:
            Diccionario con datos de la tarea
        """
        return {
            "id": str(int(time.time() * 1000)),  # Timestamp en milisegundos como ID
            "texto": texto,
            "completada": False,
            "fecha_creacion": time.time()
        }

    @staticmethod
    def agregar_tarea(pizarra: Dict, texto: str) -> Optional[Dict]:
        """
        Agrega una tarea a una pizarra

        Args:
            pizarra: Diccionario de la pizarra
            texto: Texto de la tarea

        Returns:
            La tarea creada o None si el texto está vacío
        """
        texto = texto.strip()
        if not texto:
            return None

        tarea = TaskManager.crear_tarea(texto)
        pizarra['tareas'].append(tarea)
        return tarea

    @staticmethod
    def eliminar_tarea(pizarra: Dict, tarea_id: str) -> bool:
        """
        Elimina una tarea de una pizarra

        Args:
            pizarra: Diccionario de la pizarra
            tarea_id: ID de la tarea a eliminar

        Returns:
            True si se eliminó correctamente
        """
        tareas_filtradas = [t for t in pizarra['tareas'] if t['id'] != tarea_id]

        if len(tareas_filtradas) == len(pizarra['tareas']):
            return False  # No se encontró la tarea

        pizarra['tareas'] = tareas_filtradas
        return True

    @staticmethod
    def alternar_completada(pizarra: Dict, tarea_id: str) -> bool:
        """
        Alterna el estado de completada de una tarea

        Args:
            pizarra: Diccionario de la pizarra
            tarea_id: ID de la tarea

        Returns:
            True si se encontró y actualizó la tarea
        """
        for tarea in pizarra['tareas']:
            if tarea['id'] == tarea_id:
                tarea['completada'] = not tarea['completada']
                return True
        return False

    @staticmethod
    def editar_tarea(pizarra: Dict, tarea_id: str, nuevo_texto: str) -> bool:
        """
        Edita el texto de una tarea

        Args:
            pizarra: Diccionario de la pizarra
            tarea_id: ID de la tarea
            nuevo_texto: Nuevo texto para la tarea

        Returns:
            True si se encontró y editó la tarea
        """
        nuevo_texto = nuevo_texto.strip()
        if not nuevo_texto:
            return False

        for tarea in pizarra['tareas']:
            if tarea['id'] == tarea_id:
                tarea['texto'] = nuevo_texto
                return True
        return False

    @staticmethod
    def obtener_tarea(pizarra: Dict, tarea_id: str) -> Optional[Dict]:
        """
        Obtiene una tarea por su ID

        Args:
            pizarra: Diccionario de la pizarra
            tarea_id: ID de la tarea

        Returns:
            Diccionario de la tarea o None
        """
        for tarea in pizarra['tareas']:
            if tarea['id'] == tarea_id:
                return tarea
        return None

    @staticmethod
    def contar_tareas_completadas(pizarra: Dict) -> tuple[int, int]:
        """
        Cuenta las tareas completadas y el total

        Args:
            pizarra: Diccionario de la pizarra

        Returns:
            Tupla (completadas, total)
        """
        total = len(pizarra['tareas'])
        completadas = sum(1 for t in pizarra['tareas'] if t['completada'])
        return completadas, total
