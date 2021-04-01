# import PIL as pil
import numpy as np
import colorsys
import io
import math
from sklearn import cluster
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QBuffer
from PIL import Image as pim


def create_image_from_palette(palette):
    image = pim.new(
        "RGBA",
        (128, (((palette.shape[0] - 1) // 16) + 1) * 8),
        (0, 0, 0, 0)
    )
    for i in range(palette.shape[0]):
        aux = pim.new("RGB", (8, 8), tuple(palette[i]))
        pos = ((i % 16) * 8, (i // 16) * 8)
        image.paste(aux, pos)
        if i >= 255:
            break
    return image


def get_color_value(color):
    return int(int(color[0]) + int(color[1]) + int(color[2]))

def color_sort_criteria(color):
    hasv_color = colorsys.rgb_to_hsv(*np.array(color) / 255.)
    return hasv_color

def replace_color_in_image(new_color, old_color, image):
    data = np.array(image)
    r1, g1, b1 = old_color
    r2, g2, b2 = new_color
    red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]
    mask = (red == r1) & (green == g1) & (blue == b1)
    data[:, :, :3][mask] = [r2, g2, b2]
    return pim.fromarray(data)

def step(color, repetitions=8):
    r, g, b = color
    lum = math.sqrt(0.241 * r + 0.691 * g + 0.068 * b)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    hue2 = int(h * repetitions)
    lum2 = int(lum * repetitions)  # FIXME: por qué existo?
    vue2 = int(v * repetitions)
    if hue2 % 2 == 1:
        vue2 = repetitions - vue2
        lum = repetitions - lum  # FIXME: no debería ser lum2?
    return hue2, lum, vue2


def quantize(raster, n_colors):
    width, height, depth = raster.shape
    reshaped_raster = np.reshape(raster, (width * height, depth))
    model = cluster.KMeans(n_clusters=n_colors)
    labels = model.fit_predict(reshaped_raster)
    palette = model.cluster_centers_
    quantized_raster = np.reshape(palette[labels], (width, height, palette.shape[1]))
    return quantized_raster


def pil_to_pixmap(im):
    if im.mode == "RGB":
        r, g, b = im.split()
        im = pim.merge("RGB", (b, g, r))
    elif im.mode == "RGBA":
        r, g, b, a = im.split()
        im = pim.merge("RGBA", (b, g, r, a))
    elif im.mode == "L":
        im = im.convert("RGBA")
    im2 = im.convert("RGBA")
    data = im2.tobytes("raw", "RGBA")
    qim = QImage(data, im.size[0], im.size[1], QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(qim)
    return pixmap


def pixmap_to_pil(im):
    img = im.toImage()
    buff = QBuffer()
    buff.open(QBuffer.ReadWrite)
    im.save(buff, "PNG")
    pil_img = pim.open(io.BytesIO(buff.data()))
    buff.close()
    return pil_img

def round_to_multiple_of(x, multiple):
    return multiple * round(x/multiple)