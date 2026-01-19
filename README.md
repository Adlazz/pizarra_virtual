# Pizarrón Virtual
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
- **Arrastra** el icono ⋮⋮ para reordenar las tareas

**Edición de Pizarras:**
- **Doble click** en el nombre de una pestaña para renombrarla
- Presiona Enter para confirmar o Escape para cancelar
- Click en el botón **×** de la pestaña para eliminar una pizarra (con confirmación)

**Configuración de Apariencia:**
- Click en el **⚙** (engranaje) en la esquina superior derecha
- **Color de Pizarra:** Verde Pizarrón, Negro Pizarra o Blanco Pizarra
- **Color de Letra:** Tiza Blanca, Fibra Roja o Fibra Azul

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

🚧 **En desarrollo - Fase 7 completada**

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

### Fase 5: Drag & Drop ✅
- ✅ Arrastrar tareas para reordenarlas
- ✅ Icono de agarre (grip) para indicar área de arrastre
- ✅ Feedback visual durante el arrastre

### Fase 6: Eliminar Pizarras ✅
- ✅ Botón X en cada pestaña para eliminar
- ✅ Diálogo de confirmación antes de eliminar
- ✅ Muestra cantidad de tareas que se perderán
- ✅ No permite eliminar si es la única pizarra

### Fase 7: Personalización de Apariencia ✅
- ✅ Botón de configuración (engranaje) en la UI
- ✅ Selección de color de pizarra (Verde, Negro, Blanco)
- ✅ Selección de color de letra (Tiza Blanca, Fibra Roja, Fibra Azul)
- ✅ Persistencia de preferencias de tema

### Próximos Pasos
- ⏳ Filtros (todas/pendientes/completadas)
- ⏳ Búsqueda de tareas
- ⏳ Exportar/importar pizarras

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.
