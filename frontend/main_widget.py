from PyQt5.QtWidgets import QMainWindow, QAction, QTabBar, QTabWidget
from PyQt5.QtCore import QMimeData, Qt

from frontend.central_widget import CentralWidget


class MainWidget(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Color Reductor")
        self.setAcceptDrops(True)
        self.resize(600, 500)

        # self.setMinimumHeight(400)
        # self.setMinimumWidth(500)
        self.load_gui()
        self.connect_signals()

    def load_gui(self):
        self.menu_bar = self.menuBar()
        # ACTIONS!
        # self.create_sprite_action = QAction("&Create Sprite", self)
        self.load_image_action = QAction("&Load Image", self)
        self.save_work_action = QAction("&Save", self)
        self.exit_action = QAction("&Exit", self)
        
        self.set_to_4bpp_action = QAction("&Set to 4BPP", self)
        self.set_to_8bpp_action = QAction("&Set to 8BPP", self)
        self.slice_sprite_act = QAction("&Slice Sprite", self)
        
        self.about_action = QAction("&About", self)
        self.about_action.setStatusTip("See information about this tool.")
        
        # MENUS!
        self.file_menu = self.menu_bar.addMenu("&File")
        self.file_menu.addActions([
            self.load_image_action,
            self.file_menu.addSeparator(),
            self.save_work_action,
            self.file_menu.addSeparator(),
            self.exit_action
        ])
        self.help_menu = self.menu_bar.addMenu("&Help")
        self.help_menu.addActions([
            self.about_action
        ])
        # SHORTCUTS!
        self.load_image_action.setShortcut("Ctrl+O")
        self.save_work_action.setShortcut("Ctrl+S")
        self.exit_action.setShortcut("Ctrl+Q")
        
        # OTHER STUFF!
        self.set_to_4bpp_action.setCheckable(True)
        self.set_to_8bpp_action.setCheckable(True)
        self.set_to_4bpp_action.setChecked(False)
        self.set_to_8bpp_action.setChecked(False)
        self.save_work_action.setDisabled(True)
        self.set_to_4bpp_action.setDisabled(True)
        self.set_to_8bpp_action.setDisabled(True)
        self.slice_sprite_act.setDisabled(True)
        
        self.setMenuBar(self.menu_bar)
        
        self.central_widget = CentralWidget(self)
        self.setCentralWidget(self.central_widget)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            if file_path.lower().endswith('.png'):
                self.central_widget.add_image_editor_tab(self.save_work_action, file_path)
            
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def connect_signals(self):
        self.load_image_action.triggered.connect(lambda: self.central_widget.add_image_editor_tab(self.save_work_action))
        self.save_work_action.triggered.connect(lambda: self.central_widget.tab_bar.currentWidget().save_file())
