import os, sys
import tkinter as tk
from tkinter import filedialog, messagebox, font
from PIL import Image, ImageTk
import numpy as np
import shutil

from tqdm import tqdm

from SelectImagesGUI.utils import *
from SelectImagesGUI.TkFunctions import *



class EntryBox(tk.Frame):
    def  __init__(self, parent, text, pady=30, default=None, FileAPI=True, LabelArgs=args.LABEL_ARGS, EntryArgs=args.ENTRY_ARGS, **kwargs):
        tk.Frame.__init__(self, parent, bg=colors.FILE_BG, **kwargs)

        self.label = tk.Label(self, text=text, **args.LABEL_ARGS)
        self.label.grid(column=0, row=0, pady=(pady, 0))
        self.entry = tk.Entry(self, font=("TkDefaultFont", config.FONTSIZE), **args.ENTRY_ARGS)
        self.entry.grid(column=0, row=1, ipady=3, pady=(0, pady))

        if FileAPI:
            self.button = tk.Button(self, text="..", **args.BUTTON_ARGS)
            self.button.grid(column=1, row=1, pady=(0, pady), padx=(0, 10))
        if default:
            self.entry.insert(0, default)



class FileAPIFrame(tk.Frame):
    def __init__(self, parent, input_dir, output_dir, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.input_box = EntryBox(self, text="input_dir", default=input_dir)
        self.output_box = EntryBox(self, text="output_dir", default=output_dir)
        self.input_box.grid(column=1, row=0)
        self.output_box.grid(column=3, row=0)

        self.save_button = tk.Button(self, text="SAVE", **args.BUTTON_ARGS)
        self.save_button.grid(column=4, row=1)

        self.goleft_button = tk.Button(self, text=" < ", **args.BUTTON_ARGS)
        self.goleft_button.grid(column=1, row=2)
        self.goright_button = tk.Button(self, text=" > ", **args.BUTTON_ARGS)
        self.goright_button.grid(column=3, row=2)
        self.page = tk.Label(self, **args.LABEL_ARGS)
        self.page.grid(column=2, row=2)



class ImageBlock(tk.Frame):
    def __init__(self, parent, branch_path, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.branch_path = branch_path
        self.file_name = branch_path.split("/")[-1]

        self.tk_img = None
        self.image_label= None
        self.caption_label=None



class Gallery_2(tk.Frame):
    def __init__(self, parent, image_paths, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.image_blocks = []
        self.master_dir = parent.master_dir
        self.image_paths = image_paths

    def load_ImageBlocks(self):
        for i, branch_path in enumerate(tqdm(self.image_paths)):
            new_block = self.NewImageBlock(branch_path)
            self.putImageBlock(new_block, i)
            self.image_blocks.append(new_block)

    def NewImageBlock(self, branch_path):
        new_block = ImageBlock(self, branch_path, **{"bg": colors.GALLERY_BG})

        img = Image.open(os.path.join(self.master_dir, branch_path))
        new_block.tk_img = ImageTk.PhotoImage(MAX_CROP(img, BLOCK_SIZE))
        new_block.image_label = tk.Label(new_block, **{
            "image": new_block.tk_img,
            "activebackground": "red",
            "takefocus": 1,
            "text": new_block.file_name,
            "borderwidth": 2,
            "pady": 1
        })
        new_block.caption_label = tk.Label(new_block, text=new_block.file_name, wraplength=config.BLOCK_W, **args.CAPTION_ARGS)

        new_block.image_label.grid(column=0, row=0)
        new_block.caption_label.grid(column=0, row=1)
        return new_block

    def putImageBlock(self, block, idx):
        col = idx % config.N_COL
        row = int(idx // config.N_COL)
        block.grid(column=col, row=row, pady=(20, 0), padx=3)



class SettingWindow(tk.Frame):
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, bg="#221133", **kwargs)

        self.set_window_w = EntryBox(self, text="Window Width", default=config.WINDOW_W, FileAPI=False,\
                                        LabelArgs=args.SUB_LABEL_ARGS, EntryArgs=args.SUB_ENTRY_ARGS)
        self.set_window_w.grid(column=1, row=1, padx=20, pady=10)
        self.set_window_h = EntryBox(self, text="Window Height", default=config.WINDOW_H, FileAPI=False,\
                                        LabelArgs=args.SUB_LABEL_ARGS, EntryArgs=args.SUB_ENTRY_ARGS)
        self.set_window_h.grid(column=2, row=1, padx=20, pady=10)
        self.set_ncol = EntryBox(self, text="[ image / row ]", default=config.N_COL, FileAPI=False,\
                                        LabelArgs=args.SUB_LABEL_ARGS, EntryArgs=args.SUB_ENTRY_ARGS)
        self.set_ncol.grid(column=1, row=2, padx=20, pady=10)
        self.set_nimage = EntryBox(self, text="[ image / page ]", default=config.N_IMAGE_PER_PAGE, FileAPI=False,\
                                        LabelArgs=args.SUB_LABEL_ARGS, EntryArgs=args.SUB_ENTRY_ARGS)
        self.set_nimage.grid(column=2, row=2, padx=20, pady=10)

        self.cancel = tk.Button(self, text="Cancel", command=self.Quit)
        self.apply = tk.Button(self, text="Apply", command=self.ApplyChanges)
        self.cancel.grid(column=3, row=3)
        self.apply.grid(column=4, row=3)

    def Quit(self):
        self.master.destroy()

    def ApplyChanges(self):
        window_w = int(self.set_window_w.entry.get())
        window_h = int(self.set_window_h.entry.get())
        n_col = int(self.set_ncol.entry.get())
        n_image_per_page = int(self.set_nimage.entry.get())

        optimize_params_from_windowWH_ncol_nimage(window_w, window_h, n_col, n_image_per_page)
        Write_Config(config, args)

        if messagebox.askyesno("Reload now?", "Reload app now?\n(These changes are reflected after reloading)"):
            Reload()



class MenuBar(tk.Menu):
    def __init__(self, root, **kwargs):
        tk.Menu.__init__(self, root, **kwargs)
        self.root = root

        
        # ファイルメニュー
        self.filemenu = tk.Menu(self, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.NewFile)
        self.filemenu.add_command(label="Reload", command=self.reload)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Close Tab", command=self.test)
        self.filemenu.add_command(label="Close App", command=self.Quit)
        self.add_cascade(label="File", menu=self.filemenu)
        
        self.filemenu = tk.Menu(self, tearoff=0)
        self.filemenu.add_command(label="Preference", command=self.SetPreference)
        self.add_cascade(label="Edit", menu=self.filemenu)

    def test(self):
        print("hello")

    def reload(self):
        if messagebox.askyesno("Reload now?", "Reload now?"):
            Reload()

    def NewFile(self):
        self.root.winfo_children()[0].frame.FileAPI_for_input_box()

    def Quit(self):
        self.root.destroy()

    def SetPreference(self):
        window = tk.Toplevel()
        sub_frame = SettingWindow(window)
        sub_frame.pack()
        window.mainloop()



class MainFrame(tk.Frame):
    """
        Background Preference
    """
    def __init__(self, parent, input_dir=None, output_dir=None, **kwargs):
        tk.Frame.__init__(self, parent, **args.MAINFRAME_ARGS)
        # tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.master_dir = input_dir
        self.output_dir = output_dir

        self.gallery_paths = []
        self.gallerys = []
        self.now_focus = 0
        self.file_frame = FileAPIFrame(self, self.master_dir, output_dir, **args.FILE_ARGS)
        self.file_frame.pack()

        if self.master_dir:
            self.LoadFirstGallery()

        self.BINDING()

    def RemoveFocus(self):
        focus_on(self)

    def LoadFirstGallery(self):
        all_branch_paths = AllImagesUnderDirectory(self.master_dir)
        self.gallery_paths = SPLIT_LIST(all_branch_paths, config.N_IMAGE_PER_PAGE)
        self.file_frame.page.config(text=f"{self.now_focus+1}/{len(self.gallery_paths)}")
        self.load_gallery(0)
        self.gallerys[0].pack()

    def load_gallery(self, idx):
        new_gallery = Gallery_2(self, self.gallery_paths[idx], **args.GALLERY_ARGS)
        new_gallery.load_ImageBlocks()
        for image_block in new_gallery.image_blocks:
            image_block.image_label.bind("<Button-1>", self.LeftClickEvent)
            image_block.image_label.bind("<Button-3>", self.RightClickEvent)

        self.gallerys.append(new_gallery)

    def BINDING(self, for_file_frame=True, for_gallery=True):
        if for_file_frame:
            self.file_frame.input_box.button.config(command=self.FileAPI_for_input_box)
            self.file_frame.output_box.button.config(command=self.FileAPI_for_output_box)
            self.file_frame.save_button.config(command=self.SaveButtonEvent)

            self.file_frame.goleft_button.config(command=self.GOLeftEvent)
            self.file_frame.goright_button.config(command=self.GORightEvent)
            self.file_frame.page.config(text=f"{self.now_focus+1}/{len(self.gallery_paths)}")

    def RELOAD_GALLERY(self):
        for gallery in self.gallerys:
            gallery.destroy()

        self.gallerys = []
        self.now_focus = 0
        self.file_frame.page.config(text=f"{self.now_focus+1}/{len(self.gallery_paths)}")
        self.LoadFirstGallery()

    def TURN_GALLERY(self, val):
        self.RemoveFocus()
        self.gallerys[self.now_focus].pack_forget()
        self.now_focus += val
        if self.now_focus >=  len(self.gallery_paths):
            self.now_focus = 0
        elif self.now_focus < 0:
            self.now_focus = len(self.gallery_paths) - 1

        if self.now_focus >= len(self.gallerys):
            self.load_gallery(self.now_focus)
        self.gallerys[self.now_focus].pack()
        self.file_frame.page.config(text=f"{self.now_focus+1}/{len(self.gallery_paths)}")

    def GOLeftEvent(self):
        self.TURN_GALLERY(-1)

    def GORightEvent(self):
        self.TURN_GALLERY(+1)

    def INCERT_TO(self, entry, key, dir_name):
        entry.delete(0, "end")
        entry.insert(0, dir_name)
        entry.xview_moveto(1.0)

        if key == "input":
            self.master_dir = dir_name
        elif key == "output":
            self.output_dir = dir_name
        else:
            print("Invalid key")

    def FileAPI_for_input_box(self):
        self.RemoveFocus()
        master_dir = filedialog.askdirectory(initialdir = 'C:\\pg')
        if master_dir:
            self.INCERT_TO(self.file_frame.input_box.entry, "input", master_dir)

            output_dir = CountupIfExists(self.master_dir, f"{self.master_dir}_selected")

            self.INCERT_TO(self.file_frame.output_box.entry, "output", output_dir)

            self.RELOAD_GALLERY()

    def FileAPI_for_output_box(self):
        self.RemoveFocus()
        output_dir = filedialog.askdirectory(initialdir = 'C:\\pg')
        if output_dir:
            self.INCERT_TO(self.file_frame.output_box.entry, "output", output_dir)

    def LeftClickEvent(self, event):
        self.RemoveFocus()
        # Toggle Active
        if event.widget["state"] == "active":
            event.widget["state"] = "normal"
        else:
            event.widget["state"] = "active"

    def RightClickEvent(self, event):
        self.RemoveFocus()
        # popup image
        master_dir = event.widget.master.master.master.master_dir
        branch_path = event.widget.master.branch_path
        PopupImage(master_dir, branch_path)

    def SaveButtonEvent(self):
        self.RemoveFocus()

        self.output_dir = self.file_frame.output_box.entry.get()

        SaveSelectedImages(self.gallerys, self.master_dir, self.output_dir)



class MainCanvas(tk.Canvas):
    """
        UI Preference
    """
    def __init__(self, root, input_dir, output_dir, **kwargs):
        tk.Canvas.__init__(self, root, **kwargs)

        self.root = root
        self.menubar = MenuBar(root)
        self.root.config(menu=self.menubar)
        self.frame = MainFrame(self, input_dir, output_dir)

        self.BINDING()
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

    def BINDING(self):
        # scroll bar setting
        bar = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        bar.pack(side=tk.RIGHT, fill=tk.Y)
        bar.config(command=self.yview)

        self.config(yscrollcommand=bar.set)
        self.config(scrollregion=(0,0,config.CANVAS_W,config.CANVAS_H))
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_window((0,0), window=self.frame, anchor=tk.NW, width=config.CANVAS_W, height=config.CANVAS_H)


        # binding to keyboard and mouse button

        # linux mouse bind
        try:
            self.bind_all("<Button>", self.MouseBind)
            self.bind_all("<Shift-Button>", self.ShiftMouseBind)
        except:
            print("Button key bind failed: OS will be windows or mac")

        # windows and mac
        try:
            self.bind_all("<Button>", self.MouseBind)
            self.bind_all("<Shift-Button>", self.ShiftMouseBind)
        except:
            print("Button key bind failed: OS will be linux")

        self.bind_all("<Key>", self.KeyBind)

        # self.bind_all("<Control-Button>", self.ControlMouseBind)

    def ControlMouseBind(self, event):
        x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        y = self.root.winfo_pointery() - self.root.winfo_rooty()
        print(x, y)
        
        num = event.num
        if   num == 4:
            self.scale("all", x, y, 1.25, 1.25)
        elif num == 5:
            self.scale("all", x, y, 0.8, 0.8)


    def Scroll(self, direction, delta):
        if   direction == "y":
            self.yview_scroll(-1*(delta//120), "units")
        elif direction == "x":
            self.xview_scroll(-1*(delta//120), "units")

    def KeyBind(self, event):
        key = event.keysym
        if   key == "j": self.Scroll("y", -120)
        elif key == "k": self.Scroll("y", +120)
        elif key == "h": self.Scroll("x", +120)
        elif key == "l": self.Scroll("x", -120)

        elif key == "Down":  self.Scroll("y", -120)
        elif key == "Up":    self.Scroll("y", +120)
        elif key == "Left":  self.Scroll("x", +120)
        elif key == "Right": self.Scroll("x", -120)

        elif key == "n": self.frame.GORightEvent()
        elif key == "q": self.root.quit()
        # elif key == "Return": 

    def MouseBind(self, event):
        if   event.num == 4: self.Scroll("y", +120)
        elif event.num == 5: self.Scroll("y", -120)
        elif event.num == 6: self.Scroll("x", +120)
        elif event.num == 7: self.Scroll("x", -120)

        elif event.delta == +120: self.Scroll("y", +120)
        elif event.delta == -120: self.Scroll("y", -120)

    def ShiftMouseBind(self, event):
        num = event.num
        if   num == 4: self.Scroll("x", +120)
        elif num == 5: self.Scroll("x", -120)

        elif event.delta == +120: self.Scroll("x", +120)
        elif event.delta == -120: self.Scroll("x", -120)

