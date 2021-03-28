from PyQt5.QtWidgets import QLabel

from frontend.editor_widget import EditorWidget


class TilesetEditorWidget(EditorWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        label = QLabel("Este es un tileset-editor")
        self.left_lay.addWidget(label)

