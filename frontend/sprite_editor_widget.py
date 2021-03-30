from PyQt5.QtWidgets import QLabel

from frontend.editor_widget import EditorWidget


class SpriteEditorWidget(EditorWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trigger_set_sprite_ui_images.emit()
        self.trigger_set_palette_clickable.emit()

        self.left_lay.addStretch()
        

            

