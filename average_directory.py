from PIL import Image, ImageTk
import os
import threading
import time
from image_averager import img_averager
import tkinter as tk
average_folder = ""
located_in = os.path.dirname(os.path.abspath(__file__)) 
img_size = (500, 500)
imgs = []
stop_event = threading.Event()
methods = []
first = True
average_func_array = []
for name, member in vars(img_averager).items():
    if isinstance(member, staticmethod):
        func = member.__func__
        average_func_array.append(func)
def working(Event):
    count = 4
    while not Event.is_set():
        print(f"working{'.' * (count % 4)}", end = "\r")
        count += 1
        time.sleep(0.2)
        print("             ",end = "\r")
        
        

def start():
    global average_folder
    average_folder = entry.get()
    ls = os.listdir(f"{located_in}/{average_folder}")
    image_viewer(ls, f"{located_in}/{average_folder}")
def clear():
    global R
    for i in R.winfo_children():
        i.destroy()

images = []
dir_start = f"{located_in}/{average_folder}"
dir_list = os.listdir(dir_start)
count = 0
counter = 0
def average_img(folder, out_folder):
        global R
        global first
        global imgs
        global methods
        
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
   
        
        
         
        if first:
            for i in range(len(average_func_array)):
                stop_event.clear()
                threading.Thread(target=working, args=(stop_event,)).start()
                avg_img, current_method =  average_func_array[i](images, img_size)
                stop_event.set()
                labe = tk.Label(R, text = f"saving {current_method} img")
                labe.pack()
                R.update_idletasks()
                avg_img.save(f"{out_folder}/image {current_method}.png")
                imgs.append(avg_img)
                methods.append(current_method)
            first = False
        saved_to = tk.Label(R, text=f"image saved to {folder}/image {methods[count]}.png")
        img_tk = ImageTk.PhotoImage(imgs[count])
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
        ave_type = tk.Label(R, text=methods[count])
        up = tk.Button(R, text = "go to next")
        go_back.pack(anchor="nw")
        image.image = img_tk
        image.pack()
        button_up.pack()
        button_down.pack()
        ave_type.pack()
        saved_to.pack()

def image_viewer(lis= [], dr = ""):
    clear()
    global R
    global down_b
    global up_b
    global blur
    global image
    global counter
    def back_to_dir_entering():
        global R
        
        clear()
        entry = tk.Entry(R, width = 30)
        activate = tk.Button(R, text="average this directory?", command = start)
        entry.pack()
        activate.pack()
    R.title("image viewin time")
    print(f"directory passed is {dr}, list is {lis}")
    Dr = f"{dr}/{lis[counter]}"
    print(dr)
    dir_enter = tk.Button(R, text = "go back to directory entering?", command = back_to_dir_entering)
    blur = tk.Button(R, text= "want to see all thumbnails bflurred?", command= lambda fold =dr, o_fold=f"{dr}: averaged": average_img(fold, o_fold) )
    blur.pack(anchor="nw")
    dir_enter.pack(anchor="ne")
    img = Image.open(Dr).resize(img_size)
    tk_img = ImageTk.PhotoImage(img)
    image= tk.Label(R, image = tk_img)
    image.image = tk_img
    saved_to = tk.Label(R, text=f"all images saved to {dr}")
    image.pack()
    def up():
        global counter
        if counter + 1 < len(lis):
            counter += 1
        image_viewer(lis, dr)
    def down():
        global counter
        if counter - 1 >= 0:
            counter -= 1
        image_viewer(lis, dr)
    up_b = tk.Button(R, text= "next image -->", command=up)
    down_b = tk.Button(R, text= "<-- go back", command=down)
    down_b.pack()
    up_b.pack()
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
