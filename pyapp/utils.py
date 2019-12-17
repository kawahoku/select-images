
import os, sys
import json
from easydict import EasyDict as edict 
#=================================================================================================#
# read config file

json_file = "config.json"
pardir = os.path.dirname(__file__)
print(pardir)
config_file = os.path.join(pardir, json_file)
read_config = True

if read_config:
    with open(config_file, "r") as f:
        json_obj = json.load(f)

    config = edict(json_obj["DEFAULT"])
    colors = edict(json_obj["COLOR"])
    args = edict(json_obj["ARGS"])

    WINDOW_SIZE = f'{config.WINDOW_W}x{config.WINDOW_H}'
    CANVAS_SIZE = (config.CANVAS_W, config.CANVAS_H)
    POPUP_SIZE = (config.POPUP_W, config.POPUP_H)
    BLOCK_SIZE = (config.BLOCK_W, config.BLOCK_H)

def optimize_params_from_windowWH_ncol_nimage(window_w, window_h, n_col, n_image_per_page):
    if not isinstance(window_h, int): return False
    if not isinstance(window_w, int): return False
    if not isinstance(n_col, int): return False
    if not isinstance(n_image_per_page, int): False

    config.N_COL = n_col
    config.N_IMAGE_PER_PAGE = n_image_per_page
    config.WINDOW_W = window_w
    config.WINDOW_H = window_h
    config.BLOCK_W = int(window_w / (n_col + 1))
    config.BLOCK_H = int(config.BLOCK_W * 0.67)
    config.POPUP_W = int(window_w * 1.0)
    config.POPUP_H = int(window_h * 1.0)
    config.CANVAS_W = int(config.BLOCK_W * (n_col + 1))
    config.CANVAS_H = int((config.BLOCK_H * 1.4) * (1 + n_image_per_page / n_col))
    config.FONTSIZE = window_w // 100

    return True


def Write_Config(config, args):
    json_obj["DEFAULT"] = config
    json_obj["ARGS"] = args
    with open(config_file, "w") as f:
        json.dump(json_obj, f, indent=4)

#================================================================================================="
# utileties ( IS_IMAGE(), SPLIT_LIST(), RESIZE(), MAX_CROP() )
from PIL import Image
import numpy as np

import time

def IS_IMAGE(path):
    for fmt in config.FORMAT:
        if path.endswith(fmt):
            return True
    return False

def SPLIT_LIST(L, n):
    out = []
    for i in range(0, len(L), n):
        out.append(L[i:i+n])
    return out

def RESIZE(img, block_size):
    if isinstance(img, Image.Image):
        img_w, img_h = img.size
        blc_w, blc_h = block_size

        if blc_w and blc_h:
            ratio = blc_w/img_w if img_w/blc_w > img_h/blc_h else blc_h/img_h
        elif blc_w:
            ratio = blc_w / img_w
        elif blc_h:
            ratio = blc_h / img_h

        img_w = int(img_w*ratio)
        img_h = int(img_h*ratio)
        return img.resize((img_w, img_h), Image.ANTIALIAS)
    else:
        raise TypeError("image to RESIZE() must be: 'PIL.Image.Image' or 'cv2 image (np.ndarray)'")

def MAX_CROP(img, block_size):
    img_w, img_h = img.size
    blc_w, blc_h = block_size

    ratio = blc_w/img_w if img_w/blc_w < img_h/blc_h else blc_h/img_h

    img_w = int(img_w*ratio)
    img_h = int(img_h*ratio)
    img = img.resize((img_w, img_h), Image.NEAREST)
    
    padx = img_w - blc_w
    pady = img_h - blc_h
    img = img.crop((padx//2, pady//2, img_w - padx//2, img_h - pady//2))

    return img

def Reload():
    python = sys.executable
    os.execl(python, python, * sys.argv)

#================================================================================================="

if __name__ == "__main__":
    print(json_obj)
    print()
    config.N_COL = 4
    json_obj["DEFAULT"] = config
    Write_Config(config, args)
    print(json_obj)

