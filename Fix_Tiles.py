import os
import json
import logging
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

#SE => AE
dic_mapping = {
    # Mirror
    (8,16):(13,16),
    # Grate
    (9,16):(11,16),
    # Platform
    (10,16):(6,16),
    # Water
    (11,16):(12,16),
    # Bridge
    (12,16):(15,16),
    # Spike Left
    (13,16):(9,16),
    # Spike Top
    (14,16):(7,16),
    # Spike Right
    (15,16):(10,16),
    # Spike Bottom
    (16,16):(8,16),
    # Foreground
    (16,15):(14,16)
}

cwd = os.getcwd()
logging.basicConfig(filename='0_Fix_Tiles.log', level=logging.INFO, format='%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.info('Script launched!')

path = ''
if path == '':
    path = cwd

if 'out' not in os.listdir(path) or not os.path.isdir('out'):
    os.mkdir(path + '\\' + 'out')

list_all = [file for file in os.listdir(path) if file[-4:] == ".png"]

for png in list_all:
    path_png =  path + '\\' + png
    path_out_png =  path + '\\out\\' + png
    
    logging.info('Processing image: ' + path_png)
    im = Image.open(path_png).convert()
    
    x_tiles = int(im.size[0] / 17)
    y_tiles = int(im.size[1] / 17)
    
    try:
        for x_tile in range(x_tiles):
            for y_tile in range(y_tiles):
                # Cut image tile by tile
                box = (x_tile*17, (y_tile)*17, (x_tile+1)*17, (y_tile+1)*17)
                region = im.crop(box)

                # Load image as list of pixels
                pixels = region.load()

                # Load all pixels of metadata -- Got a bit confused with x and y and swapped them... Oops! Maybe Fix that?
                last_row = {(16, i): pixels[i,16] for i in range(17)}
                last_col = {(i, 16): pixels[16,i] for i in range(16)}

                dic = dict(last_col)
                dic.update(last_row)

                list_px_edit = []

                # Load pixels to change
                for coor in dic:
                    # If not transparent and in dic_mapping
                    if dic[coor][3] >= 50 and coor in dic_mapping:
                        list_px_edit.append(coor)

                # Change old pixels to new
                for coor in list_px_edit:
                    x_old = coor[0]
                    y_old = coor[1]

                    new_coor = dic_mapping[coor]
                    x_new = new_coor[0]
                    y_new = new_coor[1]

                    pixels[y_old,x_old] = (0, 0, 0, 0)
                    pixels[y_new,x_new] = (0, 0, 0, 255)

                im.paste(region, box)
                im.crop(box)

        im.save(path_out_png)
    except:
        print(png)
#         raise