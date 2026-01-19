"""
Sistema de persistencia de datos para el Pizarrón Digital
Maneja el guardado y carga de pizarras y tareas en formato JSON
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Optional


class Storage:
    """Gestor de almacenamiento de datos"""

    def __init__(self):
        """Inicializa el sistema de almacenamiento"""
        self.data_dir = self._obtener_directorio_datos()
        self.data_file = self.data_dir / "pizarras.json"
        self._crear_directorio_si_no_existe()

    def _obtener_directorio_datos(self) -> Path:
        """
        Obtiene el directorio de datos de la aplicación según el SO
        Windows: %APPDATA%/PizarronDigital
        Linux/Mac: ~/.local/share/PizarronDigital
        """
        if os.name == 'nt':  # Windows
            base_dir = Path(os.getenv('APPDATA', ''))
        else:  # Linux/Mac
            base_dir = Path.home() / '.local' / 'share'

        return base_dir / 'PizarronDigital'

    def _crear_directorio_si_no_existe(self):
        """Crea el directorio de datos si no existe"""
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _obtener_datos_por_defecto(self) -> Dict:
        """Retorna la estructura de datos por defecto"""
        return {
            "pizarras": [
                {
                    "id": "trabajo",
                    "nombre": "Trabajo",
                    "orden": 0,
                    "tareas": []
                },
                {
                    "id": "casa",
                    "nombre": "Casa",
                    "orden": 1,
                    "tareas": []
                },
                {
                    "id": "personal",
                    "nombre": "Personal",
                    "orden": 2,
                    "tareas": []
                }
            ],
            "pizarra_activa": "trabajo",
            "configuracion": {
                "tema_fondo": "verde",
                "tema_letra": "tiza_blanca"
            }
        }

    def cargar_datos(self) -> Dict:
        """
        Carga los datos desde el archivo JSON
        Si no existe, retorna datos por defecto
        """
        if not self.data_file.exists():
            return self._obtener_datos_por_defecto()

        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                # Validar estructura básica
                if 'pizarras' not in datos or 'pizarra_activa' not in datos:
                    return self._obtener_datos_por_defecto()
                return datos
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error al cargar datos: {e}")
            return self._obtener_datos_por_defecto()

    def guardar_datos(self, datos: Dict) -> bool:
        """
        Guarda los datos en el archivo JSON
        Retorna True si tuvo éxito, False en caso contrario
        """
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"Error al guardar datos: {e}")
            return False

    def agregar_pizarra(self, datos: Dict, nombre: str) -> Optional[Dict]:
        """
        Agrega una nueva pizarra a los datos
        Retorna la pizarra creada o None si el nombre ya existe
        """
        # Validar que el nombre no esté vacío
        nombre = nombre.strip()
        if not nombre:
            return None

        # Validar que no exista una pizarra con ese nombre
        nombres_existentes = [p['nombre'].lower() for p in datos['pizarras']]
        if nombre.lower() in nombres_existentes:
            return None

        # Generar ID único (basado en el nombre, en minúsculas y sin espacios)
        pizarra_id = nombre.lower().replace(' ', '_')

        # Determinar el orden (último + 1)
        max_orden = max([p['orden'] for p in datos['pizarras']], default=-1)

        # Crear nueva pizarra
        nueva_pizarra = {
            "id": pizarra_id,
            "nombre": nombre,
            "orden": max_orden + 1,
            "tareas": []
        }

        datos['pizarras'].append(nueva_pizarra)
        return nueva_pizarra

    def eliminar_pizarra(self, datos: Dict, pizarra_id: str) -> bool:
        """
        Elimina una pizarra por su ID
        No permite eliminar si es la única pizarra
        Retorna True si tuvo éxito
        """
        if len(datos['pizarras']) <= 1:
            return False

        # Buscar y eliminar la pizarra
        pizarras_filtradas = [p for p in datos['pizarras'] if p['id'] != pizarra_id]

        if len(pizarras_filtradas) == len(datos['pizarras']):
            return False  # No se encontró la pizarra

        datos['pizarras'] = pizarras_filtradas

        # Si era la pizarra activa, cambiar a la primera
        if datos['pizarra_activa'] == pizarra_id:
            datos['pizarra_activa'] = datos['pizarras'][0]['id']

        return True

    def obtener_pizarra(self, datos: Dict, pizarra_id: str) -> Optional[Dict]:
        """Obtiene una pizarra por su ID"""
        for pizarra in datos['pizarras']:
            if pizarra['id'] == pizarra_id:
                return pizarra
        return None

    def establecer_pizarra_activa(self, datos: Dict, pizarra_id: str) -> bool:
        """
        Establece la pizarra activa
        Retorna True si tuvo éxito
        """
        if self.obtener_pizarra(datos, pizarra_id) is not None:
            datos['pizarra_activa'] = pizarra_id
            return True
        return False
