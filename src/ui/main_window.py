"""
Ventana principal del Pizarrón Digital
"""
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk, ImageFilter
import random
from ui.styles import COLORS, FONTS, WINDOW_CONFIG, TEXTURE_CONFIG
from ui.tab_manager import TabManager
from ui.task_widget import TaskWidget
from core.storage import Storage
from core.task_manager import TaskManager


class MainWindow(ctk.CTk):
    """Ventana principal de la aplicación"""

    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.title(WINDOW_CONFIG['title'])
        self.geometry(f"{WINDOW_CONFIG['width']}x{WINDOW_CONFIG['height']}")
        self.resizable(WINDOW_CONFIG['resizable'][0], WINDOW_CONFIG['resizable'][1])

        # Configurar tema oscuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Color de fondo base
        self.configure(fg_color=COLORS['pizarra_fondo'])

        # Inicializar sistemas de gestión
        self.storage = Storage()
        self.tab_manager = TabManager()
        self.task_manager = TaskManager()
        self.datos = self.storage.cargar_datos()

        # Botones de pestañas (para mantener referencias)
        self.tab_buttons = {}

        # Widgets de tareas (para mantener referencias)
        self.task_widgets = []

        # Cargar pizarras en el tab manager
        self.tab_manager.cargar_pizarras(
            self.datos['pizarras'],
            self.datos['pizarra_activa']
        )

        # Registrar callback para cambios de pestaña
        self.tab_manager.agregar_callback_cambio(self._on_cambio_pestana)

        # Crear la interfaz
        self._crear_interfaz()

        # Configurar atajos de teclado
        self._configurar_atajos_teclado()

    def _crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""

        # Frame principal que contendrá todo
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS['pizarra_fondo'],
            corner_radius=0
        )
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Crear y aplicar textura de pizarrón
        self._aplicar_textura_pizarron()

        # Frame para el borde/marco de madera
        self.marco_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=COLORS['marco_madera'],
            corner_radius=0
        )
        self.marco_frame.pack(fill="both", expand=True, padx=8, pady=8)

        # Frame interior del pizarrón (contenido)
        self.pizarra_frame = ctk.CTkFrame(
            self.marco_frame,
            fg_color=COLORS['pizarra_fondo'],
            corner_radius=0
        )
        self.pizarra_frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Título principal con efecto de tiza
        self.titulo_label = ctk.CTkLabel(
            self.pizarra_frame,
            text="Mis Pizarras",
            font=FONTS['tiza_titulo'],
            text_color=COLORS['tiza_blanca'],
            fg_color="transparent"
        )
        self.titulo_label.pack(pady=(20, 10))

        # Línea decorativa debajo del título (simulando tiza)
        self.linea_frame = ctk.CTkFrame(
            self.pizarra_frame,
            height=2,
            fg_color=COLORS['tiza_blanca'],
            corner_radius=1
        )
        self.linea_frame.pack(fill="x", padx=250, pady=(0, 10))

        # Contenedor de pestañas
        self.tabs_frame = ctk.CTkFrame(
            self.pizarra_frame,
            fg_color="transparent",
            height=50
        )
        self.tabs_frame.pack(fill="x", padx=30, pady=(10, 0))

        # Crear las pestañas
        self._crear_pestanas()

        # Contenedor principal para las tareas (scrolleable)
        self.contenido_frame = ctk.CTkScrollableFrame(
            self.pizarra_frame,
            fg_color="transparent"
        )
        self.contenido_frame.pack(fill="both", expand=True, padx=30, pady=(10, 20))

        # Mostrar contenido de la pizarra activa
        self._mostrar_contenido_pizarra()

    def _aplicar_textura_pizarron(self):
        """
        Crea y aplica una textura de pizarrón con ruido sutil
        para dar efecto más realista
        """
        # Crear imagen con textura
        ancho = WINDOW_CONFIG['width']
        alto = WINDOW_CONFIG['height']

        # Crear imagen base
        imagen = Image.new('RGB', (ancho, alto), COLORS['pizarra_fondo'])
        pixels = imagen.load()

        # Convertir color hex a RGB
        base_color = self._hex_to_rgb(COLORS['pizarra_fondo'])

        # Agregar ruido sutil para textura
        for i in range(ancho):
            for j in range(alto):
                # Ruido aleatorio muy sutil
                noise = random.uniform(-TEXTURE_CONFIG['noise_intensity'],
                                      TEXTURE_CONFIG['noise_intensity'])

                # Efecto de viñeteado (más oscuro en los bordes)
                center_x = ancho / 2
                center_y = alto / 2
                dist_x = abs(i - center_x) / center_x
                dist_y = abs(j - center_y) / center_y
                vignette = 1 - (dist_x * dist_y * TEXTURE_CONFIG['vignette_strength'])

                # Aplicar efectos
                r = int(min(255, max(0, base_color[0] * (1 + noise) * vignette)))
                g = int(min(255, max(0, base_color[1] * (1 + noise) * vignette)))
                b = int(min(255, max(0, base_color[2] * (1 + noise) * vignette)))

                pixels[i, j] = (r, g, b)

        # Aplicar un desenfoque muy leve para suavizar
        imagen = imagen.filter(ImageFilter.GaussianBlur(radius=0.5))

        # Guardar referencia para que no sea garbage collected
        self.texture_image = ImageTk.PhotoImage(imagen)

    def _hex_to_rgb(self, hex_color):
        """Convierte color hexadecimal a tupla RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _crear_pestanas(self):
        """Crea los botones de pestañas para cada pizarra"""
        # Limpiar pestañas existentes
        for widget in self.tabs_frame.winfo_children():
            widget.destroy()
        self.tab_buttons.clear()

        # Determinar si se puede eliminar (más de una pizarra)
        puede_eliminar = len(self.tab_manager.pizarras) > 1

        # Crear pestaña para cada pizarra
        for i, pizarra in enumerate(self.tab_manager.pizarras):
            es_activa = pizarra['id'] == self.tab_manager.pizarra_activa_id

            # Frame contenedor de la pestaña
            tab_frame = ctk.CTkFrame(
                self.tabs_frame,
                fg_color="transparent" if not es_activa else COLORS['pizarra_borde'],
                corner_radius=8,
                width=120 if puede_eliminar else 100,
                height=35
            )
            tab_frame.pack(side="left", padx=5)
            tab_frame.pack_propagate(False)

            # Frame interior para organizar nombre y botón X
            tab_inner = ctk.CTkFrame(
                tab_frame,
                fg_color="transparent"
            )
            tab_inner.pack(expand=True, fill="both", padx=5, pady=5)

            # Label del nombre (visible por defecto)
            tab_label = ctk.CTkLabel(
                tab_inner,
                text=pizarra['nombre'],
                font=FONTS['tiza_small'],
                text_color=COLORS['tiza_blanca'],
                fg_color="transparent"
            )
            tab_label.pack(side="left", expand=True, fill="both")

            # Botón X para eliminar (solo si hay más de una pizarra)
            if puede_eliminar:
                btn_eliminar = ctk.CTkButton(
                    tab_inner,
                    text="×",
                    font=('Arial', 14, 'bold'),
                    fg_color="transparent",
                    text_color=COLORS['tiza_gris'],
                    hover_color=COLORS['pizarra_borde'],
                    width=20,
                    height=20,
                    corner_radius=4,
                    command=lambda pid=pizarra['id']: self._confirmar_eliminar_pizarra(pid)
                )
                btn_eliminar.pack(side="right", padx=(5, 0))

            # Entry para edición (oculto por defecto)
            tab_entry = ctk.CTkEntry(
                tab_frame,
                font=FONTS['tiza_small'],
                fg_color=COLORS['pizarra_borde'],
                text_color=COLORS['tiza_blanca'],
                border_width=1,
                border_color=COLORS['tiza_amarilla'],
                width=90,
                height=28
            )

            # Bindings
            tab_label.bind("<Button-1>", lambda e, pid=pizarra['id']: self._cambiar_pestana(pid))
            tab_label.bind("<Double-Button-1>", lambda e, pid=pizarra['id']: self._iniciar_edicion_pestana(pid))
            tab_frame.bind("<Button-1>", lambda e, pid=pizarra['id']: self._cambiar_pestana(pid))

            # Si es activa, agregar subrayado
            if es_activa:
                underline = ctk.CTkFrame(
                    self.tabs_frame,
                    height=2,
                    width=80,
                    fg_color=COLORS['tiza_amarilla']
                )
                underline.place(in_=tab_frame, relx=0.5, rely=1.0, anchor="n", y=-5)
                self.tab_buttons[f"{pizarra['id']}_underline"] = underline

            # Guardar referencias
            self.tab_buttons[pizarra['id']] = {
                'frame': tab_frame,
                'inner': tab_inner,
                'label': tab_label,
                'entry': tab_entry
            }

        # Botón para agregar nueva pizarra
        btn_nueva = ctk.CTkButton(
            self.tabs_frame,
            text="+",
            font=('Segoe Print', 18, 'bold'),
            fg_color="transparent",
            text_color=COLORS['tiza_amarilla'],
            hover_color=COLORS['pizarra_borde'],
            border_width=1,
            border_color=COLORS['tiza_amarilla'],
            corner_radius=8,
            width=40,
            height=35,
            command=self._dialogo_nueva_pizarra
        )
        btn_nueva.pack(side="left", padx=5)

    def _cambiar_pestana(self, pizarra_id: str):
        """Cambia a una pestaña específica"""
        self.tab_manager.cambiar_pizarra_activa(pizarra_id)

    def _on_cambio_pestana(self, pizarra_id_nueva: str, pizarra_id_anterior: str):
        """Callback ejecutado cuando cambia la pestaña activa"""
        # Actualizar visualización de pestañas
        self._actualizar_pestanas()

        # Actualizar contenido
        self._mostrar_contenido_pizarra()

        # Guardar cambio
        self.datos['pizarra_activa'] = pizarra_id_nueva
        self._guardar_datos()

    def _actualizar_pestanas(self):
        """Actualiza la apariencia de las pestañas según la activa"""
        for pizarra in self.tab_manager.pizarras:
            tab_data = self.tab_buttons.get(pizarra['id'])
            if not tab_data or not isinstance(tab_data, dict):
                continue

            es_activa = pizarra['id'] == self.tab_manager.pizarra_activa_id

            # Actualizar estilo del frame
            tab_data['frame'].configure(
                fg_color="transparent" if not es_activa else COLORS['pizarra_borde']
            )

            # Manejar subrayado
            underline_key = f"{pizarra['id']}_underline"
            if es_activa:
                if underline_key not in self.tab_buttons:
                    underline = ctk.CTkFrame(
                        self.tabs_frame,
                        height=2,
                        width=80,
                        fg_color=COLORS['tiza_amarilla']
                    )
                    underline.place(in_=tab_data['frame'], relx=0.5, rely=1.0, anchor="n", y=-5)
                    self.tab_buttons[underline_key] = underline
            else:
                if underline_key in self.tab_buttons:
                    self.tab_buttons[underline_key].destroy()
                    del self.tab_buttons[underline_key]

    def _iniciar_edicion_pestana(self, pizarra_id: str):
        """Inicia la edición del nombre de una pestaña"""
        tab_data = self.tab_buttons.get(pizarra_id)
        if not tab_data or not isinstance(tab_data, dict):
            return

        # Obtener la pizarra
        pizarra = self.tab_manager.obtener_pizarra_por_id(pizarra_id)
        if not pizarra:
            return

        # Ocultar label
        tab_data['label'].pack_forget()

        # Mostrar entry con el nombre actual
        tab_data['entry'].delete(0, 'end')
        tab_data['entry'].insert(0, pizarra['nombre'])
        tab_data['entry'].pack(expand=True, padx=2, pady=2)
        tab_data['entry'].focus()
        tab_data['entry'].select_range(0, 'end')

        # Bindings para confirmar o cancelar
        tab_data['entry'].bind("<Return>", lambda e, pid=pizarra_id: self._confirmar_edicion_pestana(pid))
        tab_data['entry'].bind("<Escape>", lambda e, pid=pizarra_id: self._cancelar_edicion_pestana(pid))
        tab_data['entry'].bind("<FocusOut>", lambda e, pid=pizarra_id: self._confirmar_edicion_pestana(pid))

    def _confirmar_edicion_pestana(self, pizarra_id: str):
        """Confirma la edición del nombre de una pestaña"""
        tab_data = self.tab_buttons.get(pizarra_id)
        if not tab_data or not isinstance(tab_data, dict):
            return

        nuevo_nombre = tab_data['entry'].get().strip()

        # Obtener la pizarra actual
        pizarra = self.tab_manager.obtener_pizarra_por_id(pizarra_id)
        if not pizarra:
            self._finalizar_edicion_pestana(pizarra_id)
            return

        # Validar que no esté vacío y no sea igual al actual
        if nuevo_nombre and nuevo_nombre != pizarra['nombre']:
            # Validar que no exista otra pizarra con ese nombre
            nombres_existentes = [p['nombre'].lower() for p in self.tab_manager.pizarras if p['id'] != pizarra_id]
            if nuevo_nombre.lower() not in nombres_existentes and len(nuevo_nombre) <= 20:
                # Actualizar nombre en la pizarra
                pizarra['nombre'] = nuevo_nombre

                # Guardar datos
                self._guardar_datos()

        self._finalizar_edicion_pestana(pizarra_id)

    def _cancelar_edicion_pestana(self, pizarra_id: str):
        """Cancela la edición del nombre de una pestaña"""
        self._finalizar_edicion_pestana(pizarra_id)

    def _finalizar_edicion_pestana(self, pizarra_id: str):
        """Finaliza la edición del nombre de una pestaña"""
        tab_data = self.tab_buttons.get(pizarra_id)
        if not tab_data or not isinstance(tab_data, dict):
            return

        # Obtener la pizarra
        pizarra = self.tab_manager.obtener_pizarra_por_id(pizarra_id)
        if not pizarra:
            return

        # Ocultar entry
        tab_data['entry'].pack_forget()

        # Mostrar label con el nombre actualizado
        tab_data['label'].configure(text=pizarra['nombre'])
        tab_data['label'].pack(expand=True, fill="both", padx=5, pady=5)

    def _mostrar_contenido_pizarra(self):
        """Muestra el contenido de la pizarra activa"""
        # Limpiar contenido actual
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        self.task_widgets.clear()

        # Obtener pizarra activa
        pizarra_activa = self.tab_manager.obtener_pizarra_activa()

        if not pizarra_activa:
            return

        # Header con nombre y contador
        header_frame = ctk.CTkFrame(
            self.contenido_frame,
            fg_color="transparent"
        )
        header_frame.pack(fill="x", pady=(10, 15))

        # Nombre de la pizarra
        nombre_label = ctk.CTkLabel(
            header_frame,
            text=f"📋 {pizarra_activa['nombre']}",
            font=FONTS['tiza_subtitulo'],
            text_color=COLORS['tiza_amarilla'],
            fg_color="transparent"
        )
        nombre_label.pack(side="left")

        # Contador de tareas
        completadas, total = self.task_manager.contar_tareas_completadas(pizarra_activa)
        contador_label = ctk.CTkLabel(
            header_frame,
            text=f"{completadas}/{total}",
            font=FONTS['tiza_small'],
            text_color=COLORS['tiza_gris'],
            fg_color="transparent"
        )
        contador_label.pack(side="right")

        # Campo de entrada para nueva tarea
        input_frame = ctk.CTkFrame(
            self.contenido_frame,
            fg_color="transparent"
        )
        input_frame.pack(fill="x", pady=(0, 20))

        self.entrada_tarea = ctk.CTkEntry(
            input_frame,
            placeholder_text="Nueva tarea...",
            font=FONTS['tiza_normal'],
            fg_color=COLORS['pizarra_borde'],
            text_color=COLORS['tiza_blanca'],
            placeholder_text_color=COLORS['tiza_gris'],
            border_width=2,
            border_color=COLORS['tiza_amarilla'],
            height=40
        )
        self.entrada_tarea.pack(fill="x", side="left", expand=True, padx=(0, 10))
        self.entrada_tarea.bind("<Return>", lambda e: self._agregar_tarea())

        # Botón para agregar tarea
        btn_agregar = ctk.CTkButton(
            input_frame,
            text="+",
            font=('Segoe Print', 20, 'bold'),
            fg_color=COLORS['tiza_amarilla'],
            text_color=COLORS['pizarra_fondo'],
            hover_color=COLORS['tiza_blanca'],
            width=50,
            height=40,
            command=self._agregar_tarea
        )
        btn_agregar.pack(side="right")

        # Contenedor de tareas
        tareas_frame = ctk.CTkFrame(
            self.contenido_frame,
            fg_color="transparent"
        )
        tareas_frame.pack(fill="both", expand=True)

        # Mostrar tareas
        if pizarra_activa['tareas']:
            for tarea in pizarra_activa['tareas']:
                task_widget = TaskWidget(
                    tareas_frame,
                    tarea,
                    on_completar=self._on_completar_tarea,
                    on_eliminar=self._on_eliminar_tarea,
                    on_editar=self._on_editar_tarea,
                    on_reordenar=self._on_reordenar_tarea
                )
                task_widget.pack(fill="x", pady=3)
                self.task_widgets.append(task_widget)
        else:
            # Mensaje cuando no hay tareas
            mensaje = ctk.CTkLabel(
                tareas_frame,
                text="No hay tareas todavía\n\nEscribe en el campo de arriba y presiona Enter",
                font=FONTS['tiza_normal'],
                text_color=COLORS['tiza_gris'],
                fg_color="transparent",
                justify="center"
            )
            mensaje.pack(expand=True, pady=50)

    def _dialogo_nueva_pizarra(self):
        """Muestra el diálogo para crear una nueva pizarra"""
        dialog = ctk.CTkInputDialog(
            text="Nombre de la nueva pizarra:",
            title="Nueva Pizarra"
        )

        nombre = dialog.get_input()

        if nombre is None:  # Usuario canceló
            return

        nombre = nombre.strip()

        # Validar nombre
        es_valido, mensaje_error = self.tab_manager.validar_nombre_pizarra(nombre)

        if not es_valido:
            # Mostrar error
            error_dialog = ctk.CTkToplevel(self)
            error_dialog.title("Error")
            error_dialog.geometry("300x150")
            error_dialog.resizable(False, False)

            error_label = ctk.CTkLabel(
                error_dialog,
                text=mensaje_error,
                font=FONTS['tiza_normal'],
                wraplength=250
            )
            error_label.pack(pady=20)

            btn_ok = ctk.CTkButton(
                error_dialog,
                text="OK",
                command=error_dialog.destroy
            )
            btn_ok.pack(pady=10)

            # Centrar el diálogo
            error_dialog.transient(self)
            error_dialog.grab_set()

            return

        # Agregar pizarra
        nueva_pizarra = self.storage.agregar_pizarra(self.datos, nombre)

        if nueva_pizarra:
            # Actualizar tab manager
            self.tab_manager.agregar_pizarra(nueva_pizarra)

            # Guardar datos
            self._guardar_datos()

            # Recrear pestañas
            self._crear_pestanas()

            # Cambiar a la nueva pizarra
            self.tab_manager.cambiar_pizarra_activa(nueva_pizarra['id'])

    def _confirmar_eliminar_pizarra(self, pizarra_id: str):
        """Muestra diálogo de confirmación para eliminar una pizarra"""
        # Obtener la pizarra
        pizarra = self.tab_manager.obtener_pizarra_por_id(pizarra_id)
        if not pizarra:
            return

        # No permitir eliminar si es la única
        if len(self.tab_manager.pizarras) <= 1:
            return

        # Contar tareas
        num_tareas = len(pizarra['tareas'])
        mensaje = f"¿Eliminar la pizarra '{pizarra['nombre']}'?"
        if num_tareas > 0:
            mensaje += f"\n\nSe eliminarán {num_tareas} tarea(s)."

        # Crear diálogo de confirmación
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirmar eliminación")
        dialog.geometry("350x180")
        dialog.resizable(False, False)
        dialog.configure(fg_color=COLORS['pizarra_fondo'])

        # Mensaje
        mensaje_label = ctk.CTkLabel(
            dialog,
            text=mensaje,
            font=FONTS['tiza_normal'],
            text_color=COLORS['tiza_blanca'],
            wraplength=300,
            justify="center"
        )
        mensaje_label.pack(pady=(25, 20))

        # Frame para botones
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=10)

        # Botón Cancelar
        btn_cancelar = ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            font=FONTS['tiza_small'],
            fg_color=COLORS['pizarra_borde'],
            text_color=COLORS['tiza_blanca'],
            hover_color=COLORS['tiza_gris'],
            width=100,
            command=dialog.destroy
        )
        btn_cancelar.pack(side="left", padx=10)

        # Botón Eliminar
        btn_eliminar = ctk.CTkButton(
            btn_frame,
            text="Eliminar",
            font=FONTS['tiza_small'],
            fg_color="#8B0000",
            text_color=COLORS['tiza_blanca'],
            hover_color="#A52A2A",
            width=100,
            command=lambda: self._eliminar_pizarra(pizarra_id, dialog)
        )
        btn_eliminar.pack(side="left", padx=10)

        # Centrar el diálogo
        dialog.transient(self)
        dialog.grab_set()

    def _eliminar_pizarra(self, pizarra_id: str, dialog):
        """Elimina una pizarra después de confirmación"""
        dialog.destroy()

        # Eliminar de storage y tab_manager
        if self.storage.eliminar_pizarra(self.datos, pizarra_id):
            self.tab_manager.eliminar_pizarra(pizarra_id)

            # Guardar datos
            self._guardar_datos()

            # Actualizar pizarra activa en datos
            self.datos['pizarra_activa'] = self.tab_manager.pizarra_activa_id

            # Recrear pestañas
            self._crear_pestanas()

            # Mostrar contenido de la nueva pizarra activa
            self._mostrar_contenido_pizarra()

    def _agregar_tarea(self):
        """Agrega una nueva tarea a la pizarra activa"""
        # Obtener texto del campo de entrada
        texto = self.entrada_tarea.get().strip()

        if not texto:
            return

        # Obtener pizarra activa
        pizarra_activa = self.tab_manager.obtener_pizarra_activa()
        if not pizarra_activa:
            return

        # Agregar tarea
        tarea = self.task_manager.agregar_tarea(pizarra_activa, texto)

        if tarea:
            # Limpiar campo de entrada
            self.entrada_tarea.delete(0, 'end')

            # Guardar datos
            self._guardar_datos()

            # Refrescar contenido
            self._mostrar_contenido_pizarra()

            # Hacer focus en el campo de entrada
            self.entrada_tarea.focus()

    def _on_completar_tarea(self, tarea_id: str):
        """Callback cuando se completa/descompleta una tarea"""
        # Obtener pizarra activa
        pizarra_activa = self.tab_manager.obtener_pizarra_activa()
        if not pizarra_activa:
            return

        # Alternar estado de completada
        self.task_manager.alternar_completada(pizarra_activa, tarea_id)

        # Guardar datos
        self._guardar_datos()

        # Actualizar el widget específico
        for widget in self.task_widgets:
            if widget.tarea['id'] == tarea_id:
                widget.actualizar_tarea(widget.tarea)
                break

    def _on_eliminar_tarea(self, tarea_id: str):
        """Callback cuando se elimina una tarea"""
        # Obtener pizarra activa
        pizarra_activa = self.tab_manager.obtener_pizarra_activa()
        if not pizarra_activa:
            return

        # Eliminar tarea
        self.task_manager.eliminar_tarea(pizarra_activa, tarea_id)

        # Guardar datos
        self._guardar_datos()

        # Refrescar contenido
        self._mostrar_contenido_pizarra()

    def _on_editar_tarea(self, tarea_id: str, nuevo_texto: str):
        """Callback cuando se edita una tarea"""
        # Obtener pizarra activa
        pizarra_activa = self.tab_manager.obtener_pizarra_activa()
        if not pizarra_activa:
            return

        # Editar tarea
        self.task_manager.editar_tarea(pizarra_activa, tarea_id, nuevo_texto)

        # Guardar datos
        self._guardar_datos()

    def _on_reordenar_tarea(self, tarea_id: str, direccion: int):
        """Callback cuando se reordena una tarea mediante drag & drop"""
        # Obtener pizarra activa
        pizarra_activa = self.tab_manager.obtener_pizarra_activa()
        if not pizarra_activa:
            return

        # Reordenar tarea
        if self.task_manager.reordenar_tarea(pizarra_activa, tarea_id, direccion):
            # Guardar datos
            self._guardar_datos()

            # Refrescar contenido
            self._mostrar_contenido_pizarra()

    def _guardar_datos(self):
        """Guarda los datos en el almacenamiento"""
        self.storage.guardar_datos(self.datos)

    def _configurar_atajos_teclado(self):
        """Configura los atajos de teclado de la aplicación"""
        # Ctrl+N para nueva pizarra
        self.bind("<Control-n>", lambda e: self._dialogo_nueva_pizarra())

        # Ctrl+Tab para siguiente pizarra
        self.bind("<Control-Tab>", lambda e: self.tab_manager.siguiente_pizarra())

        # Ctrl+Shift+Tab para pizarra anterior
        self.bind("<Control-Shift-Tab>", lambda e: self.tab_manager.pizarra_anterior())

        # Ctrl+1 a Ctrl+9 para las primeras 9 pizarras
        for i in range(1, 10):
            self.bind(f"<Control-Key-{i}>", lambda e, idx=i-1: self._cambiar_a_pizarra_por_indice(idx))

    def _cambiar_a_pizarra_por_indice(self, indice: int):
        """Cambia a una pizarra por su índice"""
        pizarra = self.tab_manager.obtener_pizarra_por_indice(indice)
        if pizarra:
            self.tab_manager.cambiar_pizarra_activa(pizarra['id'])

    def ejecutar(self):
        """Inicia el loop principal de la aplicación"""
        self.mainloop()
