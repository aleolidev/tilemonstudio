from PyQt5.QtWidgets import QWidget, QTabBar, QTabWidget, QVBoxLayout, QLabel
# from frontend.editor_widget import EditorWidget
from frontend.sprite_editor_widget import SpriteEditorWidget
from frontend.tileset_editor_widget import TilesetEditorWidget
from frontend.background_editor_widget import BackgroundEditorWidget


class CentralWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.c = 0
        self.load_gui()
        self.connect_signals()
        self.show()
    
    def load_gui(self):
        self.lay = QVBoxLayout()
        self.tab_bar = QTabWidget()
        self.tab_bar.setTabsClosable(True)
        # self.tab_bar.setStyleSheet("QTabWidget::pane { margin: 0px,0px,0px,0px; }")
        self.lay.addWidget(self.tab_bar)
        self.setLayout(self.lay)
    
    def connect_signals(self):
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
    
    def add_tab(self, name, widget):
        # Es posible que tenga un botón como los navegadores, pero no lo veo necesario.
        # https://stackoverflow.com/questions/19975137/how-can-i-add-a-new-tab-button-next-to-the-tabs-of-a-qmdiarea-in-tabbed-view-m
        # label = QLabel(f"Hola Ikacito {self.c}")
        index = self.tab_bar.addTab(widget, name)
        print("NEW TAB")
    
    def close_tab(self, index):
        # DO NOT DELETE REF!
        # ref: https://stackoverflow.com/questions/19151159/qtabwidget-close-tab-button-not-working
        # TODO: check if work is saved, show pop-up
        self.tab_bar.removeTab(index)

    def add_sprite_editor_tab(self, a, b):
        print(a, b)
        sprte_editor_tab = SpriteEditorWidget()
        self.add_tab(f"tab {self.c}", sprte_editor_tab)
        self.c += 1

    def add_tileset_editor_tab(self):
        tileset_editor_tab = TilesetEditorWidget()
        self.add_tab(f"tab {self.c}", tileset_editor_tab)
        self.c += 1
    
    def add_background_editor_tab(self):
        background_editor_tab = BackgroundEditorWidget()
        self.add_tab(f"tab {self.c}", background_editor_tab)
        self.c += 1



