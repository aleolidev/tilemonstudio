from PyQt5.QtWidgets import QLabel, QPushButton, QGroupBox, QVBoxLayout, QFileDialog
from PyQt5.QtWidgets import QSizePolicy, QSpinBox
from PyQt5.QtCore import Qt
from PIL import Image as pim
import math
import png

from frontend.editor_widget import EditorWidget

class ImageEditorWidget(EditorWidget):
    RGB_COLOR_COUNT = 256
    GRAYSCALE_COLOR_COUNT= 256
    def __init__(self, drag_path = None):
        super().__init__()
        self.trigger_set_sprite_ui_images.emit(drag_path)
        if self.sprite != None:
            self.trigger_set_palette_clickable.emit()

            self.add_sprite_options()
            self.left_lay.addStretch()

    def add_sprite_options(self):
        self.sprite_colors_amount_label = QLabel("Max Colors:")
        self.sprite_colors_amount_label.setFixedWidth(128)
        self.sprite_colors_amount_spinbox = QSpinBox()
        self.sprite_colors_amount_spinbox.setFixedWidth(128)
        self.sprite_index_button = QPushButton("Index Image")
        self.sprite_index_button.setFixedWidth(128)

        palette_value = len(self.palette.palette)
        if(len(self.palette.palette) > 256):
            palette_value = 256

        self.sprite_colors_amount_spinbox.setRange(2, palette_value)
        self.sprite_colors_amount_spinbox.setValue(palette_value)

        self.sprite_group_layout = QVBoxLayout()
        self.sprite_group_layout.addWidget(self.sprite_colors_amount_label, alignment=Qt.AlignCenter)
        self.sprite_group_layout.addWidget(self.sprite_colors_amount_spinbox, alignment=Qt.AlignCenter)
        self.sprite_group_layout.addWidget(self.sprite_index_button, alignment=Qt.AlignCenter)
        self.sprite_groupbox = QGroupBox("Sprite")  # TODO: archivo de traducción!
        self.sprite_groupbox.setLayout(self.sprite_group_layout)
        self.sprite_groupbox.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

        self.left_lay.addWidget(self.sprite_groupbox)

        self.sprite_index_button.clicked.connect(lambda: self.index_sprite(self.sprite_colors_amount_spinbox.value()))

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', self.file_name, '*.png')
        if file_name != "":
            im, pal = self.format_save_sprite(self.sprite_colors_amount_spinbox.value())
            
            with open(file_name, 'wb') as f:
                png_writer = png.Writer(im.shape[1], im.shape[0], palette=pal)
                png_writer.write(f, im)
        

    def change_color_depth(self, image, color_count):
        if image.mode == 'L':
            raito = self.GRAYSCALE_COLOR_COUNT / color_count
            change = lambda value: math.trunc(value/raito)*raito
            return image.point(change)
        
        if image.mode == 'RGB' or image.mode == 'RGBA':
            raito = self.RGB_COLOR_COUNT / color_count
            change = lambda value: math.trunc(value/raito)*raito
            return pim.eval(image, change)
        
        raise ValueError('Images in {mode} cannot de used.'.format(mode=image.mode))

            

