from PyQt5.QtWidgets import QWidget, QHBoxLayout
from frontend.palette_widget import PaletteWidget



class EditorWidget(QWidget):
    """
        Debería ser una clase abstracta pero no puedo hacerla heredar de ABC
        NO INSTANCIAR
        Para hacer un "Editor de X" tienes que heredar de esta clase e instanciar al hijo
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.palette_widget = PaletteWidget()
        
        self.lay = QHBoxLayout()
        self.lay.addWidget(self.palette_widget)
        self.setLayout(self.lay)


if __name__ == "__main__":
    a = EditorWidget()


