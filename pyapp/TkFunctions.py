import os, shutil
import tkinter as tk
from PIL import Image

from utils import IS_IMAGE, RESIZE, config

def SaveSelectedImages(tkGallerys, input_dir, output_dir):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("\n===================== SAVE BEGIN =======================")
    selected = []
    for gallery in tkGallerys:
        for block in gallery.image_blocks:
            if block.image_label["state"] ==  "active":
                selected.append(block.branch_path)
    new_images = []
    existing_images = []

    log_text = ""
    log_text += f"{input_dir}\n\n -> \n\n{output_dir}\n\n"
    for branch_path in selected:
        input_path = os.path.join(input_dir, branch_path)
        output_path = os.path.join(output_dir, branch_path)
        output_dir = output_path.rsplit("/", 1)[0]
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        if os.path.isfile(output_path):
            existing_images.append(branch_path)
            continue
        else:
            new_images.append(branch_path)
            shutil.copyfile(input_path, output_path)

    log_text += f"\n-----------------------------------------\n"
    log_text += f"SELECTED:\n{selected}\n"
    log_text += f"\n-----------------------------------------\n"
    log_text += f"SAVED:\n{new_images}\n"
    log_text += f"\n-----------------------------------------\n"
    log_text += f"ALREADY EXIST:\n{existing_images}\n\n"
    log_text += f"\n-----------------------------------------\n"
    tk.messagebox.showinfo("Save Complete", log_text)

    print(log_text)
    print("===================== SAVE COMPLETE ====================\n")

def PopupImage(master_dir, branch_path):
    img = Image.open(os.path.join(master_dir, branch_path))
    img = RESIZE(img, (config.POPUP_W, config.POPUP_H))
    img.show(title=branch_path)

def CountupIfExists(master_dir, path):
    idx = 1
    while(os.path.exists(path)):
        path = master_dir + f"_selected({idx})"
        idx += 1
    return path

def AllImagesUnderDirectory(master_dir):
    searchlist = [("", os.listdir(master_dir))]
    all_branch_paths = []
    for filetuple in searchlist:
        branch_dir, file_list = filetuple
        # print(branch_dir)
        for file_name in file_list:
            branch_path  = os.path.join(branch_dir, file_name)
            full_path = os.path.join(master_dir, branch_path)
            if IS_IMAGE(full_path):
                all_branch_paths.append(branch_path)
            elif os.path.isdir(full_path):
                searchlist.append((branch_path, os.listdir(full_path)))
            else:
                # print("otherwise")
                pass

    return all_branch_paths


def focus_on(widget):
    widget.focus_set()

