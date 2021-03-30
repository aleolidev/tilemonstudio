import numpy as np
import PIL as pil
from backend.color_utilities import create_image_from_palette


class Palette:
    COLORPICKER_FRAME_THICKNESS = 2  # TODO: parametrizar?
    def __init__(self, palette: np.ndarray):
        self.palette: np.ndarray = palette
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
        base_tile = pil.Image.new("RGB", (8, 8), (196, 196, 196))  # TODO: parametrizar
        smaller_base_tile = pil.Image.new("RGB", (4, 4), (224, 224, 224))  # TODO: parametrizar
        base_tile.paste(smaller_base_tile, (0, 4))
        base_tile.paste(smaller_base_tile, (4, 0))
        void_temp_palette_image = pil.Image.new("RGB", (128, 128), (255, 0, 0))
        void_palette_image = pil.Image.new(
            "RGBA", 
            (128 + (self.COLORPICKER_FRAME_THICKNESS * 2),
             128 + (self.COLORPICKER_FRAME_THICKNESS * 2),
            ),
            (0, 0, 0, 0)
        )
        void_temp_palette_image.paste(base_tile, (0, 0))
        for i in range(4):  # TODO: testear si pueden estar en el mismo loop!
            void_temp_palette_image.paste(void_temp_palette_image, ((2**i) * 8, 0))
            void_temp_palette_image.paste(void_temp_palette_image, (0, ((2**i) * 8)))
        void_palette_image.paste(
            void_temp_palette_image,
            (self.COLORPICKER_FRAME_THICKNESS, self.COLORPICKER_FRAME_THICKNESS))
        return void_palette_image
    
    def generate_colorpick_frame(self):
        frame = pil.Image.new(
            "RGBA", 
            (8 + (2 * self.COLORPICKER_FRAME_THICKNESS), 
             8 + (2 * self.COLORPICKER_FRAME_THICKNESS)), 
            (0, 0, 0, 0))
        vertical_red_stick = pil.Image.new(
            "RGB", 
            (self.COLORPICKER_FRAME_THICKNESS, 
             8 + self.COLORPICKER_FRAME_THICKNESS), 
            (255, 32, 32))
        horizontal_red_stick = pil.Image.new(
            "RGB", 
            (8 + self.COLORPICKER_FRAME_THICKNESS, 
             self.COLORPICKER_FRAME_THICKNESS), 
            (255, 32, 32))
        frame.paste(vertical_red_stick, (0, 0))
        frame.paste(horizontal_red_stick, (0, 8 + self.COLORPICKER_FRAME_THICKNESS))
        frame.paste(
            vertical_red_stick, 
            (8 + self.COLORPICKER_FRAME_THICKNESS, 
             self.COLORPICKER_FRAME_THICKNESS))
        frame.paste(horizontal_red_stick, (self.COLORPICKER_FRAME_THICKNESS, 0))
        return frame        





