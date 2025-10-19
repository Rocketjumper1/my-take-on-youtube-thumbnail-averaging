import yt_dlp
import os
import tkinter as tk
import numpy as np
from image_averager import img_averager
from PIL import Image, ImageTk
average_func_array = []
for name, member in vars(img_averager).items():
    if isinstance(member, staticmethod):
        func = member.__func__
        average_func_array.append(func)
sshot_folder = ""
list = []
img_size = (500, 500)
MIN_LENGTH =  60
up_b = None
down_b = None
image= None
view = None
blur = None
debug = True
debug_channel = "youtube.com/@emnersonn"
yt_dlp_p = {
"skip_download": True,
"writethumbnail": True, #tell it to write the thumbnail only
"outtmpl": "%(uploader)s/%(title)s.%(ext)s", #the output folder(s)
"quiet": False,
"ignoreerrors": True,
"no_warnings": True  #make sure the video is longer than MIN_LENGTH


}

count = 0
counter = 0
def start_event():
	global sshot_folder
	global view
	global entry
	read = entry.get()


	screenshot_grabber(read)
def down(L, D):
	global counter
	if (counter - 1) >= 0:
		counter -= 1
	clear()
	image_viewer(L, D)


def up(L, D):
	global counter
	if (counter + 1) <= (len(L) - 1):
		counter += 1
	clear()
	image_viewer(L, D)
def clear():
    global R
    for element in R.winfo_children():
            element.destroy()
def average_img(folder, out_folder):
        global R
        
        
        
        print(folder)
        print(out_folder)
        ls = os.listdir(folder)
        print(ls, out_folder)
        clear()
        if not os.path.isdir(out_folder):
            os.mkdir(out_folder)
        else:
            lsi = os.listdir(out_folder)
            for i in lsi:
                os.remove(out_folder + f"/{i}")
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
def print_mult(sentance, num, ends="\n"):
    for i in range(num):
        print(sentance, end=ends)
def return_start():
    global entry
    clear()
    R.title("screenshot shower")
    R.geometry("1200x1600")
    label = tk.Label(R, text="what channel would you like to view the thumbnails of... please enter url to their channel")
    label.pack(pady=3)
    entry = tk.Entry(R, width = 30)
    entry.insert(0, "youtube.com/@")
    entry.pack()
    start = tk.Button(R, text="confirm_channel", command = start_event)
    start.pack()
def image_viewer(lis= [], dr = ""):
	view.destroy()
	global R
	global down_b
	global up_b
	global blur
	global image
	global counter
	R.title("image viewin time")
	go_back = tk.Button(R, text="go back to url entering", command= return_start)
	print(f"directory passed is {dr}, list is {lis}")
	Dr = f"{dr}/{lis[counter]}"
	print(dr)
	blur = tk.Button(R, text= "want to see all thumbnails bflurred?", command= lambda fold =dr, o_fold=f"{dr}: averaged": average_img(fold, o_fold) )
	blur.pack(anchor="nw")
	img = Image.open(Dr).resize(img_size)
	tk_img = ImageTk.PhotoImage(img)
	image= tk.Label(R, image = tk_img)
	image.image = tk_img
	saved_to = tk.Label(R, text=f"all images saved to {dr}")
	go_back.pack(anchor="ne")
	image.pack()
	up_b = tk.Button(R, text= "next image -->", command=lambda l=lis, d=dr: up(l, d))
	down_b = tk.Button(R, text= "<-- go back", command=lambda l=lis, d=dr: down(l, d))
	down_b.pack()
	up_b.pack()
	saved_to.pack()
def screenshot_grabber(channel_url):
    global R
    clear()
    with yt_dlp.YoutubeDL(yt_dlp_p) as ydl:
        info = ydl.extract_info(channel_url, download= False)
        ls = os.listdir(info.get('uploader'))
        dr = os.path.dirname(os.path.abspath(__file__))
        for i in ls:
            deldir = f"{dr}/{info.get('uploader')}/{i}"
            print(f"removing {deldir}")
            os.remove(deldir)

        if info.get('_type') == "playlist":
            entries = []
            for e in info.get('entries'):
                if e.get('duration') is not None and e.get('duration') > MIN_LENGTH:
                    print(f"video: {e.get('title')} duration: {e.get('duration')}")
                    entries.append(e)
            urls = [e['webpage_url'] for e in entries]
            print(urls)
            ydl.download(urls)
        elif info.get('duration') is not None and info.get('duration') > MIN_LENGTH:
            ydl.download([channel_url])
        uploader = info.get("uploader") or "unknown"
        l = os.listdir(uploader)
        global view
        view = tk.Button(R, text = "would you like to start viewing images", command = lambda ls=l , d=os.path.dirname(os.path.abspath(__file__)) + f"/{uploader}" : image_viewer(ls, d)  )
        view.pack()


R = tk.Tk() # the root of the tkinter gui
R.title("screenshot shower")
R.geometry("1200x1600")
label = tk.Label(R, text="what channel would you like to view the thumbnails of... please enter url to their channel")
label.pack(pady=3)
entry = tk.Entry(R, width = 30)
entry.insert(0, "youtube.com/@")
entry.pack()

start = tk.Button(R, text="confirm_channel", command = start_event)
start.pack()

if __name__ == "__main__":
    R.mainloop()

