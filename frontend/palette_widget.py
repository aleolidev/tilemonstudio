from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QSpacerItem
from PyQt5.QtWidgets import QLabel, QSlider, QPushButton, QGroupBox
from PyQt5.QtGui import QColor, QIcon, QPixmap, QCursor
from PyQt5.QtCore import Qt

class PaletteWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_gui()
        self.connect_signals()
    
    def load_gui(self):
        
        self.palettes_label = QLabel("Linkin park")
        self.palettes_label.setCursor(QCursor(Qt.PointingHandCursor))
        
        
        self.palettes_group_layout = QVBoxLayout()
        self.palettes_group_layout.addWidget(self.palettes_label)
        self.palette_groupbox = QGroupBox("Palettes")  # TODO: archivo de traducción!
        
        
        
        self.edit_color_group_layout = QVBoxLayout()
        self.edit_color_groupbox = QGroupBox("Edit color")  # TODO: archivo de traducción!
        
        self.lay = QVBoxLayout()
        self.lay.addWidget(self.palette_groupbox)
        self.lay.addWidget(self.edit_color_groupbox)
        self.setLayout(self.lay)
    
    def connect_signals(self):
        pass


