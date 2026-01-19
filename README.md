# Pizarrón Digital

Una aplicación minimalista de escritorio para gestionar tareas pendientes con la estética de un pizarrón escolar.

## Características

- Interfaz minimalista que simula un pizarrón verde oscuro
- Efecto de escritura con tiza
- Gestión de múltiples pizarras (Trabajo, Casa, Banda, etc.)
- Tachar/eliminar tareas al completarlas
- Persistencia de datos en formato JSON

## Requisitos

- Python 3.8 o superior
- CustomTkinter 5.2.2
- Pillow 10.2.0

## Instalación

1. Clonar el repositorio o descargar los archivos

2. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
```

3. Activar el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Para ejecutar la aplicación:

```bash
python main.py
```

### Funcionalidades

**Gestión de Pizarras:**
- Crea múltiples pizarras para organizar tus tareas
- Cambia entre pizarras usando las pestañas o atajos de teclado
- Cada pizarra guarda sus tareas independientemente

**Gestión de Tareas:**
- Escribe una tarea en el campo "Nueva tarea..." y presiona Enter
- Marca tareas como completadas usando el checkbox (se tacharán automáticamente)
- Elimina tareas usando el botón X
- Visualiza el contador de tareas completadas en la esquina superior derecha
- **Doble click** en una tarea para editarla (solo tareas pendientes)

**Edición de Pizarras:**
- **Doble click** en el nombre de una pestaña para renombrarla
- Presiona Enter para confirmar o Escape para cancelar

### Atajos de Teclado

- **Ctrl+N**: Crear nueva pizarra
- **Ctrl+Tab**: Cambiar a la siguiente pizarra
- **Ctrl+Shift+Tab**: Cambiar a la pizarra anterior
- **Ctrl+1 a Ctrl+9**: Cambiar a una pizarra específica (1-9)
- **Enter**: Agregar nueva tarea (cuando el campo de entrada tiene foco)

## Estructura del Proyecto

```
pizarron_digital/
├── main.py                  # Punto de entrada principal
├── src/
│   ├── ui/
│   │   ├── main_window.py   # Ventana principal con toda la lógica de UI
│   │   ├── tab_manager.py   # Gestor de pestañas de pizarras
│   │   ├── task_widget.py   # Widget individual para cada tarea
│   │   └── styles.py        # Estilos y configuración visual
│   ├── core/
│   │   ├── task_manager.py  # Lógica de gestión de tareas
│   │   └── storage.py       # Persistencia de datos en JSON
│   └── assets/
│       └── fonts/           # Fuentes manuscritas (futuro)
├── requirements.txt
└── README.md
```

## Almacenamiento de Datos

Los datos se guardan automáticamente en:
- **Windows**: `%APPDATA%/PizarronDigital/pizarras.json`
- **Linux/Mac**: `~/.local/share/PizarronDigital/pizarras.json`

## Estado del Proyecto

🚧 **En desarrollo - Fase 4 completada**

### Fase 1: Setup Inicial ✅
- ✅ Estructura base del proyecto
- ✅ Ventana principal con efecto de pizarrón
- ✅ Sistema de estilos y colores

### Fase 2: Sistema de Múltiples Pizarras ✅
- ✅ Gestión de múltiples pizarras
- ✅ Pestañas visuales con estilo tiza
- ✅ Diálogo para crear nuevas pizarras
- ✅ Persistencia de datos en JSON
- ✅ Atajos de teclado
- ✅ Área scrolleable para contenido

### Fase 3: Sistema de Tareas ✅
- ✅ Campo de entrada para nuevas tareas
- ✅ Agregar tareas con Enter o botón +
- ✅ Checkbox para marcar tareas completadas
- ✅ Efecto de tachado en tareas completadas
- ✅ Eliminar tareas con botón X
- ✅ Contador de tareas (completadas/total)
- ✅ Guardado automático en JSON
- ✅ Widget personalizado para cada tarea

### Fase 4: Edición Inline ✅
- ✅ Editar tareas con doble click
- ✅ Renombrar pestañas con doble click
- ✅ Confirmación con Enter, cancelación con Escape
- ✅ Validaciones de nombre (máx. 20 caracteres, no duplicados)

### Próximos Pasos
- ⏳ Drag & drop para reordenar tareas
- ⏳ Filtros (todas/pendientes/completadas)
- ⏳ Búsqueda de tareas
- ⏳ Exportar/importar pizarras
- ⏳ Eliminar pizarras

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.
