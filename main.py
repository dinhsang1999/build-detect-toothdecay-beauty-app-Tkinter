# Import required Libraries
from tkinter import *
import tkinter
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os
from matplotlib import image
import numpy as np
import customtkinter
import threading
import time

# -------- LOADING SREEN --------------

def task():
    # The window will stay open until this function call ends.
    time.sleep(5)
    root.destroy()

WIDTH_GUI_LOADING = 600
HEIGHT_GUI_LOADING = 400

root = customtkinter.CTk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width/2) - (WIDTH_GUI_LOADING/2))
y_cordinate = int((screen_height/2) - (HEIGHT_GUI_LOADING/2))
customtkinter.set_appearance_mode('light') #SYSTEM,Dark,Light
# customtkinter.set_default_color_theme('dark-blue') #green,dark-blue,white
#centre
root.geometry("{}x{}+{}+{}".format(WIDTH_GUI_LOADING,HEIGHT_GUI_LOADING,x_cordinate,y_cordinate))
root.overrideredirect(True)
# root.attributes('-disabled', True)
#Create FRAME



#Draw from here
logo_bme = ImageTk.PhotoImage(Image.open('logo_bme.png').resize((100, 100), Image.ANTIALIAS))
label_logo_bme = customtkinter.CTkLabel(master=root)
label_logo_bme.grid(row=0, column=0)
label_logo_bme.place(relx=0.5, rely=0.2,anchor='center')
# label_logo_bme.pack()
label_logo_bme.configure(image=logo_bme)

title_text = customtkinter.CTkLabel(master=root,text='CARIES DETECTION',text_font=("Roboto Bold", -48),text_color='black')
title_text.grid(row=0, column=0)
title_text.place(relx=0.5, rely=0.5,anchor='center')

intro_text = customtkinter.CTkLabel(master=root,text='a product detect carries early from infrared light by processing image',text_font=("Roboto Medium", -14),text_color='gray')
intro_text.grid(row=0, column=0)
intro_text.place(relx=0.5, rely=0.6,anchor='center')

author_text = customtkinter.CTkLabel(master=root,text='Author: Eng.Nguyen Dac Can \n from biomedical engineering department',text_font=("Roboto Medium", -16),text_color='gray')
author_text.grid(row=0, column=0)
author_text.place(relx=0.5, rely=0.75,anchor='center')

root.after(200, task)
root.mainloop()

#_________________________________________


#---------MAIN---------------------------------
root = customtkinter.CTk()

customtkinter.set_appearance_mode('light') #SYSTEM,Dark,Light
customtkinter.set_default_color_theme('green') #green,dark-blue,white

WIDTH_GUI = 800
HEIGHT_GUI = 500

#Delete all option for user
# root.overrideredirect(True)
#Prevent all user option
# root.attributes('-disabled', True)
#Position GUI
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width/2) - (WIDTH_GUI/2))
y_cordinate = int((screen_height/2) - (HEIGHT_GUI/2))
# customtkinter.set_appearance_mode('light') #SYSTEM,Dark,Light
# customtkinter.set_default_color_theme('dark-blue') #green,dark-blue,white
#centre
root.geometry("{}x{}+{}+{}".format(WIDTH_GUI,HEIGHT_GUI,x_cordinate,y_cordinate))

#-----------Funtion----------------
def CLAHE(img):
    '''
    img: BGR
    return BGR
    '''
    lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)
    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4,4)) #FIXME:
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl,a,b))

    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    return enhanced_img

def change_brightness(img, value=30):
    '''
    img: BGR
    value: inc/dec brightness
    return: BGR
    '''
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v,value)
    v[v > 255] = 255
    v[v < 0] = 0
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def save_info(name_info,gender_info,age_info):
    '''
    Appear patient_info.txt is not exist, then eppend info to the file 
    '''
    path_save = 'patient_info.txt'

    cb = name_info + '-' + gender_info + '-' + age_info

    with open(path_save, 'a') as f:
        f.write(f'\n{cb}')
    
def mask_ori(image_ori,image_gray,scale_rad=50):
    '''
        image_ori:RGB
        image_gray: BGR
        Return: BGR
    '''
    mask = np.zeros(image_ori.shape[:2], dtype="uint8")
    y_centroid = mask.shape[0] // 2
    x_centroid = mask.shape[1] // 2
    radius = y_centroid - scale_rad
    cv2.circle(mask, (x_centroid, y_centroid), radius, 255, -1,lineType=cv2.LINE_AA)
    
    masked = cv2.bitwise_and(image_gray, image_gray, mask=mask)
    mask = cv2.bitwise_not(mask)

    bk = cv2.bitwise_and(image_ori, image_ori, mask=mask)

    return cv2.bitwise_or(masked, bk)

#----------------------------------------------------------------------------------------------------------------------------
#-----------CUSTOM GUI--------------------

WIDTH_CAM = 640
HEIGHT_CAM = 360

# Set GUI
root.title("EARLY CARIES DETECTION APP")

# Logo
photo = PhotoImage(file = "happy.png")
root.iconphoto(False, photo)

# configure grid layout (2x1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Custom frame on window
root.frame_left = customtkinter.CTkFrame(master=root,
                                            width=180,
                                            corner_radius=0)
root.frame_left.grid(row=0, column=0, sticky="nswe")
root.frame_right = customtkinter.CTkFrame(master=root)
root.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

# ============ frame_left ============

# configure grid layout (1x11)
# root.frame_left.grid_rowconfigure(12, weight=1)

logo_bme = ImageTk.PhotoImage(Image.open('logo_bme.png').resize((40, 40), Image.ANTIALIAS))
label_logo_bme = customtkinter.CTkLabel(master=root.frame_left)
label_logo_bme.grid(row=0, column=0)
label_logo_bme.configure(image=logo_bme)

# USER INPUT
input_user = customtkinter.CTkLabel(master=root.frame_left,
                                        text="PATIENT INPUT",
                                        text_font=("Roboto Bold", -16))  # font name and size in px
input_user.grid(row=1, column=0, pady=5, padx=10)

patient_name = customtkinter.CTkLabel(master=root.frame_left,
                                        text='Name',
                                        text_font=("Roboto Medium", -12))
patient_name.grid(row=2, column=0, pady=0, padx=0, sticky='w')

entry_name =  customtkinter.CTkEntry(master=root.frame_left,
                                    width=50,
                                    placeholder_text="Enter your name")
entry_name.grid(row=3, column=0, columnspan=2, pady=0, padx=10, sticky="we")

patient_gender = customtkinter.CTkLabel(master=root.frame_left,
                                        text='Gender',
                                        text_font=("Roboto Medium", -12))
patient_gender.grid(row=4, column=0, pady=0, padx=0, sticky='w')

entry_gender =  customtkinter.CTkEntry(master=root.frame_left,
                                    width=50,
                                    placeholder_text="Enter your gender")
entry_gender.grid(row=5, column=0, columnspan=2, pady=0, padx=10, sticky="we")

patient_age = customtkinter.CTkLabel(master=root.frame_left,
                                        text='Age',
                                        text_font=("Roboto Medium", -12))
patient_age.grid(row=6, column=0, pady=0, padx=0, sticky='w')

entry_age =  customtkinter.CTkEntry(master=root.frame_left,
                                    width=50,
                                    placeholder_text="Enter your age")
entry_age.grid(row=7, column=0, columnspan=2, pady=0, padx=10, sticky="we")

save_button = customtkinter.CTkButton(master=root.frame_left,
                                        text="Save",
                                        command = lambda: save_info(entry_name.get(),entry_gender.get(),entry_age.get()),
                                        text_font=("Roboto Bold", -12))
save_button.grid(row=8, column=0, pady=10, padx=10,sticky='w')

#-------------------------------------------------------------------------------------

exit_button = customtkinter.CTkButton(master=root.frame_left,
                                        text="Exit",
                                        command= lambda: on_closing(),
                                        text_font=("Roboto Bold", -12),
                                        fg_color="#F54040")
exit_button.grid(row=13, column=0, pady=20, padx=10,sticky='w')

# ============ frame_right ============

# videoloop_stop is a simple switcher between ON and OFF modes
videoloop_stop = [False]
button1 = customtkinter.CTkButton(master=root.frame_left,
                                        text="Start",
                                        command = lambda: button1_clicked(videoloop_stop),
                                        text_font=("Roboto Bold", -12),
                                        fg_color="#94B49F",
                                        text_color='white')
button1.grid(row=9, column=0, pady=10, padx=10,sticky='w')


def on_closing():
    # root.after(20)
    global is_running
    is_running = False
    videoloop_stop[0] = False
    root.destroy()

def disable_envent():
    pass

is_running = True
root.protocol("WM_DELETE_WINDOW",disable_envent)

first = customtkinter.CTkLabel(master=root.frame_right,text="Don't PRESS close-button when running CAMERA, STOP camera before or press EXIT!",text_font=("Roboto Bold", -12))
first.grid(row=0, column=0)
first.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# -----------------------------
def start__(mirror=False):

        first.destroy()

        # Appear 2 button for camera
        global snap_button
        global button2
        snap_button = customtkinter.CTkButton(master=root.frame_left,
                                        text="Snap",
                                        command= lambda: snap_shot(),
                                        text_font=("Roboto Bold", -12),
                                        fg_color="#4b208c",
                                        text_color='white')
        button2 = customtkinter.CTkButton(master=root.frame_left,
                                        text="Stop",
                                        command = lambda: button2_clicked(videoloop_stop),
                                        text_font=("Roboto Bold", -12),
                                        fg_color="#DF7861")
        button2.grid(row=10, column=0, pady=10, padx=10,sticky='w')
        snap_button.grid(row=12, column=0, pady=10, padx=10,sticky='w')

        global gray_3

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360) #1080, 720, 360
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) #1920, 1280, 640

        
        cam = customtkinter.CTkLabel(master=root.frame_right,text="Loading Camera....",text_font=("Roboto Bold", -12))
        cam.grid(row=0, column=0)
        cam.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        cam.pack(expand=True,fill=tk.BOTH)
        while is_running:
            if not is_running:
                break

            if videoloop_stop[0]:
                videoloop_stop[0] = False
                cam.destroy()
                break
            # time.sleep(0.05)
            # Get the latest frame and convert into Image
            image= cap.read()[1]
            
            # Flip the image
            flip = cv2.flip(image, 1) #0: vertical ||  1: horizontal

            # Decreare brightness before contrast
            brightness = change_brightness(flip,value=-50) #FIXME:

            # Contrast
            clahe = CLAHE(brightness)
            enhance = cv2.detailEnhance(clahe, sigma_s=10, sigma_r=0.15)

            # Grayscale
            gray_1 = cv2.cvtColor(enhance, cv2.COLOR_BGR2GRAY) #gray 1 chanel
            gray_3 = cv2.cvtColor(gray_1, cv2.COLOR_GRAY2BGR) #gray 3 chanel

            # Mask
            ori = cv2.cvtColor(flip, cv2.COLOR_BGR2RGB)
            final = mask_ori(ori,gray_3)

            #Array to Image
            img = Image.fromarray(final)

            # Convert image to PhotoImage
            imgtk = ImageTk.PhotoImage(image = img)
            cam.imgtk = imgtk
            cam.configure(image=imgtk) #Set width and height of camera

    
def button1_clicked(videoloop_stop):
    thread = threading.Thread(target=start__, args=(videoloop_stop,))
    thread.start()

def button2_clicked(videoloop_stop):
    snap_button.destroy()
    button2.destroy()
    videoloop_stop[0] = True

def save_picture():
    image_name = "IMG-" + time.strftime("%H-%M-%d-%m-%y") + ".jpg"
    path = 'image_save'
    os.makedirs(path,exist_ok=True)
    cv2.imwrite(os.path.join(path,image_name), img_new_win)

    videoloop_stop[0] = False
    new_win.destroy()

def snap_shot():
    global new_win
    global img_new_win
    new_win = customtkinter.CTkToplevel()

    # customtkinter.set_appearance_mode('light') #SYSTEM,Dark,Light
    # customtkinter.set_default_color_theme('green')
    # root.grid_columnconfigure(1, weight=1)
    # root.grid_rowconfigure(0, weight=1)
    # root.frame_left.grid(row=0, column=0, sticky="nswe")
    # root.frame_right = customtkinter.CTkFrame(master=root)
    # root.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

    new_win.attributes('-fullscreen', True)
    picture_label = customtkinter.CTkLabel(master=new_win)
    picture_label.grid(row=0, column=0)
    picture_label.place(relx = 0.5,
            rely = 0.3,
            anchor = 'center')

    img_new_win = gray_3

    imgcvt = Image.fromarray(img_new_win)
    imgtk = ImageTk.PhotoImage(image=imgcvt)
    picture_label.imgtk = imgtk
    picture_label.configure(image=imgtk)
    
    save_button = customtkinter.CTkButton(new_win, text="Save",
                                            text_font=("Roboto Bold", -50),
                                            command= lambda: save_picture(),
                                            width=250,height=68,
                                            text_color='white')
    save_button.grid(row=0, column=0, pady=100, padx=100)
    save_button.place(anchor = 'center',
                        relx = 0.4,
                        rely = 0.6)

    cancel_button = customtkinter.CTkButton(new_win, text="Cancel",
                                                text_font=("Roboto Bold", -50),
                                                command=lambda: new_win.destroy(),
                                                width=250,height=68,
                                                fg_color="#DF7861",
                                                text_color="black",
                                                hover_color="#F54040")
    cancel_button.grid(row=0, column=0, pady=30, padx=30)
    cancel_button.place(anchor = 'center',
                        relx = 0.6,
                        rely = 0.6)
    
    new_win.mainloop()

root.mainloop()   