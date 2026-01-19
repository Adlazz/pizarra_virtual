"""
Estilos y configuración visual para el Pizarrón Digital
"""

# Temas de fondo disponibles
TEMAS_FONDO = {
    'verde': {
        'nombre': 'Verde Pizarrón',
        'pizarra_fondo': '#1a2f1a',
        'pizarra_borde': '#0d1f0d',
        'marco_madera': '#5d4037',
    },
    'negro': {
        'nombre': 'Negro Pizarra',
        'pizarra_fondo': '#1a1a1a',
        'pizarra_borde': '#0d0d0d',
        'marco_madera': '#3d3d3d',
    },
    'blanco': {
        'nombre': 'Blanco Pizarra',
        'pizarra_fondo': '#f0f0f0',
        'pizarra_borde': '#d0d0d0',
        'marco_madera': '#8b7355',
    },
}

# Temas de letra disponibles
TEMAS_LETRA = {
    'tiza_blanca': {
        'nombre': 'Tiza Blanca',
        'principal': '#f5f5f0',
        'secundario': '#a0a0a0',
        'acento': '#fffacd',
    },
    'fibra_roja': {
        'nombre': 'Fibra Roja',
        'principal': '#dc3545',
        'secundario': '#a02530',
        'acento': '#ff6b7a',
    },
    'fibra_azul': {
        'nombre': 'Fibra Azul',
        'principal': '#4a90d9',
        'secundario': '#2c5aa0',
        'acento': '#7ab8ff',
    },
}

# Configuración actual (se actualiza dinámicamente)
TEMA_ACTUAL = {
    'fondo': 'verde',
    'letra': 'tiza_blanca',
}

def obtener_colores():
    """Obtiene los colores según el tema actual"""
    fondo = TEMAS_FONDO[TEMA_ACTUAL['fondo']]
    letra = TEMAS_LETRA[TEMA_ACTUAL['letra']]

    return {
        'pizarra_fondo': fondo['pizarra_fondo'],
        'pizarra_borde': fondo['pizarra_borde'],
        'marco_madera': fondo['marco_madera'],
        'tiza_blanca': letra['principal'],
        'tiza_amarilla': letra['acento'],
        'tiza_gris': letra['secundario'],
        'tachado': '#707070',
    }

# Colores iniciales (compatibilidad)
COLORS = obtener_colores()

def actualizar_colores():
    """Actualiza el diccionario COLORS con el tema actual"""
    global COLORS
    COLORS.update(obtener_colores())

# Fuentes con estilo manuscrito/tiza
FONTS = {
    'tiza_titulo': ('Segoe Print', 24, 'bold'),
    'tiza_normal': ('Segoe Print', 16),
    'tiza_small': ('Segoe Print', 12),
    'tiza_subtitulo': ('Segoe Print', 18, 'bold'),
}

# Dimensiones de la ventana
WINDOW_CONFIG = {
    'width': 900,
    'height': 650,
    'title': 'Pizarrón Digital',
    'resizable': (False, False)
}

# Configuración del efecto de textura
TEXTURE_CONFIG = {
    'noise_intensity': 0.03,
    'vignette_strength': 0.15,
}