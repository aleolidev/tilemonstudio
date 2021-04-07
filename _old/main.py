# This Python file uses the following encoding: utf-8 
import sys
import resources
import png
import io
import time
import numpy as np
import math
from numpy import random
import colorsys
from sklearn import cluster
from colors import rgb, hex
from PIL import Image, ImageQt, ImageColor
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class TilemonStudioWindow(QMainWindow):
    def __init__(self):
        self.load_init_window_toolbar()
        #self.load_tileset_window()

    def load_init_window_toolbar(self):
        QMainWindow.__init__(self)
        
        self.set_window_basic_info("Tilemon Studio", (248, 200), True)

        # Creates a Sprite From a RAW Image
        self.createSpriteAct = QAction('&Create Sprite', self)
        self.createSpriteAct.setShortcut('Ctrl+I')
        self.createSpriteAct.triggered.connect(lambda *args: self.create_sprite_triggered())

        # Load a Sprite
        self.loadSpriteAct = QAction('&Load Sprite', self)
        self.loadSpriteAct.setShortcut('Ctrl+Shift+I')

        # Creates a Tileset From RAW Image
        self.createTilesetAct = QAction('&Create Tileset', self)
        self.createTilesetAct.setShortcut('Ctrl+T')

        # Load a Tileset
        self.loadTilesetAct = QAction('&Load Tileset', self)
        self.loadTilesetAct.setShortcut('Ctrl+Shift+T')

        # Creates a Background From RAW Image
        self.createBackgroundAct = QAction('&Create Background', self)
        self.createBackgroundAct.setShortcut('Ctrl+B')

        # Load a Background
        self.loadBackgroundAct = QAction('&Load Background', self)
        self.loadBackgroundAct.setShortcut('Ctrl+Shift+B')

        # Exit application
        self.exitAct = QAction('&Exit', self)
        self.exitAct.setShortcut('Ctrl+Q')
        self.exitAct.triggered.connect(qApp.quit)

        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&File')
        self.fileMenu.addAction(self.createSpriteAct)
        self.fileMenu.addAction(self.loadSpriteAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.createTilesetAct)
        self.fileMenu.addAction(self.loadTilesetAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.createBackgroundAct)
        self.fileMenu.addAction(self.loadBackgroundAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        """self.solidColorOption = QAction('&Solid Color', self)
        self.solidColorOption.setCheckable(True)
        self.solidColorOption.setChecked(True)
        self.solidColorOption.setStatusTip('Set the background color to a solid color')

        self.transpColorOption = QAction('&Transparent Color', self)
        self.transpColorOption.setCheckable(True)
        self.transpColorOption.setChecked(False)
        self.transpColorOption.setStatusTip('Set the background color to transparent')

        self.keepAbundantOption = QAction('&Area Coverage', self)
        self.keepAbundantOption.setCheckable(True)
        self.keepAbundantOption.setChecked(False)
        self.keepAbundantOption.setStatusTip('While reducting colors, keep the most abundant in the image')

        self.avgColorOption = QAction('&Average Color', self)
        self.avgColorOption.setCheckable(True)
        self.avgColorOption.setChecked(False)
        self.avgColorOption.setStatusTip('While reducting colors, uses an average color')

        self.kMeansOption = QAction('&K-Means', self)
        self.kMeansOption.setCheckable(True)
        self.kMeansOption.setChecked(True)
        self.kMeansOption.setStatusTip('K-Means method for calculate average color by groups')

        self.refactorTilesetOption = QAction('&Refactor tileset', self)
        self.refactorTilesetOption.setCheckable(True)
        self.refactorTilesetOption.setChecked(False)
        self.refactorTilesetOption.setStatusTip('Refactor the tileset removing void tiles')

        self.removeRepTilesOption = QAction('&Remove repeated tiles', self)
        self.removeRepTilesOption.setCheckable(True)
        self.removeRepTilesOption.setChecked(True)
        self.removeRepTilesOption.setStatusTip('Optimize tileset removing repeated tiles')

        self.removeRepFlipTilesOption = QAction('&Remove repeated (flipped) tiles', self)
        self.removeRepFlipTilesOption.setCheckable(True)
        self.removeRepFlipTilesOption.setChecked(True)
        self.removeRepFlipTilesOption.setStatusTip('Optimize tileset removing repetead flipped tiles')

        self.options = self.menubar.addMenu('&Options')
        self.options.addAction(self.solidColorOption)
        self.options.addAction(self.transpColorOption)
        self.options.addSeparator()
        self.options.addAction(self.keepAbundantOption)
        self.options.addAction(self.avgColorOption)
        self.options.addAction(self.kMeansOption)
        self.options.addSeparator()
        self.options.addAction(self.refactorTilesetOption)
        self.options.addSeparator()
        self.options.addAction(self.removeRepTilesOption)
        self.options.addAction(self.removeRepFlipTilesOption)"""

        self.infoAct = QAction('&Info', self)
        self.infoAct.setStatusTip('See information')

        self.helpMenu = self.menubar.addMenu('&Help')
        self.helpMenu.addAction(self.infoAct)


    # deprecated
    def set_window_basic_info(self, title, size:tuple, isFixed):
        self.setWindowTitle(title)
        width, height = size
        if isFixed:
            self.setFixedSize(width, height)
        else:
            # Everything is needed to ensure the QMainWindow is resizable and maximizable
            self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint | Qt.WindowMaximizeButtonHint)
            self.setMaximumSize(QWIDGETSIZE_MAX,QWIDGETSIZE_MAX)
            self.setMinimumSize(0,0)
            self.resize(width, height)
            self.show()

    def load_sprite_window(self):
        """

        """
        ### Set basic information
        self.set_window_basic_info("Tilemon Studio - Sprites", (448, 400), False)  # deprecated

        if True:
            ### Set Toolbar 
            self.menubar.clear()
            self.menubar = self.menuBar()
            
            # Save the Sprite
            self.saveSpriteAct = QAction('&Save Sprite', self)
            self.saveSpriteAct.setShortcut('Ctrl+S')
            # self.saveSpriteAct.triggered.connect(lambda *args: self.create_sprite_triggered())

            # Set Sprite To 4BPP
            self.setTo4BPPAct = QAction('&Set to 4BPP', self)
            self.setTo4BPPAct.setCheckable(True)
            # Set Sprite To 8BPP
            self.setTo8BPPAct = QAction('&Set to 8BPP', self)
            self.setTo8BPPAct.setCheckable(True)
            # Gives The Option of Slice the Sprite
            self.sliceSpriteAct = QAction('&Slice Sprite', self)
            self.sliceSpriteAct.setCheckable(True)
            self.sliceSpriteAct.setChecked(False)

            self.fileMenu = self.menubar.addMenu('&File')
            self.fileMenu.addAction(self.createSpriteAct)
            self.fileMenu.addAction(self.loadSpriteAct)
            self.fileMenu.addAction(self.saveSpriteAct)
            self.fileMenu.addSeparator()
            self.fileMenu.addAction(self.exitAct)

            self.options = self.menubar.addMenu('&Options')
            self.options.addAction(self.setTo4BPPAct)
            self.options.addAction(self.setTo8BPPAct)
            self.options.addSeparator()
            self.options.addAction(self.sliceSpriteAct)

            self.helpMenu = self.menubar.addMenu('&Help')
            self.helpMenu.addAction(self.infoAct)

        ### Set Graphical User Interface
        self.mainLayout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()

        # Set left side panels
        self.sprite_pal_manager = PaletteManagerWidget(self)  
        
        self.leftLayout.addWidget(self.sprite_pal_manager)
        self.leftLayout.addStretch()

        # Set right side panels (Show sprite)
        self.rightLayout.setContentsMargins(0,0,0,0)
        self.scrollAreaImage = QScrollArea(alignment=Qt.AlignCenter)
        self.scrollAreaImage.imageLabel = QLabel()
        self.scrollAreaImage.setStyleSheet("background-color:#b0b0b0;")
        self.scrollAreaImage.setWidget(self.scrollAreaImage.imageLabel)
        self.rightLayout.addWidget(self.scrollAreaImage)

        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.rightLayout)
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)



    def load_tileset_window(self):
        self.mainLayout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()
        self.leftLayout.setContentsMargins(0, 10, 0, 10)
        self.rightLayout.setContentsMargins(0, 10, 0, 10)

        self.scrollAreaProc = QScrollArea()
        self.scrollAreaDef = QScrollArea()
        self.scrollAreaPal = QScrollArea()
        self.scrollAreaProc.label = QLabel()
        self.scrollAreaDef.label = QLabel()
        self.scrollAreaPal.label = QLabel()
        self.scrollAreaProc.setWidget(self.scrollAreaProc.label)
        self.scrollAreaDef.setWidget(self.scrollAreaDef.label)
        self.scrollAreaPal.setWidget(self.scrollAreaPal.label)
        self.tabWidget = QTabWidget()
        self.tabWidget.setFixedSize(186, 334)
        self.tabWidget.addTab(self.scrollAreaProc, "Processed")
        self.tabWidget.addTab(self.scrollAreaPal, "Palettes")
        self.tabWidget.addTab(self.scrollAreaDef, "Original")

        self.colorSetLayout = QVBoxLayout()
        self.colorSetLayout.setContentsMargins(0, 0, 0, 3)
        self.colorLabelLayout = QHBoxLayout()
        self.colorPicker = QHBoxLayout()
        self.bgColorLabel = QLabel("Background Color:")
        self.backgroundColor = QColor(224, 224, 224)
        self.showColorLabel = QLabel(self.backgroundColor.name())
        self.showColorLabel.setAlignment(Qt.AlignCenter)
        self.showColorLabel.setFixedSize(100, 20)
        self.showColorLabel.setStyleSheet("background-color: " + self.backgroundColor.name() + "; color: #222;")
        self.eyeDropperIcon = QIcon(":/icons/eyedropper.png")
        self.pickColor = QPushButton()
        self.pickColor.setFixedSize(24, 24)
        self.pickColor.setIcon(self.eyeDropperIcon)
        self.colorStretch = QSpacerItem(0, 0, QSizePolicy.Expanding)

        if self.solidColorOption.isChecked():
            self.colorLabelLayout.addWidget(self.bgColorLabel)
            self.colorPicker.addWidget(self.showColorLabel)
            self.colorPicker.addWidget(self.pickColor)
            self.colorPicker.addItem(self.colorStretch)

        self.colorSetLayout.addLayout(self.colorLabelLayout)
        self.colorSetLayout.addLayout(self.colorPicker)

        self.leftLayout.addLayout(self.colorSetLayout)

        self.setColorsLayout = QVBoxLayout()
        self.subSetColorsLayout = QHBoxLayout()
        self.subSetColorsLayout.setContentsMargins(0, 0, 0, 0)
        self.subSetColorsLabel = QLabel("Maximum colors:")
        self.subSetColorsSpin = QSpinBox()
        self.subSetColorsSpin.setFixedSize(37, 22)
        self.subSetColorsStretch = QSpacerItem(0, 0, QSizePolicy.Expanding)
        self.setColorsButton = QPushButton("Set Colors")

        #if self.maxPaletteAction.isChecked():
        self.subSetColorsLayout.addWidget(self.subSetColorsLabel)
        self.subSetColorsLayout.addWidget(self.subSetColorsSpin)
        self.subSetColorsLayout.addItem(self.subSetColorsStretch)
        self.setColorsLayout.addLayout(self.subSetColorsLayout)
        self.setColorsLayout.addWidget(self.setColorsButton)

        self.leftLayout.addLayout(self.setColorsLayout)

        self.selPaletteLayout = QHBoxLayout()
        self.selPaletteLayout.setContentsMargins(0, 0, 0, 6)
        self.selPaletteLabel = QLabel("Tileset Palette:")
        self.selPaletteSpin = QSpinBox()
        self.selPaletteSpin.setFixedSize(37, 22)
        self.selPaletteStretch = QSpacerItem(0, 0, QSizePolicy.Expanding)

        self.selPaletteLayout.addWidget(self.selPaletteLabel)
        self.selPaletteLayout.addWidget(self.selPaletteSpin)
        self.selPaletteLayout.addItem(self.selPaletteStretch)

        self.leftLayout.addLayout(self.selPaletteLayout)

        self.rightLayout.addWidget(self.tabWidget)


        self.createTilesetAct.triggered.connect(lambda *args: self.select_file())
        self.solidColorOption.triggered.connect(lambda *args: self.set_solid_color())
        self.transpColorOption.triggered.connect(lambda *args: self.set_transparent_background())
        self.avgColorOption.triggered.connect(lambda *args: self.set_average_color_trigger())
        self.kMeansOption.triggered.connect(lambda *args: self.set_kmeans_trigger())
        self.keepAbundantOption.triggered.connect(lambda *args: self.set_abundant_color())
        self.removeRepTilesOption.triggered.connect(lambda *args: self.handle_remove_dup_tiles())
        self.pickColor.clicked.connect(lambda *args: self.pick_color_function())
        self.setColorsButton.clicked.connect(lambda *args: self.recalculate_palette_reduction())
        #self.reductionThresholdSlider.valueChanged[int].connect(lambda *args: self.sliderThresholdChanged())

        #self.reductionThresholdSlider.sliderReleased.connect(lambda *args: self.recalculate_palette_reduction())

        self.leftLayout.addStretch()
        self.rightLayout.addStretch()
        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.rightLayout)
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

        self.set_enabled_state_about_open(False)

    
    def create_sprite_triggered(self):
        pixmap = self.select_file("Select Sprite Image")
        
        pilimg = pixmap2pil(pixmap)
        self.sprite_pal = Palette(np.array([elem[1] for elem in (pilimg.getcolors(maxcolors=65536))]))
        
        self.load_sprite_window()

        self.scrollAreaImage.imageLabel.setPixmap(pixmap)
        self.scrollAreaImage.imageLabel.resize(pixmap.size())

        self.sprite_pal_manager.palettesLabel.setPixmap(pil2pixmap(self.sprite_pal.get_paletteviewer_image()))

    def set_solid_color(self):
        if self.sender().isChecked() == False:
            self.sender().setChecked(True)
        else:
            self.transpColorOption.setChecked(False)
        self.load_left_options()

    def set_transparent_background(self):
        if self.sender().isChecked() == False:
            self.sender().setChecked(True)
        else:
            self.solidColorOption.setChecked(False)
        self.load_left_options()

    def set_abundant_color(self):
        if self.sender().isChecked() == False:
            self.sender().setChecked(True)
        else:
            self.avgColorOption.setChecked(False)
            self.kMeansOption.setChecked(False)
            self.recalculate_palette_reduction()

    def set_average_color_trigger(self):
        if self.sender().isChecked() == False:
            self.sender().setChecked(True)
        else:
            self.keepAbundantOption.setChecked(False)
            self.kMeansOption.setChecked(False)
            self.recalculate_palette_reduction()

    def set_kmeans_trigger(self):
        if self.sender().isChecked() == False:
            self.sender().setChecked(True)
        else:
            self.keepAbundantOption.setChecked(False)
            self.avgColorOption.setChecked(False)
            self.recalculate_palette_reduction()

    def handle_remove_dup_tiles(self):
        if self.sender().isChecked():
            self.removeRepFlipTilesOption.setEnabled(True)
        else:
            self.removeRepFlipTilesOption.setEnabled(False)

    def get_reduction_method(self):
        if self.avgColorOption.isChecked():
            return 1
        elif self.kMeansOption.isChecked():
            return 2
        #Default
        else:
            return 0

    def pick_color_function(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.backgroundColor = col
            rgbColor = ImageColor.getcolor(col.name(), "RGB")
            self.showColorLabel.setText(self.backgroundColor.name())
            self.processedImage.bgColor = rgbColor
            if self.processedImage.get_color_value(np.array(rgbColor)) < 500:
                self.showColorLabel.setStyleSheet("background-color: " + self.backgroundColor.name() + "; color: #fff;")
            else:
                self.showColorLabel.setStyleSheet("background-color: " + self.backgroundColor.name() + "; color: #222;")

    def recalculate_palette_reduction(self):

        procImg = self.processedImage.rawPixmap.copy()

        colorsToSet = (self.subSetColorsSpin.value())
        if colorsToSet <= 1:
            imgSize = (self.processedImage.rawPixmap.width(), self.processedImage.rawPixmap.height())
            procImg = pil2pixmap(Image.new("RGB", imgSize, self.processedImage.bgColor))
            self.processedImage.toProcessTileset = self.processedImage.rgba_to_RBG_and_BG_color(pixmap2pil(procImg), self.processedImage.bgColor)
        else:
            procImg = pixmap2pil(procImg)
            procImg = self.processedImage.reduct_palettes(procImg, colorsToSet, self.get_reduction_method())
            self.processedImage.toProcessTileset = self.processedImage.rgba_to_RBG_and_BG_color(procImg, self.processedImage.bgColor)
        procImg = self.processedImage.toProcessTileset

        processedPix = pil2pixmap(procImg)
        self.scrollAreaProc.label.setPixmap(processedPix)
        self.scrollAreaProc.label.resize(processedPix.size())

        imgPalettes = np.array(list(self.processedImage.generate_palettes()))
        #imgPalettes = np.array([elem[1] for elem in (procImg.getcolors())])
        imgPalettes = create_image_from_palette(imgPalettes)
        imgPalettes = pil2pixmap(imgPalettes)
        self.scrollAreaPal.label.setPixmap(imgPalettes)
        self.scrollAreaPal.label.resize(imgPalettes.size())

    def set_enabled_state_about_open(self, disable):
        self.importTilesetAct.setEnabled(disable)
        self.exportTilesetAct.setEnabled(disable)
        self.exportSelPaletteAct.setEnabled(disable)
        self.exportAllPalettesAct.setEnabled(disable)

        self.solidColorOption.setEnabled(disable)
        self.transpColorOption.setEnabled(disable)
        self.keepAbundantOption.setEnabled(disable)
        self.avgColorOption.setEnabled(disable)
        self.kMeansOption.setEnabled(disable)
        self.refactorTilesetOption.setEnabled(disable)
        self.removeRepTilesOption.setEnabled(disable)
        self.removeRepFlipTilesOption.setEnabled(disable)

        self.tabWidget.setEnabled(disable)

        self.bgColorLabel.setEnabled(disable)
        self.showColorLabel.setEnabled(disable)
        self.pickColor.setEnabled(disable)

        self.subSetColorsLabel.setEnabled(disable)
        self.subSetColorsSpin.setEnabled(disable)
        self.setColorsButton.setEnabled(disable)

        self.selPaletteLabel.setEnabled(disable)
        self.selPaletteSpin.setEnabled(disable)

    def load_left_options(self):
        #Hide all widgets
        self.bgColorLabel.setParent(None)
        self.showColorLabel.setParent(None)
        self.colorPicker.removeItem(self.colorStretch)
        self.pickColor.setParent(None)

        if self.solidColorOption.isChecked():
            self.colorLabelLayout.addWidget(self.bgColorLabel)
            self.colorPicker.addWidget(self.showColorLabel)
            self.colorPicker.addWidget(self.pickColor)
            self.colorPicker.addItem(self.colorStretch)

    def select_file(self, dialog_name):
        try:
            if getattr(sys, 'frozen', False):
                application_path = os.path.dirname(sys.executable)
            elif __file__:
                application_path = os.path.dirname(__file__)
            name, _ = QFileDialog.getOpenFileName(QFileDialog(), dialog_name, application_path,"Image Files (*.png)")

            if name != "":
                pixmap = QPixmap(name)
                return pixmap
                """self.scrollAreaDef.label.setPixmap(pixmap)
                self.scrollAreaDef.label.resize(pixmap.size())

                self.processedImage = Tileset(False, pixmap)

                self.processedImage.toProcessTileset = self.processedImage.reduce_duplicate_tiles(self.processedImage.toProcessTileset, self.refactorTilesetOption.isChecked(), self.removeRepFlipTilesOption.isChecked())
                processedPix = pil2pixmap(self.processedImage.toProcessTileset)
                self.scrollAreaProc.label.setPixmap(processedPix)
                self.scrollAreaProc.label.resize(processedPix.size())
                self.set_enabled_state_about_open(True)

                hexColor = '#%02x%02x%02x' % self.processedImage.bgColor
                if self.processedImage.get_color_value(self.processedImage.bgColor) < 500:
                    self.showColorLabel.setStyleSheet("background-color: " + hexColor + "; color: #fff;")
                else:
                    self.showColorLabel.setStyleSheet("background-color: " + hexColor + "; color: #222;")

                self.showColorLabel.setText(hexColor)

                colorsAmount = self.processedImage.get_colors_amount(self.processedImage.toProcessTileset)
                self.subSetColorsSpin.setRange(1, colorsAmount)
                self.subSetColorsSpin.setValue(colorsAmount)

                #imgPalettes = (self.processedImage.toProcessTileset.getcolors())[1::2,:]
                #imgPalettes = np.array([elem[1] for elem in (self.processedImage.toProcessTileset.getcolors())])
                imgPalettes = np.array(list(self.processedImage.generate_palettes()))
                imgPalettes = create_image_from_palette(imgPalettes)
                imgPalettes = pil2pixmap(imgPalettes)
                #self.processedImage.generate_tile(self.processedImage.toProcessTileset, 1, 0)
                #imgPalettes = pil2pixmap(self.processedImage.get_tile(self.processedImage.toProcessTileset, 1, 0))
                self.scrollAreaPal.label.setPixmap(imgPalettes)
                self.scrollAreaPal.label.resize(imgPalettes.size())

                self.processedImage.generate_palettes()"""
        except:
            print("Error opening the image file")

class Tileset():
    def __init__(self, isTransparent, rawPixmap):
        self.isTransparent = isTransparent
        self.rawPixmap = rawPixmap
        self.bgColor = self.get_bg_color(np.array(pixmap2pil(rawPixmap)))
        self.toProcessTileset = self.rgba_to_RBG_and_BG_color(pixmap2pil(rawPixmap), self.bgColor)
        self.listOfTiles = {}
        
        self.slice_tileset()

    def get_tile(self, image, x, y):
        tile = image.crop((x*8, y*8, (x+1)*8, (y+1)*8))
        return tile

    def generate_tile(self, image, x, y):
        tileImg = self.get_tile(image, x, y)
        tileId = y*(image.size[0] // 8) + x
        tilePal, colorsAmount = self.get_palette_set(tileImg, self.bgColor)
        tile = Tile(tileId, tilePal, colorsAmount)
        return tile

    def slice_tileset(self):
        self.listOfTiles = {}
        image = self.toProcessTileset
        voidTile = Image.new("RGB", (8, 8), self.bgColor)
        for y in range(image.size[1] // 8):
            for x in range(image.size[0] // 8):
                tile = self.generate_tile(image, x, y)
                if self.get_tile(image, x, y) != voidTile:
                    self.listOfTiles[tile.tileId] = tile

    def get_sortedlist_tiles(self):
        return sorted(self.listOfTiles.values(), key = lambda x: x.colAmount)
    
    def generate_palettes(self):

        self.slice_tileset()

        tilepals = list(map(lambda x: x.pal,self.listOfTiles.values()))
        pals = self.optimize_palettes(tilepals)
        
        sorted_pals = []

        for pal in pals:
            sorted_pals.extend(sorted(pal, key=step, reverse=True))
            
        return sorted_pals
        

        # num_pals = 6
        # palettes = []

        # sorted_tiles = self.get_sortedlist_tiles()
        # gPalette = self.generate_global_palette()
        # gPalette_sort = self.sort_global_palette(gPalette)
        # palette = sorted_tiles[0].pal
        # print("First palette: ", palette)

        # set_tiles_indexados = {}

        # for color in gPalette_sort:
        #     if len(palette) == 15:
        #         break
        #     palette.add(color)

        # print("Palette: ",palette)
        # print("Indexed_tiles: ",len(self.check_tiles_per_palette(palette)))
        # return palette


    def optimize_palettes(self, tilepals, N=9, K=16):
        """
        Return an optimized palette set for the given tile set.
        tilepals -- A list of sets of unique colors used for each tile of the image
        N -- The maximum number of palettes for one image
        K -- The maximum number of colors for one tile palette
        """
        # Check that each tilepal fits within the color limit
        if any(len(s) > K for s in tilepals):
            print("A tile has more than %d unique colors" % K)
            return set()
        # Remove duplicate tilepals
        sets = []
        for s in tilepals:
            if s not in sets:
                sets.append(s)
        # Remove tilepals that are proper subsets of other tilepals
        sets = [s for s in sets if not any(c != s and s.issubset(c) for c in sets)]
        # Sort tilepals from most to fewest colors
        sets.sort(key=len, reverse=True)
        # Combine tilepals as long as they fit within the color limit
        opt = []
        for s in sets:
            for cs in opt:
                if len(s | cs) <= K:
                    cs.update(s)
                    break
            else:
                opt.append(s)
        # Sort tilepals from most to fewest colors
        opt.sort(key=len, reverse=True)
        # Check that the palettes fit within the palette limit
        if len(opt) > N:
            print("There are more than %d palettes" % N)
            return set()
        return opt

    def check_tiles_per_palette(self, palette, listOfTiles=None):
        if listOfTiles is None:
            listOfTiles = self.listOfTiles.values()
        tileIdList = []
        for tile in listOfTiles:
            if tile.pal.issubset(palette):
                tileIdList.append(tile.tileId)
        return tileIdList

    def generate_global_palette(self):
        gPalette = {}
        for color in map(lambda x : x[1],self.toProcessTileset.getcolors()):
            gPalette[color] = self.get_tiles_per_color(color)
        return gPalette
    
    def sort_global_palette(self,gPalette):
        return sorted(gPalette, key=gPalette.get, reverse=True)

    def get_tiles_per_color(self, color):
        counter = 0
        for tile in self.listOfTiles.values():
            if color in tile.pal:
                counter += 1
        return counter

    def reduce_duplicate_tiles(self, image, refactor, removeFlips):
        if refactor:
            # Get all tiles
            tiles = [Image.new("RGB", (8, 8), self.bgColor)]
            for y in range(image.size[1] // 8):
                for x in range(image.size[0] // 8):
                    tile = self.get_tile(image, x, y)
                    if tile not in tiles:
                        tiles.append(tile)
            tiles = np.array(tiles)
            width = 128
            # (tiles.shape[0]/16)*8
            height = tiles.shape[0] // 2
            if tiles.shape[0] % 16 > 0:
                height += 8

            reduced_tileset = Image.new("RGB", (width, height), self.bgColor)
            # Avoid to paste first void tile
            for i in range(1, tiles.shape[0]):
                pos = ((i % 16)*8, (i // 16)*8)
                reduced_tileset.paste(tiles[i], pos)

            return reduced_tileset
        else:
            return image

    # Reduct palettes by threshold
    def reduct_palettes(self, image, maxColors, method):
        img = image.copy()

        bgColorRGBA = (self.bgColor[0], self.bgColor[1], self.bgColor[2], 255)
        img = self.replace_color_in_image_alpha((0, 0, 0, 0), bgColorRGBA, img)

        pal = img.getcolors()

        if method < 2:
            while len(pal) > maxColors:
                sThreshold = 1
                i1, i2 = 0, 0

                for x in range(len(pal)):
                    for y in range(x+1, len(pal)):
                        if pal[x][1][3] == 255 and pal[y][1][3] == 255:
                            cThreshold = self.get_color_difference(pal[x][1], pal[y][1])
                            if cThreshold < sThreshold:
                                sThreshold = cThreshold
                                i1, i2 = x, y

                if method == 1:
                    #totalPixels = pal[i1][0] + pal[i2][0]
                    avgColor = (int((pal[i1][1][0] + pal[i2][1][0])/2), int((pal[i1][1][1] + pal[i2][1][1])/2), int((pal[i1][1][2] + pal[i2][1][2])/2), 255)
                    img = self.replace_color_in_image_alpha(avgColor, pal[i1][1], img)
                    img = self.replace_color_in_image_alpha(avgColor, pal[i2][1], img)
                    del pal[i2]
                    del pal[i1]
                    # Pixels amount are irrelevant in this method
                    pal.append((0, avgColor))
                else:
                    if pal[i1][0] > pal[i2][0]:
                        img = self.replace_color_in_image_alpha(pal[i1][1], pal[i2][1], img)
                        del pal[i2]
                    else:
                        img = self.replace_color_in_image_alpha(pal[i2][1], pal[i1][1], img)
                        del pal[i1]
            img = self.replace_color_in_image_alpha(bgColorRGBA, (0, 0, 0, 0), img)
        else:
            imgArr = quantize(np.array(img), maxColors)
            imgArr = np.uint8(imgArr)
            imgArr = self.replace_color_in_image_alpha(bgColorRGBA, (0, 0, 0, 0), imgArr)
            img = Image.fromarray(np.uint8(imgArr)).convert('RGB')
        return img

    def get_color_difference(self, color1, color2):
        rDiff = (float(color1[0] - color2[0]))/float(2)
        if rDiff < 0:
            rDiff = -1 * rDiff
        gDiff = (float(color1[1] - color2[1]))/float(2)
        if gDiff < 0:
            gDiff = -1 * gDiff
        bDiff = (float(color1[2] - color2[2]))/float(2)
        if bDiff < 0:
            bDiff = -1 * rDiff
        diff = ((rDiff + gDiff + bDiff)/float(3)/float(255))
        return diff

    def get_image_average_color_RGB(self, image):
        img = image.copy()

        mask = np.all(img[:,:,:3] != self.bgColor, axis=-1)

        return np.mean(img[mask], axis=0)/255.


    def get_bg_color(self, image):
        img = image.copy()
        if image.shape[2] == 4:
            img = img.reshape(-1, 4)
            allColors = img[img[:,3] == 255]
            avgColor = np.mean(allColors, axis=0)/255.
            avgColor = avgColor[:3]
            hsvColor = np.array(colorsys.rgb_to_hsv(*avgColor))

            hsvColor[0] = 1. - hsvColor[0]
            hsvColor[1] = 60./255.
            hsvColor[2] = 220./255.

            bgColor = (colorsys.hsv_to_rgb(*hsvColor))
            bgColor = tuple(((np.array(bgColor)*255).astype(np.uint8)))

            while np.all(img[:,:3] != bgColor) == False:
                hsvColor = np.array(colorsys.rgb_to_hsv(*bgColor))
                randFloat = random.rand()
                if randFloat < 0.2:
                    randFloat += 0.2
                hsvColor[1] = randFloat
                bgColor = (colorsys.hsv_to_rgb(*hsvColor))
                bgColor = tuple(((np.array(bgColor)*255).astype(np.uint8)))
            return bgColor
        else:
            return tuple(image[0][0])

    def get_color_value(self, color):
        return int(int(color[0]) + int(color[1]) + int(color[2]))

    # Converts RGBA to RBG
    def rgba_to_RBG_and_BG_color(self, img, color):
        if len(img.getcolors()[0][1]) > 3:
            image = Image.new("RGB",img.size, color)
            image.paste(img, mask=img.split()[3])
            image.convert('RGB')
            return image
        else:
            return img

    # Returns True if the first color is more abundant, else, returns false
    def replace_color_in_image(self, newColor, oldColor, image):
        data = np.array(image)

        r1, g1, b1 = oldColor
        r2, g2, b2 = newColor
        red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
        mask = (red == r1) & (green == g1) & (blue == b1)
        data[:,:,:3][mask] = [r2, g2, b2]

        return Image.fromarray(data)

    def replace_color_in_image_alpha(self, newColor, oldColor, image):
        data = np.array(image)

        r1, g1, b1, a1 = oldColor
        r2, g2, b2, a2 = newColor
        red, green, blue, alpha = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
        mask = (red == r1) & (green == g1) & (blue == b1) & (alpha == a1)
        data[:,:,:4][mask] = [r2, g2, b2, a2]

        return Image.fromarray(data)

    #Returns True if the first color is more abundant, else, returns false
    def get_more_abundant_color_between(self, color1, color2, image):
        color1Counter, color2Counter = 0, 0
        for x in range(image.width):
            for y in range(image.height):
                pixel = image.getpixel((x,y))
                if pixel[0] == color1[0] and pixel[1] == color1[1] and pixel[2] == color1[2]:
                    color1Counter = color1Counter + 1
                elif pixel[0] == color2[0] and pixel[1] == color2[1] and pixel[2] == color2[2]:
                    color2Counter = color2Counter + 1

        if color1Counter > color2Counter:
            return True
        return False

    def get_colors_amount(self, image):
        return len(image.getcolors())

    #Returns all palettes except bg color
    def get_all_palettes(self, image, bgColor):
        colors = np.empty((0,3), int)
        for x in range(image.width):
            for y in range(image.height):
                pixel = image.getpixel((x,y))
                if pixel != bgColor and self.color_already_added(pixel, colors) == False:
                    colors = np.append(colors, np.array([pixel]), axis=0)
        return colors

    def get_palette_set(self, image, bgColor):
        colors = set()
        colorsAmount = 0
        for x in range(image.width):
            for y in range(image.height):
                pixel = image.getpixel((x,y))
                if pixel != bgColor:
                    colors.add(pixel)
                    colorsAmount += 1
        return colors, colorsAmount

    #Returns if the color is already in a set of colors
    def color_already_added(self, color, setOfColors):
        for x in range(setOfColors.shape[0]):
            if color[0] == setOfColors[x][0] and color[1] == setOfColors[x][1] and color[2] == setOfColors[x][2]:
                return True
        return False

class Tile():
    def __init__(self, tileId, palette, colorsAmount):
        self.tileId = tileId
        self.pal = palette
        self.colAmount = colorsAmount

    def __str__(self):
        return "tileId: " + str(self.tileId) + "\ncolAmount: " + str(self.colAmount) + "\npal: " + str(self.pal)

class Palette():

    def __init__(self, palette):
        self.palette = palette
        self.COLORPICKER_FRAME_THICKNESS = 2
        self.raw_palette_img = create_image_from_palette(palette)
        self.void_palette_img = self.generate_void_palette_image()
        self.colorpick_frame = self.generate_colorpick_frame()
        self.color_picked = 0

    def get_paletteviewer_image(self):
        paletteviewer = self.void_palette_img.copy()
        paletteviewer.paste(self.raw_palette_img, (self.COLORPICKER_FRAME_THICKNESS, self.COLORPICKER_FRAME_THICKNESS), self.raw_palette_img)
        
        clrpicker_pos = ((self.color_picked % 16) * 8, (self.color_picked // 16) * 8)
        paletteviewer.paste(self.colorpick_frame, clrpicker_pos, self.colorpick_frame)
        
        return paletteviewer

        
    def generate_void_palette_image(self):
        baseTile = Image.new("RGB", (8, 8), (196, 196, 196))
        smallerBaseTile = Image.new("RGB", (4, 4), (224, 224, 224))
        baseTile.paste(smallerBaseTile, (0, 4))
        baseTile.paste(smallerBaseTile, (4, 0))
    
        void_temp_palette_image = Image.new("RGB", (128, 128), (255, 0, 0))
        void_palette_image = Image.new("RGBA", (128 + (self.COLORPICKER_FRAME_THICKNESS*2), 128 + (self.COLORPICKER_FRAME_THICKNESS*2)), (0, 0, 0, 0))


        void_temp_palette_image.paste(baseTile, (0, 0))

        for i in range(4):
            void_temp_palette_image.paste(void_temp_palette_image, ((2 ** i)*8, 0))

        for i in range(4):
            void_temp_palette_image.paste(void_temp_palette_image, (0, ((2 ** i)*8)))

        void_palette_image.paste(void_temp_palette_image, (self.COLORPICKER_FRAME_THICKNESS, self.COLORPICKER_FRAME_THICKNESS))

        return void_palette_image

    def generate_colorpick_frame(self):
        frame = Image.new("RGBA", (8+(2*self.COLORPICKER_FRAME_THICKNESS), 8+(2*self.COLORPICKER_FRAME_THICKNESS)), (0, 0, 0, 0))
        vertical_red_stick = Image.new("RGB", (self.COLORPICKER_FRAME_THICKNESS, 8 + self.COLORPICKER_FRAME_THICKNESS), (255, 32, 32))
        horizontal_red_stick = Image.new("RGB", (8 + self.COLORPICKER_FRAME_THICKNESS, self.COLORPICKER_FRAME_THICKNESS), (255, 32, 32))

        frame.paste(vertical_red_stick, (0, 0))
        frame.paste(horizontal_red_stick, (0, 8 + self.COLORPICKER_FRAME_THICKNESS))
        frame.paste(vertical_red_stick, (8 + self.COLORPICKER_FRAME_THICKNESS, self.COLORPICKER_FRAME_THICKNESS))
        frame.paste(horizontal_red_stick, (self.COLORPICKER_FRAME_THICKNESS, 0))

        return frame

class PaletteManagerWidget(QWidget):
    """
        Widget que contiene:
        - visor paletas
        - editor de color
        Es común a los tres editores
        Posible futuro: meter reducción de colores
    """
    def __init__(self, parent):
        super(PaletteManagerWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.clicked_color = 0

        # visor de paletas
        self.palettesGroupbox = QGroupBox("Palettes")
        self.palettesLayout = QVBoxLayout()
        self.palettesGroupbox.setLayout(self.palettesLayout)
        self.palettesGroupbox.setFixedSize(154, 169)
        self.layout.addWidget(self.palettesGroupbox)
        
        if True:
            self.palettesLabel = QLabel()
            self.palettesLabel.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.palettesLabel.mousePressEvent = self.set_clicked_color

        self.palettesLayout.addWidget(self.palettesLabel)
        self.palettesLayout.addStretch()

        # editor de colores
        self.editColorGroupbox = QGroupBox("Edit Color")
        self.editColorLayout = QVBoxLayout()
        self.selectedColorLayout = QHBoxLayout()
        self.sliderColorLayout = QVBoxLayout()
        self.editColorGroupbox.setFixedSize(154, 159)
        # self.editColorGroupbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.editColorGroupbox)
        self.editColorGroupbox.setLayout(self.editColorLayout)
        self.editColorLayout.addLayout(self.selectedColorLayout)
        self.selectedColorLayout.setContentsMargins(QMargins(0, 3, 0, 3))
        self.editColorLayout.addLayout(self.sliderColorLayout)
        self.editColorLayout.addStretch()

        self.selectedColorLabel = QLabel()
        self.selectedColorLabel.setFixedSize(32, 32)
        
        first_color = self.parent().sprite_pal.palette[0]
        bg_color = ("background-color:rgb(" + str(first_color[0]) + ", " + str(first_color[1]) + ", " + str(first_color[2]) + ");")
        bg_color = bg_color.replace(" ", "")
        self.selectedColorLabel.setStyleSheet(bg_color)  # -> color seleccionado (el que se está editando)

        self.selectedColorLayout.addWidget(self.selectedColorLabel)

        self.redColorLayout = QHBoxLayout()
        self.redColorLayout.setContentsMargins(QMargins(0, 3, 0, 3))
        self.greenColorLayout = QHBoxLayout()
        self.greenColorLayout.setContentsMargins(QMargins(0, 3, 0, 3))
        self.blueColorLayout = QHBoxLayout()
        self.blueColorLayout.setContentsMargins(QMargins(0, 3, 0, 3))

        # Red Slider
        self.redSlider = QSlider(Qt.Horizontal, self)
        self.redSlider.setRange(0, 255)
        self.redSlider.setFixedSize(96, 16)
        self.redSlider.setStyleSheet(self.generate_custom_slider(first_color, 0))
        self.redSlider.setValue(first_color[0])

        self.redSpinBox = QSpinBox()
        self.redSpinBox.setRange(0, 255)
        self.redSpinBox.setFixedSize(40, 16)
        self.redSpinBox.setValue(first_color[0])

        self.redColorLayout.addWidget(self.redSlider)
        self.redColorLayout.addWidget(self.redSpinBox)

        self.sliderColorLayout.addLayout(self.redColorLayout)

        # Green Slider
        self.greenSlider = QSlider(Qt.Horizontal)
        self.greenSlider.setRange(0, 255)
        self.greenSlider.setFixedSize(96, 16)
        self.greenSlider.setStyleSheet(self.generate_custom_slider(first_color, 1))
        self.greenSlider.setValue(first_color[1])

        self.greenSpinBox = QSpinBox()
        self.greenSpinBox.setRange(0, 255)
        self.greenSpinBox.setFixedSize(40, 16)
        self.greenSpinBox.setValue(first_color[1])

        self.greenColorLayout.addWidget(self.greenSlider)
        self.greenColorLayout.addWidget(self.greenSpinBox)

        self.sliderColorLayout.addLayout(self.greenColorLayout)

        # Blue Slider
        self.blueSlider = QSlider(Qt.Horizontal, self)
        self.blueSlider.setRange(0, 255)
        self.blueSlider.setFixedSize(96, 16)
        self.blueSlider.setStyleSheet(self.generate_custom_slider(first_color, 2))
        self.blueSlider.setValue(first_color[2])

        self.blueSpinBox = QSpinBox()
        self.blueSpinBox.setRange(0, 255)
        self.blueSpinBox.setFixedSize(40, 16)
        self.blueSpinBox.setValue(first_color[2])

        self.blueColorLayout.addWidget(self.blueSlider)
        self.blueColorLayout.addWidget(self.blueSpinBox)
        
        self.sliderColorLayout.addLayout(self.blueColorLayout)

        
    def set_clicked_color(self, event):
        main_window = self.parent().parent()
        frame_thickness = main_window.sprite_pal.COLORPICKER_FRAME_THICKNESS
        x, y = event.pos().x() - frame_thickness, event.pos().y() - frame_thickness

        if x >= 0 and y >= 0:
            print(x," // 8 = ", x // 8 ,"; (", y, " // 8) * 16 = ", (y // 8) * 16)
            clicked_color = x // 8 + ((y // 8) * 16)
            if clicked_color < main_window.sprite_pal.palette.shape[0] and clicked_color < 256:
                main_window.sprite_pal.color_picked = clicked_color
                main_window.sprite_pal_manager.palettesLabel.setPixmap(pil2pixmap(main_window.sprite_pal.get_paletteviewer_image()))

    def generate_custom_slider(self, color, rgb_index):

        custom_slider_css = """
                    .QSlider::groove:horizontal {
                        border: 0px solid #262626;
                        height: 12px;""" + self.generate_gradient(color, rgb_index) + """margin: 0 6px;
                    }

                    .QSlider::handle:horizontal {
                        width: 0;
                        height: 0;
                        border-style: solid;
                        border-width: 4;
                        border-color: #007bff;
                        margin: -2px -4px;

                    }"""

        return custom_slider_css

    def generate_gradient(self, color, rgb_index):
        if rgb_index == 1:
            low_color = (color[0], 0, color[2])
            high_color = (color[0], 255, color[2])
        elif rgb_index == 2:
            low_color = (color[0], color[1], 0)
            high_color = (color[0], color[1], 255)
        else:
            low_color = (0, color[1], color[2])
            high_color = (255, color[1], color[2])
            
        linear_gradient = "background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 rgb" + str(low_color).replace(" ", "") + ", stop: 1 rgb" + str(high_color).replace(" ", "") + ");"
        return linear_gradient

def create_image_from_palette(palette):
    image = Image.new("RGBA", (128, (((palette.shape[0] - 1) // 16) + 1)*8), (0, 0, 0, 0))
    for i in range(palette.shape[0]):
        aux = Image.new("RGB", (8, 8), tuple(palette[i]))
        pos = ((i % 16)*8, (i // 16)*8)
        image.paste(aux, pos)
        if i >= 255:
            break
    return image

def color_sort_criteria(color):
    hsvColor = colorsys.rgb_to_hsv(*np.array(color)/255.)
    return hsvColor

def step (color, repetitions=8):
    r, g, b = color
    lum = math.sqrt( .241 * r + .691 * g + .068 * b )
    h, s, v = colorsys.rgb_to_hsv(r,g,b)
    h2 = int(h * repetitions)
    lum2 = int(lum * repetitions)
    v2 = int(v * repetitions)
    if h2 % 2 == 1:
        v2 = repetitions - v2
        lum = repetitions - lum
    return (h2, lum, v2)

def quantize(raster, n_colors):
    width, height, depth = raster.shape
    reshaped_raster = np.reshape(raster, (width * height, depth))

    model = cluster.KMeans(n_clusters=n_colors)
    labels = model.fit_predict(reshaped_raster)
    palette = model.cluster_centers_

    quantized_raster = np.reshape(palette[labels], (width, height, palette.shape[1]))

    return quantized_raster

def pil2pixmap(im):

    if im.mode == "RGB":
        r, g, b = im.split()
        im = Image.merge("RGB", (b, g, r))
    elif  im.mode == "RGBA":
        r, g, b, a = im.split()
        im = Image.merge("RGBA", (b, g, r, a))
    elif im.mode == "L":
        im = im.convert("RGBA")
    im2 = im.convert("RGBA")
    data = im2.tobytes("raw", "RGBA")
    qim = QImage(data, im.size[0], im.size[1], QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(qim)
    return pixmap

def pixmap2pil(im):
    img = im.toImage()
    buff = QBuffer()
    buff.open(QBuffer.ReadWrite)
    img.save(buff, "PNG")
    pil_img = Image.open(io.BytesIO(buff.data()))
    buff.close()
    return pil_img


app = QApplication(sys.argv)
screen = TilemonStudioWindow()
screen.show()
sys.exit(app.exec_())
