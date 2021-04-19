from dataclasses import dataclass
from backend.palette import Palette
from backend.color_utilities import step, round_to_multiple_of, quantize
from backend.color_utilities import pixmap_to_pil, pil_to_pixmap
from PyQt5.QtGui import QPixmap
from PIL import Image as pim
import numpy as np
import colorsys

@dataclass
class Tile:
    tile_id: int
    palette: Palette
    col_amount: int
    

class Image:
    TO_ROUND_VALUE = 8
    def __init__(self, raw_pixmap: QPixmap):
        self.raw_pixmap = raw_pixmap
        self.bg_color = self.get_bg_color(pixmap_to_pil(raw_pixmap))
        self.rgb_image = self.rgba_to_rgb_and_background_color(pixmap_to_pil(raw_pixmap), self.bg_color)
        self.tiles = {}
        # self.slice_image()
    
    def get_tile(self, image, x, y):
        tile = image.crop((x * 8, y * 8, (x + 1) * 8, (y + 1) * 8))
        return tile
    
    def generate_tile(self, image, x, y):
        tile_img = self.get_tile(image, x, y)
        tile_id = y * (image.size[0] // 8) + x
        tile_pal, colors_amount = self.get_palette_set(tile_img, self.bg_color)
        tile = Tile(tile_id, tile_pal, colors_amount)
        return tile
    
    def generate_palettes(self,N=9):
        self.slice_image()
        tile_pals = list(map(lambda x: x.palette, self.tiles.values()))
        pals = self.optimize_palettes(tile_pals,N)

        sorted_pals = []

        for pal in pals:
            n = 15 - len(pal) 
            sorted_pals.append(self.bg_color)
            sorted_pals.extend(sorted(pal, key=step, reverse=True))
            sorted_pals.extend([self.bg_color]*n)
        return sorted_pals

    def sort_palette_by_colors(self, palette, iters):
        pal = palette.copy()
        pal.sort(key=lambda color: step(color,iters))
        return pal
    
    def slice_image(self):
        self.tiles = {}
        image = self.rgb_image
        void_tile = pim.new("RGB", (8, 8), self.bg_color)
        for y in range(image.size[1] // 8):
            for x in range(image.size[0] // 8):
                tile = self.generate_tile(image, x, y)
                if self.get_tile(image, x, y) != void_tile:
                    self.tiles[tile.tile_id] = tile
    
    def get_sortedlist_tiles(self):
        return sorted(self.tiles.values(), key=lambda x: x.col_amount)
    
    def optimize_palettes(self, tilepals, N=9, K=15):
        """
        Return an optimized palette set for the given tile set.
        tilepals -- A list of sets of unique colors used for each tile of the image
        N -- The maximum number of palettes for one image
        K -- The maximum number of colors for one tile palette
        """
        num_pals = len(tilepals) #TODO
        num_colors = len(self.rgb_image.getcolors())
        img = self.rgb_image#.copy()
        while num_pals > N:
            print(num_colors)
            img_array = quantize(np.array(img),num_colors)
            img = pim.fromarray(np.uint8(img_array)).convert('RGB')
            self.rgb_image = img
            self.slice_image()
            tilepals = list(map(lambda x: x.palette, self.tiles.values()))
            num_pals = len(tilepals)
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
            opt = self.combine_tilepals(sets,K)
            # Sort tilepals from most to fewest colors
            opt.sort(key=len, reverse=True)
            # Check that the palettes fit within the palette limit
            num_pals = len(opt)
            num_colors -= 5

        if len(opt) > N:
            print("There are more than %d palettes" % N)
            return set()
        return opt

    def get_distances(self,train,test_row):
        distances = list()
        for train_row in train:
            dist = len(self.compare_tilepals(test_row, train_row))* 1./len(train_row)
            if len(set().union(train_row,test_row)) > 15:
                dist = 0
            distances.append((train_row, dist))
        distances.sort(key=lambda tup: tup[1],reverse=True)
        return distances
    
    # Locate the most similar neighbors
    def get_neighbors(self,train, test_row):       
        # neighbors = list()
        distances = self.get_distances(train,test_row)
        pal = test_row
        i = 0
        # print(distances)
        while train:
        # for i in range(num_neighbors):
            if i < len(distances):
                if len(set().union(pal,distances[i][0])) <= 15:
                    pal.update(distances[i][0])
            else:
                break
            i += 1
        return pal
    
    def compare_tilepals(self,tilepal1,tilepal2):
        return tilepal1.intersection(tilepal2)

    def combine_tilepals(self,tilepals, n_colors):
        # self.classify_tilepals(tilepals)
        opt = []
        print("Num_tilepals : ", len(tilepals))
        # v = map(self.get_num_tiles_per_palette,tilepals)
        # print(list(v))
        # print(self.check_tiles_per_palette(tilepals[-1]))
        ref_tilepals = tilepals.copy()

        while ref_tilepals:
            s = ref_tilepals.pop(0)

            cs = self.get_neighbors(ref_tilepals,s)

            subset = True

            for pal in opt:
                if cs.issubset(pal):
                    subset = False
                    break
            if subset:
                opt.append(cs)

            sets = []
            for s in ref_tilepals:
                if s not in opt:
                    sets.append(s)
            # Remove tilepals that are proper subsets of other tilepals
            sets = [s for s in sets if not any(c != s and s.issubset(c) for c in opt)]
            ref_tilepals = sets
                # print("despues :",len(ref_tilepals))
        print(len(opt))
        print(list(map(len,opt)))
        return opt
    
    def check_tiles_per_palette(self, palette, list_of_tiles=None):
        if list_of_tiles is None:
            list_of_tiles = self.tiles.values()
        tile_id_list = [tile.tile_id for tile in list_of_tiles if tile.pal.issubset(palette)]
        return tile_id_list
    
    def generate_global_palette(self):
        g_palette = {color: self.get_tiles_per_color(color) for color in map(lambda x: x[1], self.rgb_image.getcolors())}
        return g_palette
    
    def sort_global_palette(self, g_palette):
        return sorted(g_palette, key=g_palette.get, reverse=True)
    
    def get_tiles_per_color(self, color):
        counter = 0
        for tile in self.tiles.values():
            if color in tile.pal:
                counter += 1
        return counter
    
    def reduce_duplicate_tiles(self, image, refactor, remove_flips):
        if refactor:
            tiles = [pim.new("RGB", (8, 8), self.bg_color)]
            for y in range(image.size[1] // 8):
                for x in range(image.size[0] // 8):
                    tile = self.get_tile(image, x, y)
                    if tile not in tiles:
                        tiles.append(tile)
            tiles = np.array(tiles)
            width = 128
            height = tiles.shape[0] // 2
            if tiles.shape[0] % 16 > 0:
                height += 8
            reduced_image = pim.new("RGB", (width, height), self.bg_color)
            for i in range(1, tiles.shape[0]):
                pos = ((i % 16) * 8, (i // 16) * 8)
                reduced_image.paste(tiles[i], pos)
            return reduced_image
        else:
            return image
    
    # Reduct palettes by threshold
    def reduct_palettes(self, max_colors):
        img = self.rgba_to_rgb_and_background_color(pixmap_to_pil(self.raw_pixmap), self.bg_color)
        bg_color_rgba = (
            self.bg_color[0],
            self.bg_color[1],
            self.bg_color[2],
            255
        )
        img = self.replace_color_in_image_alpha((0, 0, 0, 0), bg_color_rgba, img)
        img_arr = quantize(np.array(img), max_colors)
        img_arr = np.uint8(img_arr)
        img_arr = self.replace_color_in_image_alpha(bg_color_rgba, (0, 0, 0, 0), img_arr)
        img = pim.fromarray(np.uint8(img_arr)).convert('RGB')
        return img

    def palette_to_4bpp_format(self, image):
        bg_color_set = False
        img = image.copy()
        pal = np.array(img.getcolors(maxcolors=65536), dtype="object")[:,1]

        for col in pal:
            r_4bpp = round_to_multiple_of(col[0], self.TO_ROUND_VALUE)
            g_4bpp = round_to_multiple_of(col[1], self.TO_ROUND_VALUE)
            b_4bpp = round_to_multiple_of(col[2], self.TO_ROUND_VALUE)
            if r_4bpp > 248:
                r_4bpp = 248
            if g_4bpp > 248:
                g_4bpp = 248
            if b_4bpp > 248:
                b_4bpp = 248
            col_4bpp = (r_4bpp, g_4bpp, b_4bpp)
            if self.bg_color == col:
                bg_color_set = True
                self.bg_color = col_4bpp
            img = self.replace_color_in_image(col_4bpp, col, img)
        
        # Index bg_color if not indexed
        if not bg_color_set:
            r_4bpp = round_to_multiple_of(self.bg_color[0], self.TO_ROUND_VALUE)
            g_4bpp = round_to_multiple_of(self.bg_color[1], self.TO_ROUND_VALUE)
            b_4bpp = round_to_multiple_of(self.bg_color[2], self.TO_ROUND_VALUE)
            if r_4bpp > 248:
                r_4bpp = 248
            if g_4bpp > 248:
                g_4bpp = 248
            if b_4bpp > 248:
                b_4bpp = 248
            col_4bpp = (r_4bpp, g_4bpp, b_4bpp)
            self.bg_color = col_4bpp
        
        return img
    
    def get_color_difference(self, color1, color2):
        r_diff = abs(float(color1[0] - color2[0]) / 2.0)
        g_diff = abs(float(color1[2] - color2[2]) / 2.0)
        b_diff = abs(float(color1[2] - color2[2]) / 2.0)
        diff = sum(r_diff, g_diff, b_diff) / 3.0 / 255.0
        return diff
    
    def get_image_average_color_rgb(self, image):
        img = image.copy()
        mask = np.all(img[:, :, :3] != self.bg_color, axis=-1)
        return np.mean(img[mask], axis=0) / 255.0
    

    """
    In case it's loaded a RBGA image, it finds the most common
    color between a range of luminosity and saturation, and finds
    the "furthest" color of the found one based on the hue.
    Then, generates new randoms values for saturation and luminosity
    between a range to secure it looks pleasant until it is not
    contained in the image.

    If a RGB is loaded, will return the most common color.
    """
    def get_bg_color(self, image):
        img = np.array(image)
        if img.shape[2] == 4:
            img = pim.fromarray(img.astype(np.uint8))
            pal = np.array(img.getcolors())
            
            """ 
            Sort palette from less used colors to more used colors
            and set format to RGB colors
            """ 
            pal_sorted_by_most_common = pal[pal[:,0].argsort()]
            pal_sorted_by_most_common = np.array(pal_sorted_by_most_common[:,-1])
            pal_sorted_by_most_common = np.array([np.array(row) for row in pal_sorted_by_most_common])
            pal_sorted_by_most_common = pal_sorted_by_most_common[pal_sorted_by_most_common[:, 3] == 255]
            pal_sorted_by_most_common = np.delete(pal_sorted_by_most_common, 3, 1)

            most_common_index = len(pal_sorted_by_most_common) - 1
            most_common_color = pal_sorted_by_most_common[most_common_index]
            hsv_color = np.array(colorsys.rgb_to_hsv(*((np.array(most_common_color) / 255.0)[:3])))
            while(most_common_index >= 0 and (hsv_color[2] < 40/255 or hsv_color[2] > 200/255 or hsv_color[1] < 40/255)):
                most_common_index -= 1
                most_common_color = pal_sorted_by_most_common[most_common_index]
                hsv_color = np.array(colorsys.rgb_to_hsv(*((np.array(most_common_color) / 255.0)[:3])))
            if (most_common_index >= 0):
                hue = hsv_color[0] + 0.5
                if hue >= 1:
                    hue -= 1
                # Always the same result
                np.random.seed(0)
                hsv_color[0] = hue
                hsv_color[1] = 120/240 + (np.random.random() * (40/240))
                hsv_color[2] = 180/240 + (np.random.random() * (40/240))
                bg_color = colorsys.hsv_to_rgb(*hsv_color)
                bg_color = tuple((np.array(bg_color) * 255).astype(np.uint8))
                while np.all(pal_sorted_by_most_common[:, :3] != bg_color) == False:
                    hsv_color[1] = 120/240 + (np.random.random() * (40/240))
                    hsv_color[2] = 180/240 + (np.random.random() * (40/240))
                    bg_color = colorsys.hsv_to_rgb(*hsv_color)
                    bg_color = tuple((np.array(bg_color) * 255).astype(np.uint8))
                return bg_color
            else:
                return tuple((np.array([64, 188, 188])).astype(np.uint8))
        else:
            img = pim.fromarray(img.astype(np.uint8))
            pal = np.array(img.getcolors())
            
            # Sort palette from less used colors to more used colors 
            pal_sorted_by_most_common = pal[pal[:,0].argsort()]
            bg_color = pal_sorted_by_most_common[len(pal_sorted_by_most_common) - 1][1]
            return bg_color

    
    def rgba_to_rgb_and_background_color(self, img, color):
        if len(img.getcolors()[0][1]) > 3:
            image = pim.new("RGB", img.size, color)
            image.paste(img, mask=img.split()[3])
            image.convert("RGB")
            return image
        else:
            return img

    def replace_color_in_image(self, new_color, old_color, image):
        data = np.array(image)

        r1, g1, b1 = old_color
        r2, g2, b2 = new_color
        red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]
        mask = (red == r1) & (green == g1) & (blue == b1)
        data[:, :, :3][mask] = [r2, g2, b2]

        return pim.fromarray(np.uint8(data))
    
    def replace_color_in_image_alpha(self, new_color, old_color, image):
        data = np.array(image)

        r1, g1, b1, a1 = old_color
        r2, g2, b2, a2 = new_color
        if data.shape[2] == 3:
            alpha = np.full((data.shape[0], data.shape[1], 1), 255)
            data = np.append(data, alpha, axis=2)
        red, green, blue, alpha = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
        mask = (red == r1) & (green == g1) & (blue == b1) & (alpha == a1)
        data[:, :, :4][mask] = [r2, g2, b2, a2]

        return pim.fromarray(np.uint8(data))
    
    def get_more_abundant_color_between(self, color1, color2, image):
        color_1_counter, color_2_counter = 0, 0
        for y in range(image.height):
            for x in range(image.width):
                pixel = image.getpixel((x, y))
                if pixel[0] == color1[0] and pixel[1] == color1[1] and pixel[2] == color1[2]:
                    color_1_counter += 1
                elif pixel[0] == color2[0] and pixel[1] == color2[1] and pixel[2] == color2[2]:
                    color_2_counter += 1
        return color_1_counter > color_2_counter
    
    def get_colors_amount(self, image):
        return len(image.getcolors())
    
    def get_all_palettes(self, image, bg_color):
        colors = np.empty((0, 3), int)
        for y in range(image.height):
            for x in range(image.width):
                pixel = image.getpixel((x, y))
                if pixel != bg_color and self.color_already_added(pixel, colors) == False:
                    colors = np.append(colors, np.array([pixel]), axis=0)
        return colors
    
    def get_palette_set(self, image, bg_color):
        colors = set()
        colors_amount = 0
        for y in range(image.height):
            for x in range(image.width):
                pixel = image.getpixel((x, y))
                if pixel != bg_color:
                    colors.add(pixel)
                    colors_amount += 1
        return colors, colors_amount
    
    def color_already_added(self, color, set_of_colors):
        for x in range(set_of_colors.shape[0]):
            if color[0] == set_of_colors[x][0] and color[1] == set_of_colors[x][1] and set_of_colors[x][2]:
                return True
        return False

