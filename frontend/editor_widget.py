from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QScrollArea, QLabel, QFileDialog, QShortcut
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QPixmap, QKeySequence
from frontend.palette_widget import PaletteWidget
from backend.image import Image as cim
from backend.palette import Palette as cpal
from backend.color_utilities import pil_to_pixmap, step

import numpy as np



class EditorWidget(QWidget):
    """
        Debería ser una clase abstracta pero no puedo hacerla heredar de ABC
        NO INSTANCIAR
        Para hacer un "Editor de X" tienes que heredar de esta clase e instanciar al hijo
    """
    trigger_set_sprite_ui_images = pyqtSignal()
    trigger_set_tileset_ui_images = pyqtSignal()
    trigger_set_background_ui_images = pyqtSignal()
    trigger_set_palette_clickable = pyqtSignal()

    MAX_SCALE_FACTOR = 16
    MIN_SCALE_FACTOR = .25
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions_queue = []
        self.action_queue_index = None  # porque parte vacía
        
        self.palette_widget = PaletteWidget()
        self.left_lay = QVBoxLayout()
        self.left_lay.addWidget(self.palette_widget)

        self.image_scale_factor = 1
        self.image_scroll_area = QScrollArea(alignment=Qt.AlignCenter)
        self.image_scroll_area.setStyleSheet("background-color: #b0b0b0;")  # TODO: parametrizar
        self.image_label = QLabel()
        self.image_scroll_area.setWidget(self.image_label)
        
        self.right_lay = QVBoxLayout()
        self.right_lay.addWidget(self.image_scroll_area)
        
        self.lay = QHBoxLayout()
        self.lay.addLayout(self.left_lay)
        self.lay.addLayout(self.right_lay)
        self.setLayout(self.lay)
        
        # SHORTCUTS!
        self.zoom_in_action = QShortcut(QKeySequence('Ctrl++'), self.image_scroll_area)
        self.zoom_in_action.activated.connect(self.zoom_in)
        self.zoom_out_action = QShortcut(QKeySequence('Ctrl+-'), self.image_scroll_area)
        self.zoom_out_action.activated.connect(self.zoom_out)

        # SIGNALS!
        self.connect_signals()

    def load_image(self, type_of_image: str):
        try:
            name, _ = QFileDialog.getOpenFileName(QFileDialog(),"Select " + type_of_image,"/","Image Files (*.png)")

            if name != "":
                self.file_name = QUrl.fromLocalFile(name).fileName()

                img = QPixmap(name)
                # self.set_viewer_image(img)

                return img
        except:
            pass

    def set_viewer_image(self, img: QPixmap):
        self.image_label.setPixmap(img)
        self.image_label.resize(img.size())

    def set_sprite_ui_images(self):
        self.sprite = self.load_image("Sprite")
        
        if self.sprite != None:
            self.image = cim(self.sprite)
            # self.set_viewer_image(self.image.raw_pixmap)
            
            raw_palette = list(np.array(self.image.rgb_image.getcolors(maxcolors=65536), dtype="object")[:,1])
            pal_sorted_by_color = self.image.sort_palette_by_colors(raw_palette, 8)
            self.palette = cpal(np.array(pal_sorted_by_color))
            palette_viewer = pil_to_pixmap(self.palette.get_paletteviewer_image())
            self.palette_widget.palettes_label.setPixmap(palette_viewer)
            self.palette_widget.palettes_label.resize(palette_viewer.size())
            
            self.set_viewer_image(pil_to_pixmap(self.image.rgb_image))
            self.palette_widget.set_color_data(pal_sorted_by_color[0])

    def set_tileset_ui_images(self):
        self.tileset = self.load_image("Tileset")
        
        if self.tileset != None:
            self.image = cim(self.tileset)
            self.set_viewer_image(self.image.raw_pixmap)
            
            raw_palette = list(np.array(self.image.rgb_image.getcolors(maxcolors=65536), dtype="object")[:,1])
            pal_sorted_by_color = self.image.sort_palette_by_colors(raw_palette, 8)
            self.palette = cpal(np.array(pal_sorted_by_color))
            palette_viewer = pil_to_pixmap(self.palette.get_paletteviewer_image())
            self.palette_widget.palettes_label.setPixmap(palette_viewer)
            self.palette_widget.palettes_label.resize(palette_viewer.size())

            self.set_viewer_image(pil_to_pixmap(self.image.rgb_image))
            self.palette_widget.set_color_data(pal_sorted_by_color[0])

    def set_background_ui_images(self):
        self.background = self.load_image("Background")
        
        if self.background != None:
            self.image = cim(self.background)
            self.set_viewer_image(self.image.raw_pixmap)
            
            raw_palette = list(np.array(self.image.rgb_image.getcolors(maxcolors=65536), dtype="object")[:,1])
            pal_sorted_by_color = self.image.sort_palette_by_colors(raw_palette, 8)
            self.palette = cpal(np.array(pal_sorted_by_color))
            palette_viewer = pil_to_pixmap(self.palette.get_paletteviewer_image())
            self.palette_widget.palettes_label.setPixmap(palette_viewer)
            self.palette_widget.palettes_label.resize(palette_viewer.size())

            self.set_viewer_image(pil_to_pixmap(self.image.rgb_image))
            self.palette_widget.set_color_data(pal_sorted_by_color[0])

            

    def set_palette_clickable(self):
        self.palette_widget.palettes_label.mousePressEvent = lambda event: self.palette_widget.set_clicked_color(event, self.palette)

    def register_new_action(self, action):
        if self.action_queue_index == len(self.actions_queue) - 1:
            # si estoy apuntando al tope del stack, lo añades encima
            self.actions_queue.append(action)
            self.actions_queue_index += 1
        else:
            # si no estoy en el tope del stack, borro todo lo que me sobra
            # y luego lo añado encima
            self.actions_queue[self.actions_queue_index+1:] = []
            self.actions_queue_index += 1
            self.actions_queue.append(action)

    def undo(self):
        # deshacer
        pass
    
    def redo(self):
        # rehacer
        pass

    def zoom_in(self):
        if self.image_scale_factor < self.MAX_SCALE_FACTOR:
            self.image_scale_factor *= 2
            self.update_scaled_img()
        elif self.image_scale_factor > self.MAX_SCALE_FACTOR:
            self.image_scale_factor = self.MAX_SCALE_FACTOR
            self.update_scaled_img()

    def zoom_out(self):
        if self.image_scale_factor > self.MIN_SCALE_FACTOR:
            self.image_scale_factor /= 2
            self.update_scaled_img()
        elif self.image_scale_factor < self.MIN_SCALE_FACTOR:
            self.image_scale_factor = self.MIN_SCALE_FACTOR
            self.update_scaled_img()
            
    def update_scaled_img(self):
        img = pil_to_pixmap(self.image.rgb_image.copy())
        # Get scaled sizes
        width, height = self.image_scale_factor*img.size().width(), self.image_scale_factor*img.size().height() 
        
        img = img.scaled(width, height, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.set_viewer_image(img)

    def connect_signals(self):
        self.trigger_set_sprite_ui_images.connect(self.set_sprite_ui_images)
        self.trigger_set_tileset_ui_images.connect(self.set_tileset_ui_images)
        self.trigger_set_background_ui_images.connect(self.set_background_ui_images)
        self.trigger_set_palette_clickable.connect(self.set_palette_clickable)

        self.palette_widget.red_slider.valueChanged.connect(lambda: self.palette_widget.slider_changed(self.palette, self.image, self.update_scaled_img))
        self.palette_widget.green_slider.valueChanged.connect(lambda: self.palette_widget.slider_changed(self.palette, self.image, self.update_scaled_img))
        self.palette_widget.blue_slider.valueChanged.connect(lambda: self.palette_widget.slider_changed(self.palette, self.image, self.update_scaled_img))

        self.palette_widget.red_spin_box.valueChanged.connect(lambda: self.palette_widget.spin_box_changed(self.palette, self.image, self.update_scaled_img))
        self.palette_widget.green_spin_box.valueChanged.connect(lambda: self.palette_widget.spin_box_changed(self.palette, self.image, self.update_scaled_img))
        self.palette_widget.blue_spin_box.valueChanged.connect(lambda: self.palette_widget.spin_box_changed(self.palette, self.image, self.update_scaled_img))

if __name__ == "__main__":
    a = EditorWidget()


