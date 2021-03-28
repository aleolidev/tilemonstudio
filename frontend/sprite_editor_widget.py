from PyQt5.QtWidgets import QLabel

from frontend.editor_widget import EditorWidget


class SpriteEditorWidget(EditorWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        label = QLabel("Este es un sprite-editor")
        self.left_lay.addWidget(label)

