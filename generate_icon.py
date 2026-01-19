"""
Script para generar el icono de Pizarrón Digital
Estilo: fondo verde pizarrón con letra "P" en tiza blanca
"""
from PIL import Image, ImageDraw, ImageFont
import os

def crear_icono():
    # Tamaños para el archivo .ico (múltiples resoluciones)
    tamaños = [16, 32, 48, 64, 128, 256]

    imagenes = []

    for tamaño in tamaños:
        # Crear imagen con fondo verde pizarrón
        img = Image.new('RGBA', (tamaño, tamaño), (26, 47, 26, 255))  # #1a2f1a
        draw = ImageDraw.Draw(img)

        # Dibujar un borde sutil (marco de madera)
        borde = max(1, tamaño // 32)
        draw.rectangle(
            [0, 0, tamaño-1, tamaño-1],
            outline=(93, 64, 55, 255),  # #5d4037 marrón madera
            width=borde
        )

        # Calcular tamaño de fuente proporcional
        font_size = int(tamaño * 0.7)

        # Intentar usar una fuente con estilo manuscrito
        try:
            font = ImageFont.truetype("segoesc.ttf", font_size)  # Segoe Script
        except:
            try:
                font = ImageFont.truetype("segoepr.ttf", font_size)  # Segoe Print
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()

        # Color tiza blanca con ligera textura
        color_tiza = (245, 245, 240, 255)  # #f5f5f0

        # Dibujar la "P" centrada
        texto = "P"

        # Obtener el bounding box del texto
        bbox = draw.textbbox((0, 0), texto, font=font)
        ancho_texto = bbox[2] - bbox[0]
        alto_texto = bbox[3] - bbox[1]

        # Calcular posición centrada
        x = (tamaño - ancho_texto) // 2 - bbox[0]
        y = (tamaño - alto_texto) // 2 - bbox[1]

        # Efecto de tiza: dibujar con ligero desplazamiento para dar textura
        if tamaño >= 32:
            # Sombra sutil para efecto de relieve
            draw.text((x+1, y+1), texto, fill=(200, 200, 195, 100), font=font)

        # Texto principal
        draw.text((x, y), texto, fill=color_tiza, font=font)

        imagenes.append(img)

    # Guardar como .ico con múltiples resoluciones
    # El primer tamaño (256) será la imagen principal
    imagenes[-1].save(
        'icon.ico',
        format='ICO',
        sizes=[(s, s) for s in tamaños],
        append_images=imagenes[:-1]
    )

    print("Icono generado: icon.ico")
    print(f"Tamaños incluidos: {tamaños}")

if __name__ == "__main__":
    crear_icono()