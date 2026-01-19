"""
Punto de entrada principal de la aplicación Pizarrón Digital
"""
import sys
from pathlib import Path

# Agregar el directorio src al path para permitir imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from ui.main_window import MainWindow


def main():
    """Función principal que inicia la aplicación"""
    app = MainWindow()
    app.ejecutar()


if __name__ == "__main__":
    main()
