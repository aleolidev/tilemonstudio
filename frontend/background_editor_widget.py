from PyQt5.QtWidgets import QLabel

from frontend.editor_widget import EditorWidget


class BackgroundEditorWidget(EditorWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trigger_set_background_ui_images.emit()
        self.trigger_set_palette_clickable.emit()

        self.left_lay.addStretch()

    def save_file(self):
        print("Background saving unavailable")
