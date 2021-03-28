from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QScrollArea, QLabel
from PyQt5.QtCore import Qt
from frontend.palette_widget import PaletteWidget



class EditorWidget(QWidget):
    """
        Debería ser una clase abstracta pero no puedo hacerla heredar de ABC
        NO INSTANCIAR
        Para hacer un "Editor de X" tienes que heredar de esta clase e instanciar al hijo
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions_queue = []
        self.action_queue_index = None  # porque parte vacía
        
        self.palette_widget = PaletteWidget()
        
        self.left_lay = QVBoxLayout()
        self.left_lay.addWidget(self.palette_widget)
        
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


if __name__ == "__main__":
    a = EditorWidget()


