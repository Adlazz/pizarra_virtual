"""
Gestor de pestañas para las diferentes pizarras
"""
from typing import List, Callable, Optional, Dict


class TabManager:
    """Maneja la lógica de las pestañas de pizarras"""

    def __init__(self):
        """Inicializa el gestor de pestañas"""
        self.pizarras: List[Dict] = []
        self.pizarra_activa_id: Optional[str] = None
        self.callbacks_cambio_pestaña: List[Callable] = []

    def cargar_pizarras(self, pizarras: List[Dict], pizarra_activa_id: str):
        """
        Carga la lista de pizarras y establece la activa

        Args:
            pizarras: Lista de diccionarios con datos de pizarras
            pizarra_activa_id: ID de la pizarra activa
        """
        self.pizarras = sorted(pizarras, key=lambda p: p['orden'])
        self.pizarra_activa_id = pizarra_activa_id

    def agregar_pizarra(self, pizarra: Dict):
        """
        Agrega una nueva pizarra a la lista

        Args:
            pizarra: Diccionario con datos de la pizarra
        """
        self.pizarras.append(pizarra)
        self.pizarras.sort(key=lambda p: p['orden'])

    def eliminar_pizarra(self, pizarra_id: str) -> bool:
        """
        Elimina una pizarra de la lista

        Args:
            pizarra_id: ID de la pizarra a eliminar

        Returns:
            True si se eliminó correctamente
        """
        if len(self.pizarras) <= 1:
            return False

        pizarras_filtradas = [p for p in self.pizarras if p['id'] != pizarra_id]

        if len(pizarras_filtradas) == len(self.pizarras):
            return False

        self.pizarras = pizarras_filtradas

        # Si era la activa, cambiar a la primera
        if self.pizarra_activa_id == pizarra_id:
            self.cambiar_pizarra_activa(self.pizarras[0]['id'])

        return True

    def cambiar_pizarra_activa(self, pizarra_id: str):
        """
        Cambia la pizarra activa y notifica a los callbacks

        Args:
            pizarra_id: ID de la nueva pizarra activa
        """
        # Verificar que la pizarra existe
        if not any(p['id'] == pizarra_id for p in self.pizarras):
            return

        pizarra_anterior = self.pizarra_activa_id
        self.pizarra_activa_id = pizarra_id

        # Notificar a todos los callbacks
        for callback in self.callbacks_cambio_pestaña:
            callback(pizarra_id, pizarra_anterior)

    def obtener_pizarra_activa(self) -> Optional[Dict]:
        """
        Retorna la pizarra activa actual

        Returns:
            Diccionario con datos de la pizarra activa o None
        """
        for pizarra in self.pizarras:
            if pizarra['id'] == self.pizarra_activa_id:
                return pizarra
        return None

    def obtener_pizarra_por_id(self, pizarra_id: str) -> Optional[Dict]:
        """
        Obtiene una pizarra por su ID

        Args:
            pizarra_id: ID de la pizarra

        Returns:
            Diccionario con datos de la pizarra o None
        """
        for pizarra in self.pizarras:
            if pizarra['id'] == pizarra_id:
                return pizarra
        return None

    def obtener_pizarra_por_indice(self, indice: int) -> Optional[Dict]:
        """
        Obtiene una pizarra por su índice en la lista

        Args:
            indice: Índice de la pizarra (0-based)

        Returns:
            Diccionario con datos de la pizarra o None
        """
        if 0 <= indice < len(self.pizarras):
            return self.pizarras[indice]
        return None

    def obtener_indice_pizarra_activa(self) -> int:
        """
        Retorna el índice de la pizarra activa

        Returns:
            Índice de la pizarra activa o -1 si no se encuentra
        """
        for i, pizarra in enumerate(self.pizarras):
            if pizarra['id'] == self.pizarra_activa_id:
                return i
        return -1

    def siguiente_pizarra(self):
        """Cambia a la siguiente pizarra (circular)"""
        if not self.pizarras:
            return

        indice_actual = self.obtener_indice_pizarra_activa()
        siguiente_indice = (indice_actual + 1) % len(self.pizarras)
        siguiente_pizarra = self.pizarras[siguiente_indice]
        self.cambiar_pizarra_activa(siguiente_pizarra['id'])

    def pizarra_anterior(self):
        """Cambia a la pizarra anterior (circular)"""
        if not self.pizarras:
            return

        indice_actual = self.obtener_indice_pizarra_activa()
        anterior_indice = (indice_actual - 1) % len(self.pizarras)
        anterior_pizarra = self.pizarras[anterior_indice]
        self.cambiar_pizarra_activa(anterior_pizarra['id'])

    def agregar_callback_cambio(self, callback: Callable):
        """
        Registra un callback que se ejecutará al cambiar de pestaña

        Args:
            callback: Función que recibe (pizarra_id_nueva, pizarra_id_anterior)
        """
        self.callbacks_cambio_pestaña.append(callback)

    def validar_nombre_pizarra(self, nombre: str) -> tuple[bool, str]:
        """
        Valida que un nombre de pizarra sea válido

        Args:
            nombre: Nombre a validar

        Returns:
            Tupla (es_valido, mensaje_error)
        """
        nombre = nombre.strip()

        # Validar que no esté vacío
        if not nombre:
            return False, "El nombre no puede estar vacío"

        # Validar longitud máxima
        if len(nombre) > 20:
            return False, "El nombre no puede tener más de 20 caracteres"

        # Validar que no exista
        nombres_existentes = [p['nombre'].lower() for p in self.pizarras]
        if nombre.lower() in nombres_existentes:
            return False, "Ya existe una pizarra con ese nombre"

        return True, ""
