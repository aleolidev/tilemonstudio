from PyQt5.QtWidgets import QWidget, QTabBar, QTabWidget, QVBoxLayout, QLabel
from frontend.editor_widget import EditorWidget

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
        self.lay.addWidget(self.tab_bar)
        self.setLayout(self.lay)
    
    def connect_signals(self):
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
    
    def add_tab(self):
        # Es posible que tenga un botón como los navegadores, pero no lo veo necesario.
        # https://stackoverflow.com/questions/19975137/how-can-i-add-a-new-tab-button-next-to-the-tabs-of-a-qmdiarea-in-tabbed-view-m
        label = QLabel(f"Hola Ikacito {self.c}")
        editor = EditorWidget()
        index = self.tab_bar.addTab(editor, f"Tab {self.c}")
        self.c += 1
        # self.tab_bar.setTabButton()
        print("NEW TAB")
    
    def close_tab(self, index):
        # DO NOT DELETE REF!
        # ref: https://stackoverflow.com/questions/19151159/qtabwidget-close-tab-button-not-working
        # TODO: check if work is saved, show pop-up
        self.tab_bar.removeTab(index)

