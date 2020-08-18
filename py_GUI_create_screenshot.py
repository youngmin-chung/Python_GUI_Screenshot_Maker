from tkinter import *
from tkinter import ttk
import os
from tkinter import filedialog
import tkinter.messagebox as msgbox
from PIL import Image

root = Tk()
root.title("Python GUI")

# add file function

def add_file():
    files = filedialog.askopenfilenames(title = "Select image file(s)", filetypes=(("PNG", "*.png"), ("All files", "*.*")), initialdir = "C:/")
    # file list 
    for file in files:
        list_file.insert(END, file)


# delete file function
def delete_file():
    for index in reversed(list_file.curselection()):
        list_file.delete(index)

# save path (folder)
def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    # user click cancel 
    if folder_selected == '':
        return
    txt_dest_path.delete(0,END)
    txt_dest_path.insert(0, folder_selected)

# merge images
def merge_image():
    try:
        # width 
        img_width = cmb_width.get()
        if img_width == "Original":
            img_width = -1
        else:
            img_width = int(img_width)

        # space
        img_space = cmb_space.get()
        if img_space == "Narrow":
            img_space = 30
        elif img_space == "Normal":
            img_space = 60
        elif img_space == "Broaden":
            img_space = 90
        else:
            img_space = 0

        # format
        img_format = cmb_format.get().lower()
        
        
        #print(list_file.get(0, END)) # all file list
        images = [Image.open(x) for x in list_file.get(0, END)]

        # processing image size list
        image_sizes = []
        if img_width > -1:
            image_sizes = [(int(img_width), int(img_width * x.size[1] / x.size[0])) for x in images]
        else:
            image_sizes = [(x.size[0], x.size[1]) for x in images]

        
        widths, heights = zip(*(image_sizes))   

        # max width, total height values
        max_width, total_height = max(widths), sum(heights)

        # sketchbook
        if img_space > 0: # apply image space
            total_height += (img_space * (len(images) - 1))


        result_img = Image.new("RGB", (max_width, total_height), (255,255,255))
        y_offset = 0
        # for img in images:
        #     result_img.paste(img, (0,y_offset))
        #     y_offset += img.size[1] # add height value

        for idx, img in enumerate(images):
            # if width is not "Original"
            if img_width > -1:
                img = img.resize(image_sizes[idx])

            
            result_img.paste(img, (0, y_offset))
            y_offset += (img.size[1] + img_space)

            progress = (idx + 1) / len(images) * 100
            p_var.set(progress)
            progress_bar.update()

        # format option processing
        file_name = "merge_photo."+img_format
        dest_path = os.path.join(txt_dest_path.get(), file_name)
        result_img.save(dest_path)
        msgbox.showinfo("Alarm", "Completed..")
    except Exception as err: # exception
        msgbox.showerror("Error", err)
# Start
def start():
    # check the option value   

    # file list check
    if list_file.size() == 0:
        msgbox.showwarning("Warning", "Please add image file")
        return
    # path check
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("Warning", "Please select path")
        return
    # merge images
    merge_image()

# file frame (add files, select files, delete files)
file_frame = Frame(root)
file_frame.pack(fill="x")

btn_add_file = Button(file_frame, padx = 5, pady = 5, width = 12, text = "Add File(s)", command = add_file)
btn_add_file.pack(side="left", padx = 5, pady = 5)

btn_del_file = Button(file_frame, padx = 5, pady = 5, width = 12, text = "Select/Delete", command = delete_file)
btn_del_file.pack(side="right", padx = 5, pady = 5)

# list frame
list_frame = Frame(root)
list_frame.pack(fill="both")

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_file = Listbox(list_frame, selectmode="extended", height = 15, yscrollcommand= scrollbar.set)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)

# path frame
path_frame = LabelFrame(root, text="path")
path_frame.pack(fill="x", padx = 5, pady = 5, ipady=5)

txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side="left", fill="x", expand = True, padx = 5, pady = 5, ipady=4) # height changed

btn_dest_path = Button(path_frame, text = "Open", width = 10, command = browse_dest_path)
btn_dest_path.pack(side="right", padx = 5, pady = 5)

#option frame
frame_option = LabelFrame(root, text="Option")
frame_option.pack(padx = 5, pady = 5, ipady=5)

# 1. width option
# width label
lbl_width = Label(frame_option, text = "width", width = 8)
lbl_width.pack(side="left", padx = 5, pady = 5)

# width comobo
opt_width = ["Original", "1024", "800", "640"]
cmb_width = ttk.Combobox(frame_option, state="readonly", values=opt_width)
cmb_width.current(0)
cmb_width.pack(side="left", padx = 5, pady = 5)

# 2. space option
lbl_space = Label(frame_option, text = "space", width = 8)
lbl_space.pack(side="left", padx = 5, pady = 5)

# space combo
opt_space = ["None", "Narrow", "Normal", "Broaden"]
cmb_space = ttk.Combobox(frame_option, state="readonly", values=opt_space)
cmb_space.current(0)
cmb_space.pack(side="left", padx = 5, pady = 5)

# 3. file format
lbl_format = Label(frame_option, text = "format", width = 8)
lbl_format.pack(side="left", padx = 5, pady = 5)

# format combo
opt_format = ["PNG", "JPG", "BMP"]
cmb_format = ttk.Combobox(frame_option, state="readonly", values=opt_format)
cmb_format.current(0)
cmb_format.pack(side="left", padx = 5, pady = 5)

# progress bar
frame_progress = LabelFrame(root, text="progress")
frame_progress.pack(fill="x", padx = 5, pady = 5, ipady=5)

p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable = p_var)
progress_bar.pack(fill="x", padx = 5, pady = 5)

# Run frame
frame_run = Frame(root)
frame_run.pack(fill="x", padx = 5, pady = 5)

btn_close = Button(frame_run, padx = 5, pady = 5, text = "Close", width = 12, command = root.destroy)
btn_close.pack(side="right", padx = 5, pady = 5)

btn_start = Button(frame_run, padx = 5, pady = 5, text = "Start", width = 12, command = start)
btn_start.pack(side="right", padx = 5, pady = 5)



root.resizable(False, False)
root.mainloop()