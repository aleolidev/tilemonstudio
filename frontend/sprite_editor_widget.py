from PyQt5.QtWidgets import QLabel, QPushButton, QGroupBox, QVBoxLayout, QFileDialog
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt

from frontend.editor_widget import EditorWidget


class SpriteEditorWidget(EditorWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trigger_set_sprite_ui_images.emit()
        self.trigger_set_palette_clickable.emit()

        self.add_sprite_options()
        self.left_lay.addStretch()

    def add_sprite_options(self):
        self.sprite_index_button = QPushButton("Index Image")
        self.sprite_index_button.setFixedWidth(128)

        self.sprite_group_layout = QVBoxLayout()
        self.sprite_group_layout.addWidget(self.sprite_index_button, alignment=Qt.AlignCenter)
        self.sprite_groupbox = QGroupBox("Sprite")  # TODO: archivo de traducción!
        self.sprite_groupbox.setLayout(self.sprite_group_layout)
        self.sprite_groupbox.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

        self.left_lay.addWidget(self.sprite_groupbox)

        self.sprite_index_button.clicked.connect(lambda: self.reduce_sprite_palette(16))

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', '', '*.png')
        if file_name != "":
            self.image.rgb_image.save(file_name)
        

            

