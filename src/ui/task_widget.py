"""
Widget para mostrar una tarea individual
"""
import customtkinter as ctk
from typing import Callable
from ui.styles import COLORS, FONTS


class TaskWidget(ctk.CTkFrame):
    """Widget que representa una tarea en el pizarrón"""

    def __init__(self, parent, tarea: dict, on_completar: Callable, on_eliminar: Callable, on_editar: Callable = None, on_reordenar: Callable = None, **kwargs):
        """
        Inicializa el widget de tarea

        Args:
            parent: Widget padre
            tarea: Diccionario con datos de la tarea
            on_completar: Callback cuando se completa/descompleta la tarea
            on_eliminar: Callback cuando se elimina la tarea
            on_editar: Callback cuando se edita la tarea (doble click)
            on_reordenar: Callback cuando se reordena la tarea (drag & drop)
        """
        super().__init__(parent, fg_color="transparent", **kwargs)

        self.tarea = tarea
        self.on_completar = on_completar
        self.on_eliminar = on_eliminar
        self.on_editar = on_editar
        self.on_reordenar = on_reordenar
        self.editando = False
        self.arrastrando = False
        self.indice_original = None

        self._crear_interfaz()

    def _crear_interfaz(self):
        """Crea la interfaz del widget de tarea"""
        # Frame contenedor principal con borde
        self.container = ctk.CTkFrame(
            self,
            fg_color=COLORS['pizarra_fondo'],
            border_width=1,
            border_color=COLORS['tiza_gris'],
            corner_radius=5
        )
        self.container.pack(fill="x", pady=5)

        # Frame interior para organizar elementos
        self.inner_frame = ctk.CTkFrame(
            self.container,
            fg_color="transparent"
        )
        self.inner_frame.pack(fill="x", padx=10, pady=8)

        # Grip para arrastrar (handle de drag)
        self.grip_label = ctk.CTkLabel(
            self.inner_frame,
            text="⋮⋮",
            font=('Arial', 14),
            text_color=COLORS['tiza_gris'],
            width=20,
            cursor="hand2"
        )
        self.grip_label.pack(side="left", padx=(0, 8))

        # Bindings para drag & drop en el grip
        self.grip_label.bind("<Button-1>", self._iniciar_arrastre)
        self.grip_label.bind("<B1-Motion>", self._durante_arrastre)
        self.grip_label.bind("<ButtonRelease-1>", self._finalizar_arrastre)

        # Checkbox para marcar como completada
        self.checkbox = ctk.CTkCheckBox(
            self.inner_frame,
            text="",
            width=20,
            checkbox_width=20,
            checkbox_height=20,
            fg_color=COLORS['tiza_amarilla'],
            hover_color=COLORS['tiza_blanca'],
            border_color=COLORS['tiza_gris'],
            command=self._on_checkbox_cambio
        )
        self.checkbox.pack(side="left", padx=(0, 10))

        if self.tarea['completada']:
            self.checkbox.select()

        # Frame para contener label y entry (para edición)
        self.texto_frame = ctk.CTkFrame(
            self.inner_frame,
            fg_color="transparent"
        )
        self.texto_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Label con el texto de la tarea
        texto_color = COLORS['tiza_gris'] if self.tarea['completada'] else COLORS['tiza_blanca']
        self.texto_label = ctk.CTkLabel(
            self.texto_frame,
            text=self.tarea['texto'],
            font=FONTS['tiza_normal'],
            text_color=texto_color,
            anchor="w",
            justify="left"
        )
        self.texto_label.pack(fill="x", expand=True)

        # Bind doble click para editar
        self.texto_label.bind("<Double-Button-1>", self._iniciar_edicion)

        # Entry para edición (inicialmente oculto)
        self.texto_entry = ctk.CTkEntry(
            self.texto_frame,
            font=FONTS['tiza_normal'],
            fg_color=COLORS['pizarra_borde'],
            text_color=COLORS['tiza_blanca'],
            border_width=2,
            border_color=COLORS['tiza_amarilla'],
            height=30
        )
        # No lo empaquetamos hasta que se necesite editar

        # Aplicar tachado si está completada
        if self.tarea['completada']:
            self._aplicar_tachado()

        # Botón para eliminar
        self.btn_eliminar = ctk.CTkButton(
            self.inner_frame,
            text="✕",
            width=30,
            height=30,
            font=('Segoe Print', 16, 'bold'),
            fg_color="transparent",
            text_color=COLORS['tiza_gris'],
            hover_color=COLORS['pizarra_borde'],
            command=self._on_eliminar_click
        )
        self.btn_eliminar.pack(side="right")

    def _on_checkbox_cambio(self):
        """Callback cuando cambia el estado del checkbox"""
        self.on_completar(self.tarea['id'])
        self._actualizar_apariencia()

    def _on_eliminar_click(self):
        """Callback cuando se hace click en eliminar"""
        self.on_eliminar(self.tarea['id'])

    def _iniciar_edicion(self, event=None):
        """Inicia el modo de edición de la tarea"""
        if self.editando or self.tarea['completada']:
            return  # No editar si ya está editando o está completada

        self.editando = True

        # Ocultar label
        self.texto_label.pack_forget()

        # Mostrar entry con el texto actual
        self.texto_entry.delete(0, 'end')
        self.texto_entry.insert(0, self.tarea['texto'])
        self.texto_entry.pack(fill="x", expand=True)
        self.texto_entry.focus()
        self.texto_entry.select_range(0, 'end')

        # Bindings para confirmar o cancelar
        self.texto_entry.bind("<Return>", self._confirmar_edicion)
        self.texto_entry.bind("<Escape>", self._cancelar_edicion)
        self.texto_entry.bind("<FocusOut>", self._confirmar_edicion)

    def _confirmar_edicion(self, event=None):
        """Confirma la edición y guarda el nuevo texto"""
        if not self.editando:
            return

        nuevo_texto = self.texto_entry.get().strip()

        if nuevo_texto and nuevo_texto != self.tarea['texto']:
            # Llamar al callback de edición
            if self.on_editar:
                self.on_editar(self.tarea['id'], nuevo_texto)
                self.tarea['texto'] = nuevo_texto

        self._finalizar_edicion()

    def _cancelar_edicion(self, event=None):
        """Cancela la edición sin guardar cambios"""
        self._finalizar_edicion()

    def _finalizar_edicion(self):
        """Finaliza el modo de edición"""
        if not self.editando:
            return

        self.editando = False

        # Ocultar entry
        self.texto_entry.pack_forget()

        # Mostrar label con el texto actual
        self.texto_label.configure(text=self.tarea['texto'])
        self.texto_label.pack(fill="x", expand=True)

    def _actualizar_apariencia(self):
        """Actualiza la apariencia según el estado de completada"""
        if self.tarea['completada']:
            self.texto_label.configure(text_color=COLORS['tiza_gris'])
            self._aplicar_tachado()
        else:
            self.texto_label.configure(text_color=COLORS['tiza_blanca'])
            self._quitar_tachado()

    def _aplicar_tachado(self):
        """Aplica efecto de tachado al texto"""
        # Crear texto tachado usando caracteres Unicode de strike-through
        texto_tachado = ''.join([char + '\u0336' for char in self.tarea['texto']])
        self.texto_label.configure(text=texto_tachado)

    def _quitar_tachado(self):
        """Quita el efecto de tachado"""
        self.texto_label.configure(text=self.tarea['texto'])

    def actualizar_tarea(self, tarea: dict):
        """
        Actualiza el widget con nuevos datos de tarea

        Args:
            tarea: Diccionario actualizado de la tarea
        """
        self.tarea = tarea

        # Actualizar checkbox
        if tarea['completada']:
            self.checkbox.select()
        else:
            self.checkbox.deselect()

        # Actualizar texto
        self.texto_label.configure(text=tarea['texto'])

        # Actualizar apariencia
        self._actualizar_apariencia()

    def _iniciar_arrastre(self, event):
        """Inicia el arrastre de la tarea"""
        if self.editando:
            return

        self.arrastrando = True
        self.start_y = event.y_root
        self.posiciones_a_mover = 0
        self.container.configure(border_color=COLORS['tiza_amarilla'], border_width=2)

    def _durante_arrastre(self, event):
        """Procesa el movimiento durante el arrastre - solo calcula, no aplica"""
        if not self.arrastrando:
            return

        # Calcular movimiento acumulado desde el inicio
        delta_y = event.y_root - self.start_y

        # Calcular cuántas posiciones mover basado en el movimiento total
        # Cada ~50 pixels equivale a una posición
        self.posiciones_a_mover = int(delta_y / 50)

    def _finalizar_arrastre(self, event):
        """Finaliza el arrastre y aplica el movimiento"""
        if self.arrastrando:
            self.arrastrando = False
            self.container.configure(border_color=COLORS['tiza_gris'], border_width=1)

            # Aplicar el movimiento al soltar
            if self.posiciones_a_mover != 0 and self.on_reordenar:
                self.on_reordenar(self.tarea['id'], self.posiciones_a_mover)

            self.posiciones_a_mover = 0
