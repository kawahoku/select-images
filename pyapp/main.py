import os
import tkinter as tk
from tkinter import font
from argparse import ArgumentParser

from SelectImagesGUI.utils import config, WINDOW_SIZE
from SelectImagesGUI.pyTkComponents import MainCanvas


def gui_demo(input_dir, output_dir):

    root = tk.Tk()
    root.geometry(WINDOW_SIZE)
    root.title("Select Images")
    font.nametofont('TkDefaultFont').configure(size=config.FONTSIZE)

    if input_dir:
        idx = 1
        output_dir = input_dir + "_selected"
        while os.path.exists(output_dir):
            output_dir = input_dir + f"_selected({idx})"
            idx += 1

    print(output_dir)
    app = MainCanvas(root, input_dir, output_dir)
    root.mainloop()


def main():
    description = 'images_gui'

    parser = ArgumentParser(description=description, add_help=False)
    parser.add_argument('--input-dir', type=str, required=False, default=None,
                        dest='input_dir', help='input_dir')
    parser.add_argument('--output-dir', type=str, required=False, default=None,
                       dest='output_dir', help='output dir')
    args = parser.parse_args()

    gui_demo(args.input_dir, args.output_dir)


if __name__ == '__main__':
    main()
