"""
Estilos y configuración visual para el Pizarrón Digital
"""

# Paleta de colores del pizarrón
COLORS = {
    'pizarra_fondo': '#1a2f1a',      # Verde pizarrón oscuro principal
    'pizarra_borde': '#0d1f0d',      # Verde más oscuro para bordes
    'tiza_blanca': '#f5f5f0',        # Blanco tiza (levemente amarillento)
    'tiza_amarilla': '#fffacd',      # Amarillo tiza
    'tiza_gris': '#a0a0a0',          # Gris para texto secundario
    'tachado': '#707070',            # Color para tareas tachadas
    'marco_madera': '#5d4037',       # Color para simular marco de madera
}

# Fuentes con estilo manuscrito/tiza
FONTS = {
    'tiza_titulo': ('Segoe Print', 24, 'bold'),    # Título principal
    'tiza_normal': ('Segoe Print', 16),            # Texto normal
    'tiza_small': ('Segoe Print', 12),             # Texto pequeño
    'tiza_subtitulo': ('Segoe Print', 18, 'bold'), # Subtítulos
}

# Dimensiones de la ventana
WINDOW_CONFIG = {
    'width': 900,
    'height': 650,
    'title': 'Pizarrón Digital',
    'resizable': (False, False)  # No redimensionable
}

# Configuración del efecto de textura
TEXTURE_CONFIG = {
    'noise_intensity': 0.03,    # Intensidad del ruido (muy sutil)
    'vignette_strength': 0.15,  # Fuerza del viñeteado/gradiente
}
