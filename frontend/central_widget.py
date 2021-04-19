from PyQt5.QtWidgets import QWidget, QTabBar, QTabWidget, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence
# from frontend.editor_widget import EditorWidget
from frontend.image_editor_widget import ImageEditorWidget


class CentralWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.c = 0
        self.load_gui()
        self.connect_signals()
        self.show()
    
    def load_gui(self):
        self.lay = QVBoxLayout()
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.tab_bar = QTabWidget()
        self.tab_bar.setTabsClosable(True)
        self.lay.addWidget(self.tab_bar)
        self.setLayout(self.lay)

        self.close_current_tab = QShortcut(QKeySequence('Ctrl+W'), self.tab_bar)
        self.close_current_tab.activated.connect(lambda: self.close_tab(self.tab_bar.currentIndex()))
    
    def connect_signals(self):
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
    
    def add_tab(self, name, widget):
        # Es posible que tenga un botón como los navegadores, pero no lo veo necesario.
        # https://stackoverflow.com/questions/19975137/how-can-i-add-a-new-tab-button-next-to-the-tabs-of-a-qmdiarea-in-tabbed-view-m
        # label = QLabel(f"Hola Ikacito {self.c}")
        index = self.tab_bar.addTab(widget, name)

    def close_tab(self, index):
        # DO NOT DELETE REF!
        # ref: https://stackoverflow.com/questions/19151159/qtabwidget-close-tab-button-not-working
        # TODO: check if work is saved, show pop-up
        self.tab_bar.removeTab(index)

    def add_image_editor_tab(self, save_option, drag_path = None):
        if drag_path == None:
            sprite_editor_tab = ImageEditorWidget()
        else:
            sprite_editor_tab = ImageEditorWidget(drag_path)
        if sprite_editor_tab.sprite != None:
            if not save_option.isEnabled():
                save_option.setEnabled(True)
            self.add_tab(sprite_editor_tab.file_name, sprite_editor_tab)
            self.c += 1



