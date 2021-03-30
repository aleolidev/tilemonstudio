from PyQt5.QtWidgets import QLabel

from frontend.editor_widget import EditorWidget


class TilesetEditorWidget(EditorWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trigger_set_tileset_ui_images.emit()
        self.trigger_set_palette_clickable.emit()

        self.left_lay.addStretch()

