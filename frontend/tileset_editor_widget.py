from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QFileDialog, QSpinBox
from PyQt5.QtWidgets import QLabel, QPushButton, QCheckBox, QSizePolicy
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import Qt
import png

from frontend.editor_widget import EditorWidget


class TilesetEditorWidget(EditorWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trigger_set_tileset_ui_images.emit()
        self.trigger_set_palette_clickable.emit()

        self.add_tileset_options()
        self.left_lay.addStretch()
    
    def add_tileset_options(self):
        self.tileset_remove_flipped_checkbox = QCheckBox("Remove flipped")
        self.tileset_remove_flipped_checkbox.setFixedWidth(128)
        self.tileset_remove_rep_button = QPushButton("Remove Repeated Tiles")
        self.tileset_remove_rep_button.setFixedWidth(128)

        self.tileset_max_palettes_label = QLabel("Maximum Palettes:")
        self.tileset_max_palettes_label.setStyleSheet("margin-top: 12px;")
        self.tileset_max_palettes_label.setFixedWidth(128)
        self.tileset_max_palettes_spinbox = QSpinBox()
        self.tileset_max_palettes_spinbox.setRange(1, 7)
        self.tileset_max_palettes_spinbox.setFixedWidth(128)

        self.tileset_process_button = QPushButton("Process Tileset")
        self.tileset_process_button.setFixedWidth(128)

        self.tileset_group_layout = QVBoxLayout()

        self.tileset_group_layout.addWidget(self.tileset_remove_rep_button, alignment=Qt.AlignCenter)
        self.tileset_group_layout.addWidget(self.tileset_remove_flipped_checkbox, alignment=Qt.AlignCenter)

        self.tileset_group_layout.addWidget(self.tileset_max_palettes_label, alignment=Qt.AlignCenter)
        self.tileset_group_layout.addWidget(self.tileset_max_palettes_spinbox, alignment=Qt.AlignCenter)
        
        self.tileset_group_layout.addWidget(self.tileset_process_button, alignment=Qt.AlignCenter)
        self.tileset_groupbox = QGroupBox("Tileset")  # TODO: archivo de traducción!
        self.tileset_groupbox.setLayout(self.tileset_group_layout)
        self.tileset_groupbox.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

        self.left_lay.addWidget(self.tileset_groupbox)

        self.tileset_remove_rep_button.clicked.connect(lambda: self.remove_repeated_tiles(self.tileset_remove_flipped_checkbox.isChecked()))

        self.tileset_process_button.clicked.connect(lambda: self.process_tileset(self.tileset_max_palettes_spinbox.value()))

    def remove_repeated_tiles(self, remove_flipped):
        pass

    def process_tileset(self,max_palettes):
        print("gonorrea hijueputa", max_palettes)
        palettes = self.image.generate_palettes()
        self.palette_widget.set_color_data(palettes)

    def save_file(self):
        print("Tileset saving unavailable")
