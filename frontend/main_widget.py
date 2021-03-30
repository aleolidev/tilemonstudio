from PyQt5.QtWidgets import QMainWindow, QAction, QTabBar, QTabWidget

from frontend.central_widget import CentralWidget


class MainWidget(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tilemon Studio - Remake")
        self.resize(600, 500)
        # self.setMinimumHeight(400)
        # self.setMinimumWidth(500)
        self.load_gui()
        self.connect_signals()

    def load_gui(self):
        self.menu_bar = self.menuBar()
        # ACTIONS!
        self.create_sprite_action = QAction("&Create Sprite", self)
        self.load_sprite_action = QAction("&Load Sprite", self)
        self.create_tileset_action = QAction("&Create Tileset", self)
        self.load_tileset_action = QAction("&Load Tiileset", self)
        self.create_background_action = QAction("&Create Background", self)
        self.load_background_action = QAction("&Load Background", self)
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
            self.create_sprite_action,
            self.load_sprite_action,
            self.create_tileset_action,
            self.create_background_action,
            self.load_background_action,
            self.file_menu.addSeparator(),
            self.save_work_action,
            self.file_menu.addSeparator(),
            self.exit_action
        ])
        self.options_menu = self.menu_bar.addMenu("&Options")
        self.options_menu.addActions([
            self.set_to_4bpp_action,
            self.set_to_8bpp_action,
            self.slice_sprite_act
        ])
        self.help_menu = self.menu_bar.addMenu("&Help")
        self.help_menu.addActions([
            self.about_action
        ])
        # SHORTCUTS!
        self.create_sprite_action.setShortcut("Ctrl+I")
        self.load_sprite_action.setShortcut("Ctrl+Shift+I")
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
    
    def connect_signals(self):
        self.create_sprite_action.triggered.connect(self.central_widget.add_sprite_editor_tab)
        self.create_tileset_action.triggered.connect(self.central_widget.add_tileset_editor_tab)
        self.create_background_action.triggered.connect(self.central_widget.add_background_editor_tab)
