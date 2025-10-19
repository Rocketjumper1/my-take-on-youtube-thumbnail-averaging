from PIL import Image, ImageTk
import os
import time
from image_averager import img_averager
import tkinter as tk
average_folder = ""
located_in = os.path.dirname(os.path.abspath(__file__)) 
img_size = (500, 500)
average_func_array = []
for name, member in vars(img_averager).items():
    if isinstance(member, staticmethod):
        func = member.__func__
        average_func_array.append(func)

def start():
    average_img(f"{located_in}/{entry.get()}", f"{located_in}/{entry.get()}: averaged")
def clear():
    global R
    for i in R.winfo_children():
        i.destroy()

images = []
dir_start = f"{located_in}/{average_folder}"
dir_list = os.listdir(dir_start)
count = 0

def average_img(folder, out_folder):
        global R
        
        
        
        print(folder)
        print(out_folder)
        ls = os.listdir(folder)
        print(ls, out_folder)
        clear()
        if not os.path.isdir(out_folder):
            os.mkdir(out_folder)
        
        images = []
        for i in ls:
            path = f"{folder}/{i}"
            print(i)
            images.append(Image.open(path))
   
        
        
 
        
        avg_img, current_method =  average_func_array[count](images, img_size)
        
        avg_img.save(f"{out_folder}/image {current_method}.png")
        saved_to = tk.Label(R, text=f"image saved to {folder}/image {current_method}.png")
        img_tk = ImageTk.PhotoImage(avg_img)
        image = tk.Label(R, text="average_img", image=img_tk)
        
        
        def helper_up():
            global R
            global count
            clear()
            if count + 1 < len(average_func_array):
                count += 1
            average_img(folder, out_folder)
        def helper_down():
            global R
            global count
            clear()
            if count - 1 >= 0 :
                count -= 1
            average_img(folder, out_folder)
        def helper_del_func():
            clear()
            image_viewer(ls, folder)
        go_back = tk.Button(R, text = "go back", command = helper_del_func)
        button_up = tk.Button(R, text= "Next method -->", command = helper_up)
        button_down = tk.Button(R, text = "<-- Previous_method", command = helper_down)
        ave_type = tk.Label(R, text=current_method)
        up = tk.Button(R, text = "go to next")
        go_back.pack(anchor="nw")
        image.image = img_tk
        image.pack()
        button_up.pack()
        button_down.pack()
        ave_type.pack()
        saved_to.pack()
R = tk.Tk()
R.geometry("1000x1000")
R.title("image averager by local directory (folder must be in same dir as script)")
entry = tk.Entry(R, width = 30)
activate = tk.Button(R, text="average this directory?", command = start)
entry.pack()
activate.pack()
if __name__ == "__main__":
    R.mainloop()