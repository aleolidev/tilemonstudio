from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QSpacerItem
from PyQt5.QtWidgets import QLabel, QSlider, QPushButton, QGroupBox, QSpinBox, QSizePolicy
from PyQt5.QtGui import QColor, QIcon, QPixmap, QCursor
from PyQt5.QtCore import QMargins, QSignalBlocker, pyqtSignal
from backend.color_utilities import create_image_from_palette, replace_color_in_image
from backend.image import pil_to_pixmap
from backend.image import Image as cim
from backend.palette import Palette
from PyQt5.QtCore import Qt

class PaletteWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_gui()
        self.connect_signals()
    
    def load_gui(self):
        
        self.palettes_label = QLabel("")
        self.palettes_label.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.palettes_group_layout = QVBoxLayout()
        self.palettes_group_layout.addWidget(self.palettes_label, alignment=Qt.AlignCenter)
        self.palette_groupbox = QGroupBox("Palettes")  # TODO: archivo de traducción!
        self.palette_groupbox.setLayout(self.palettes_group_layout)
        self.palette_groupbox.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        
        # TODO: Set Color after create PaletteWidget, and after change selected index
        self.edit_color_selected_label = QLabel("")
        self.edit_color_selected_label.setFixedSize(32, 32)

        self.edit_color_red_layout = QVBoxLayout()
        self.edit_color_red_layout.setContentsMargins(QMargins(0, 3, 0, 3))
        self.edit_color_green_layout = QVBoxLayout()
        self.edit_color_green_layout.setContentsMargins(QMargins(0, 3, 0, 3))
        self.edit_color_blue_layout = QVBoxLayout()
        self.edit_color_blue_layout.setContentsMargins(QMargins(0, 3, 0, 3))

        self.edit_color_group_layout = QVBoxLayout()
        self.edit_color_label_layout = QHBoxLayout()
        self.edit_color_scrolls_layout = QHBoxLayout()

        # Red Slider
        self.red_slider = QSlider(Qt.Vertical, self)
        self.red_slider.setRange(0, 255)
        self.red_slider.setFixedSize(24, 96)
        self.red_slider.setStyleSheet(self.generate_custom_slider(0))

        self.red_spin_box = QSpinBox()
        self.red_spin_box.setRange(0, 255)
        self.red_spin_box.setFixedSize(40, 16)

        self.edit_color_red_layout.addWidget(self.red_slider, alignment= Qt.AlignCenter)
        self.edit_color_red_layout.addWidget(self.red_spin_box, alignment= Qt.AlignCenter)

        # Green Slider
        self.green_slider = QSlider(Qt.Vertical)
        self.green_slider.setRange(0, 255)
        self.green_slider.setFixedSize(24, 96)
        self.green_slider.setStyleSheet(self.generate_custom_slider(1))

        self.green_spin_box = QSpinBox()
        self.green_spin_box.setRange(0, 255)
        self.green_spin_box.setFixedSize(40, 16)

        self.edit_color_green_layout.addWidget(self.green_slider, alignment= Qt.AlignCenter)
        self.edit_color_green_layout.addWidget(self.green_spin_box, alignment= Qt.AlignCenter)

        # Blue Slider
        self.blue_slider = QSlider(Qt.Vertical, self)
        self.blue_slider.setRange(0, 255)
        self.blue_slider.setFixedSize(24, 96)
        self.blue_slider.setStyleSheet(self.generate_custom_slider(2))

        self.blue_spin_box = QSpinBox()
        self.blue_spin_box.setRange(0, 255)
        self.blue_spin_box.setFixedSize(40, 16)

        self.edit_color_blue_layout.addWidget(self.blue_slider, alignment= Qt.AlignCenter)
        self.edit_color_blue_layout.addWidget(self.blue_spin_box, alignment= Qt.AlignCenter)

        self.edit_color_label_layout.addWidget(self.edit_color_selected_label)

        self.edit_color_scrolls_layout.addLayout(self.edit_color_red_layout)
        self.edit_color_scrolls_layout.addLayout(self.edit_color_green_layout)
        self.edit_color_scrolls_layout.addLayout(self.edit_color_blue_layout)

        self.edit_color_group_layout.addLayout(self.edit_color_label_layout)
        self.edit_color_group_layout.addLayout(self.edit_color_scrolls_layout)
        self.edit_color_groupbox = QGroupBox("Edit color")  # TODO: archivo de traducción!
        self.edit_color_groupbox.setLayout(self.edit_color_group_layout)

        self.lay = QVBoxLayout()
        self.lay.addWidget(self.palette_groupbox)
        self.lay.addWidget(self.edit_color_groupbox)
        self.setLayout(self.lay)
    
    def set_clicked_color(self, event, pal_object):
        frame_thickness = pal_object.COLORPICKER_FRAME_THICKNESS
        x, y = event.pos().x() - frame_thickness, event.pos().y() - frame_thickness

        if x >= 0 and y >= 0:
            # print(x," // 8 = ", x // 8 ,"; (", y, " // 8) * 16 = ", (y // 8) * 16)
            clicked_color = x // 8 + ((y // 8) * 16)
            if clicked_color < pal_object.palette.shape[0] and clicked_color < 256:
                pal_object.color_picked = clicked_color
                self.palettes_label.setPixmap(pil_to_pixmap(pal_object.get_paletteviewer_image()))
                self.set_color_data(pal_object.palette[pal_object.color_picked])

    def set_color_data(self, color):
        self.set_label_color(color)

        self.block_slider_spin_signals(True)

        self.red_slider.setValue(color[0])
        self.red_spin_box.setValue(color[0])

        self.green_slider.setValue(color[1])
        self.green_spin_box.setValue(color[1])

        self.blue_slider.setValue(color[2])
        self.blue_spin_box.setValue(color[2])

        self.block_slider_spin_signals(False)

    def set_label_color(self, color):
        bg_color = ("background-color:rgb(" + str(color[0]) + ", " + str(color[1]) + ", " + str(color[2]) + ");")
        bg_color = bg_color.replace(" ", "")
        self.edit_color_selected_label.setStyleSheet(bg_color)

    def generate_custom_slider(self, rgb_index):

        custom_slider_css = """
                    .QSlider::groove:vertical {
                        border: 0px solid #262626;
                        width: 16px;""" + self.generate_gradient(rgb_index) + """margin: 8px 0;
                    }
                    .QSlider::handle:vertical {
                        width: 0;
                        height: 0;
                        border-style: solid;
                        border-width: 4;
                        border-color: #007bff;
                        margin: -4px -2px;
                    }"""

        return custom_slider_css

    def generate_gradient(self, rgb_index):
        black = (0, 0, 0)
        if rgb_index == 1:
            high_color = (0, 255, 0)
        elif rgb_index == 2:
            high_color = (0, 0, 255)
        else:
            high_color = (255, 0, 0)

        linear_gradient = "background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb" + str(high_color).replace(" ", "") + ", stop: 1 rgb" + str(black).replace(" ", "") + ");"
        return linear_gradient

    def slider_changed(self, palette, image, update_scaled_img):
        self.block_slider_spin_signals(True)
        self.red_spin_box.setValue(self.red_slider.value())
        self.green_spin_box.setValue(self.green_slider.value())
        self.blue_spin_box.setValue(self.blue_slider.value())

        self.edit_color(palette, image, update_scaled_img)
        self.block_slider_spin_signals(False)

    def spin_box_changed(self, palette, image, update_scaled_img):
        self.block_slider_spin_signals(True)

        self.red_slider.setValue(self.red_spin_box.value())
        self.green_slider.setValue(self.green_spin_box.value())
        self.blue_slider.setValue(self.blue_spin_box.value())
        
        self.edit_color(palette, image, update_scaled_img)
        self.block_slider_spin_signals(False)

    def edit_color(self, palette, image, update_scaled_img):
        ### Recalculate and set: color label, palette data and image, sprite image
        # Color label
        color = (self.red_slider.value(), self.green_slider.value(), self.blue_slider.value())
        old_color = tuple(palette.palette[palette.color_picked])
        self.set_label_color(color)

        # Palette Data and Image
        palette.palette[palette.color_picked] = color
        palette.raw_palette_img = create_image_from_palette(palette.palette)
        self.palettes_label.setPixmap(pil_to_pixmap(palette.get_paletteviewer_image()))

        # Sprite Image
        # image.rgb_image = replace_color_in_image((0, 0, 255), (0, 255, 0), image.rgb_image)
        # image.rgb_image = replace_color_in_image((0, 255, 0), (255, 0, 0), image.rgb_image)
        # image.rgb_image = replace_color_in_image((255, 0, 0), (0, 0, 0), image.rgb_image)
        image.rgb_image = replace_color_in_image(color, old_color, image.rgb_image)
        update_scaled_img()

    def block_slider_spin_signals(self, status):
        """ 
        Avoids the recall of functions which programatically
        sets the values of sliders and spin boxes
        """
        self.red_slider.blockSignals(status)
        self.green_slider.blockSignals(status)
        self.blue_slider.blockSignals(status)
        self.red_spin_box.blockSignals(status)
        self.green_spin_box.blockSignals(status)
        self.blue_spin_box.blockSignals(status)

    def connect_signals(self):
        pass


