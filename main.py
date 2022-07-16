# Import required Libraries
from tkinter import *
import tkinter
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os
from cv2 import mean
from matplotlib import image
import numpy as np
import customtkinter
import threading
import time

# -------- LOADING SREEN --------------

def task():
    # The window will stay open until this function call ends.
    time.sleep(1)
    root.destroy()

WIDTH_GUI_LOADING = 600
HEIGHT_GUI_LOADING = 400

root = customtkinter.CTk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width/2) - (WIDTH_GUI_LOADING/2))
y_cordinate = int((screen_height/2) - (HEIGHT_GUI_LOADING/2))
customtkinter.set_appearance_mode('light') #SYSTEM,Dark,Light

root.geometry("{}x{}+{}+{}".format(WIDTH_GUI_LOADING,HEIGHT_GUI_LOADING,x_cordinate,y_cordinate))
root.overrideredirect(True)

#Draw from here
logo_bme = ImageTk.PhotoImage(Image.open('logo_bme.png').resize((100, 100), Image.Resampling.LANCZOS))
label_logo_bme = customtkinter.CTkLabel(master=root)
label_logo_bme.grid(row=0, column=0)
label_logo_bme.place(relx=0.4, rely=0.2,anchor='center')
label_logo_bme.configure(image=logo_bme)

logo_app = ImageTk.PhotoImage(Image.open('happy_large.png').resize((100, 100), Image.Resampling.LANCZOS))
label_logo_app = customtkinter.CTkLabel(master=root)
label_logo_app.grid(row=0, column=0)
label_logo_app.place(relx=0.6, rely=0.2,anchor='center')
label_logo_app.configure(image=logo_app)

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
HEIGHT_GUI = 400

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
def CLAHE(img,slipslim):
    """
    It takes an image, converts it to the LAB color space, splits the channels, applies CLAHE to the L
    channel, merges the channels back together, and converts the image back to BGR
    
    :param img: BGR
    :param slipslim: The limit for contrast limiting. The higher the limit, the more contrast will be
    limited
    :return: The enhanced image.
    """
    '''
    sliplim Double
    img: BGR
    return BGR
    '''
    lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)
    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv2.createCLAHE(clipLimit=slipslim, tileGridSize=(4,4)) #FIXME:
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl,a,b))

    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    return enhanced_img

def change_brightness(img, value=30):
    """
    It takes an image, converts it to HSV, increases the value channel by 30, and then converts it back
    to BGR
    
    :param img: BGR
    :param value: inc/dec brightness, defaults to 30 (optional)
    :return: the image with the brightness changed.
    """
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
    """
    If the file doesn't exist, create it and write the info to it. If it does exist, just write the info
    to it
    
    :param name_info: the name of the patient
    :param gender_info: the gender of the patient
    :param age_info: the age of the patient
    """
    '''
    Appear patient_info.txt is not exist, then eppend info to the file 
    '''
    global save_button
    path_save = 'patient_info.txt'
    save_button.configure(text='Saved!')

    cb = name_info + '-' + gender_info + '-' + age_info

    with open(path_save, 'a') as f: # 
        f.write(f'\n{cb}')
    
def mask_ori(image_ori,image_gray,scale_rad=50,shape='circle',run=0):
    """
    It takes an image and a mask, and returns the image with the mask applied
    
    :param image_ori: The original image in RGB format
    :param image_gray: BGR
    :param scale_rad: The radius of the circle, defaults to 50 (optional)
    :param shape: 'circle', 'fill', 'rectangle', defaults to circle (optional)
    :param run: the number of pixels to fill in the mask, defaults to 0 (optional)
    :return: The masked image.
    """
    '''
        image_ori:RGB
        image_gray: BGR
        Return: BGR
    '''
    mask = np.zeros(image_ori.shape[:2], dtype="uint8")
    
    if shape == 'circle':
        y_centroid = mask.shape[0] // 2
        x_centroid = mask.shape[1] // 2
        if run < y_centroid - scale_rad:
            radius = run
        else:
            radius = y_centroid - scale_rad
        cv2.circle(mask, (x_centroid, y_centroid), radius, 255, -1,lineType=cv2.LINE_AA)
    elif shape == 'fill':
        cv2.rectangle(mask,(0,0),(run,mask.shape[0]),255,-1,lineType=cv2.LINE_AA)
    else:
        x_l = (mask.shape[1] // 2) // 6
        y_l = (mask.shape[0] // 2) // 6
        x_r = (mask.shape[1] // 2) + ((mask.shape[1] // 2) - (mask.shape[1] // 2) // 6)
        y_r = (mask.shape[0] // 2) + ((mask.shape[0] // 2) - (mask.shape[0] // 2) // 6)
        cv2.rectangle(mask,(x_l,y_l),(x_r,y_r),255,-1,lineType=cv2.LINE_AA)

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

logo_bme = ImageTk.PhotoImage(Image.open('logo_bme.png').resize((40, 40), Image.Resampling.LANCZOS))
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
exit_button.grid(row=30, column=0, pady=20, padx=10,sticky='w')

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
    """
    It sets the global variable is_running to False, and then destroys the root window
    """
    # root.after(20)
    global is_running
    time.sleep(1)
    is_running = False
    videoloop_stop[0] = False
    root.destroy()

def disable_envent():
    pass

is_running = True
root.protocol("WM_DELETE_WINDOW",disable_envent)

first = customtkinter.CTkLabel(master=root.frame_right,text="A product detect carries early from infrared light by processing image \n Author: Eng.Nguyen Dac Can \n from biomedical engineering department",text_font=("Roboto Bold", -12))
first.grid(row=0, column=0)
first.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

flip_h_c = 1
flip_v_c = 0
apply_his_eq = False
apply_de_eh = False
ct_1_c = True
ct_2_c = False
# -----------------------------
def start__(mirror=False):
        """
        It starts the camera and displays the video feed in the right frame.
        
        :param mirror: If True, the image will be flipped horizontally, defaults to False (optional)
        """
        button1.destroy()
        first.destroy()
        save_button.destroy()
        patient_name.destroy()
        entry_name.destroy()
        patient_gender.destroy()
        entry_gender.destroy()
        patient_age.destroy()
        entry_age.destroy()
        exit_button.destroy()
        label_logo_bme.destroy()
        input_user.destroy()

        # Appear some button for camera
        global snap_button
        global button2
        global slider_brightness
        global bA
        global h_flip
        global v_flip
        global heq
        global dteh
        global ct_1
        global ct_2
        global dn_1
        global dn_2
        global option_

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
        snap_button.grid(row=11, column=0, pady=10, padx=10,sticky='w')

        option_ = customtkinter.CTkOptionMenu(master=root.frame_left,
                                                        values=["none","circle", "retangle","fill"],text_font=("Roboto Medium", -12),
                                                        command=shape_f)
        option_.grid(row=12, column=0)

        h_flip = customtkinter.CTkSwitch(master=root.frame_left
                                        ,text='horizontalFlip'
                                        ,text_font=("Roboto Medium", -12)
                                        ,command=flip_h)
        h_flip.grid(row=16, column=0,sticky='w')

        v_flip = customtkinter.CTkSwitch(master=root.frame_left
                                        ,text='verticalFlip'
                                        ,text_font=("Roboto Medium", -12)
                                        ,command=flip_v)
        v_flip.grid(row=17, column=0,sticky='w')

        bA = customtkinter.CTkLabel(master=root.frame_left,
                                        text="brightnessAdjust:",
                                        text_font=("Roboto Medium", -12))  # font name and size in px
        bA.grid(row=13, column=0)

        slider_brightness = customtkinter.CTkSlider(master=root.frame_left,
                                                from_=-150,
                                                to=100,
                                                number_of_steps=50,
                                                width=150
                                                )
        slider_brightness.grid(row=14, column=0)
        slider_brightness.set(0)

        heq = customtkinter.CTkSwitch(master=root.frame_left
                                        ,text='histogramEqual'
                                        ,text_font=("Roboto Medium", -12)
                                        ,command=heq_f)
        heq.grid(row=18, column=0,sticky='w')

        dteh = customtkinter.CTkSwitch(master=root.frame_left
                                        ,text='detailEnhance'
                                        ,text_font=("Roboto Medium", -12)
                                        ,command=dteh_f)
        dteh.grid(row=20, column=0,sticky='w')

        ct_1 = customtkinter.CTkSwitch(master=root.frame_left
                                        ,text='contrast_1'
                                        ,text_font=("Roboto Medium", -12)
                                        ,command=ct_1_f,check_state=True)
        ct_1.grid(row=19, column=0,sticky='w')


        ct_2 = customtkinter.CTkSwitch(master=root.frame_left
                                        ,text='contrast_2'
                                        ,text_font=("Roboto Medium", -12)
                                        ,command=ct_2_f)
        ct_2.grid(row=25, column=0,sticky='w')

        dn_1 = customtkinter.CTkSwitch(master=root.frame_left
                                        ,text='blackEnhance'
                                        ,text_font=("Roboto Medium", -12)
                                    )
        dn_1.grid(row=26, column=0,sticky='w')

        dn_2 = customtkinter.CTkSwitch(master=root.frame_left
                                        ,text='deNoise_2'
                                        ,text_font=("Roboto Medium", -12)
                                        )
        dn_2.grid(row=28, column=0,sticky='w')

        global gray_3
        global lb
        global slipslim_1
        global lfps
        global nlb
        global shift

        lb = customtkinter.CTkLabel(master=root.frame_left,
                                    text="clipLimit:",
                                    text_font=("Roboto Medium", -10))  # font name and size in px
        lb.grid(row=30, column=0)
        slipslim_1 = customtkinter.CTkSlider(master=root.frame_left,
                                            from_=0,
                                            to=30,
                                            number_of_steps=30,
                                            width=150
                                            )
        slipslim_1.grid(row=31, column=0)
        slipslim_1.set(4)


        lfps = customtkinter.CTkLabel(master=root.frame_left,
                                    text="FPS",
                                    height=10,
                                    text_font=("Roboto Bold", -14))  # font name and size in px
        lfps.grid(row=32, column=0)
        nlb = customtkinter.CTkLabel(master=root.frame_left,
                                    text='30',
                                    height=10,
                                    text_font=("Roboto Medium", -12))  # font name and size in px
        nlb.grid(row=33, column=0)
        
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360) #1080, 720, 360
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) #1920, 1280, 640
        # cap.set(cv2.CAP_PROP_FPS, 15)

        pre_image = cap.read()[1]

        cam = customtkinter.CTkLabel(master=root.frame_right,text="Loading Camera....",text_font=("Roboto Bold", -12))
        cam.grid(row=0, column=0)
        cam.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        cam.pack(expand=True,fill=tk.BOTH)
        
        time_i = time.time()
        time_h = time.time()
        shift = 0
        kernel = np.ones((5,5),np.uint8)

        while is_running:

            if videoloop_stop[0]:
                videoloop_stop[0] = False
                cam.destroy()
                break
            # time.sleep(0.05)
            # Get the latest frame and convert into Image
            image= cap.read()[1]
            difference = cv2.subtract(image, pre_image)
            b, g, r = cv2.split(difference)
            

            if (cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0) or (np.mean(image)==255):
                time_i=time.time()
                pass
            else:
                # print(1)
                pre_image=image
                # Flip the image
                if flip_h_c == 1:
                    if flip_v_c == 0:
                        flip = cv2.flip(image, 1)
                    else:
                        flip = cv2.flip(image, 1)
                        flip = cv2.flip(image, 0)
                if flip_h_c == 0:
                    if flip_v_c == 1:
                        flip = cv2.flip(image, 0)
                    else:
                        flip = image
                
                ori = cv2.cvtColor(flip, cv2.COLOR_BGR2RGB)
                # Decreare brightness before contrast
                brightness = change_brightness(flip,value=slider_brightness.get()) #FIXME:

                # apply histogram equalization
                if apply_his_eq:
                    brightness = cv2.cvtColor(brightness, cv2.COLOR_BGR2GRAY)
                    brightness = cv2.equalizeHist(brightness)
                    brightness = cv2.cvtColor(brightness, cv2.COLOR_GRAY2BGR)
                
                # Contrast
                if ct_1_c:
                    brightness = CLAHE(brightness,slipslim_1.get())

                if apply_de_eh:
                    enhance = cv2.detailEnhance(brightness, sigma_s=10, sigma_r=0.15)
                else:
                    enhance = brightness
                
                if ct_2_c:
                    enhance = CLAHE(enhance,slipslim_1.get())
                
                if dn_1.get() == 1:
                    # denoised = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
                    erosion = cv2.erode(enhance,kernel,iterations = 1)
                else:
                    erosion=enhance
                
                if dn_2.get() == 1:
                    # median = cv2.medianBlur(smooth, 5)
                    # gaussian = cv2.GaussianBlur(median, (5, 5), 0)
                    # kernel3 = np.ones((5,5),np.float32)/25
                    # denoise = cv2.filter2D(gaussian, cv2.CV_8UC3, kernel3)
                    denoise = cv2.bilateralFilter(erosion,9,75,75)
                else:
                    denoise = erosion

                # Grayscale
                gray_1 = cv2.cvtColor(denoise, cv2.COLOR_BGR2GRAY) #gray 1 chanel
                gray_3 = cv2.cvtColor(gray_1, cv2.COLOR_GRAY2BGR) #gray 3 chanel

                

                # Mask
                
                if shift < ori.shape[1]:
                    shift += 5
                
                if option_.get() != 'none':
                    final = mask_ori(ori,gray_3,scale_rad=5,shape=option_.get(),run=shift)
                else:
                    final = ori

                #Array to Image
                img = Image.fromarray(final)

                # Convert image to PhotoImage
                imgtk = ImageTk.PhotoImage(image = img)
                # cam.imgtk = imgtk
                cam.configure(image=imgtk) #Set width and height of camera
                cam.image = imgtk

                time_o = time.time() - time_i
                fps_ =round(1 / time_o)
                if fps_ > 10:
                    fps = fps_ - (fps_ % 5)

                time_i = time.time()
                if time_i - time_h > 1:
                    time_h = time_i
                    nlb.configure(text=str(fps))
                
    
def button1_clicked(videoloop_stop):
    """
    It starts a thread that runs the function start__, which is a function that runs a loop that plays a
    video
    
    :param videoloop_stop: This is a boolean variable that is used to stop the video loop
    """
    global entry_name
    global entry_gender
    global entry_age
    # global first
    if entry_name.get() == "" or entry_gender.get() == "" or entry_age.get() == 0:
        first.configure(text_color='red')
        first.configure(text='PLEASE, FULLFILL INFORMATION!!!')
    else:
        thread = threading.Thread(target=start__, args=(videoloop_stop,))
        thread.start()

def button2_clicked(videoloop_stop):
    """
    It destroys all the widgets in the first window and creates new widgets in the second window
    
    :param videoloop_stop: a list of one element, which is a boolean
    """
    global button1
    global save_button
    global patient_name
    global entry_name
    global patient_gender
    global entry_gender
    global patient_age
    global entry_age
    global exit_button
    global label_logo_bme
    global input_user

    bA.destroy()
    snap_button.destroy()
    option_.destroy()
    button2.destroy()
    slider_brightness.destroy()
    h_flip.destroy()
    v_flip.destroy()
    heq.destroy()
    dteh.destroy()
    ct_1.destroy()
    ct_2.destroy()
    dn_1.destroy()
    dn_2.destroy()
    nlb.destroy()
    lfps.destroy()

    if ct_1_c == True:
        lb.destroy()
        slipslim_1.destroy()

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
    button1 = customtkinter.CTkButton(master=root.frame_left,
                                        text="Start",
                                        command = lambda: button1_clicked(videoloop_stop),
                                        text_font=("Roboto Bold", -12),
                                        fg_color="#94B49F",
                                        text_color='white')
    button1.grid(row=9, column=0, pady=10, padx=10,sticky='w')
    save_button = customtkinter.CTkButton(master=root.frame_left,
                                        text="Save",
                                        command = lambda: save_info(entry_name.get(),entry_gender.get(),entry_age.get()),
                                        text_font=("Roboto Bold", -12))
    save_button.grid(row=8, column=0, pady=10, padx=10,sticky='w')

    exit_button = customtkinter.CTkButton(master=root.frame_left,
                                        text="Exit",
                                        command= lambda: on_closing(),
                                        text_font=("Roboto Bold", -12),
                                        fg_color="#F54040")
    exit_button.grid(row=30, column=0, pady=20, padx=10,sticky='w')



    videoloop_stop[0] = True

def save_picture():
    """
    It saves the image in a folder called image_save, and then destroys the window
    """
    image_name = "IMG-" + time.strftime("%H-%M-%d-%m-%y") + ".jpg"
    path = 'image_save'
    os.makedirs(path,exist_ok=True)
    cv2.imwrite(os.path.join(path,image_name), img_new_win)

    videoloop_stop[0] = False
    new_win.destroy()

def shape_f(mirror):
    """
    If the shift is not zero, set it to zero
    
    :param mirror: The mirror object
    """
    global shift
    if shift != 0:
        shift = 0

def flip_h():
    """
    If the variable flip_h_c is 0, set it to 1. If it's 1, set it to 0
    """
    global flip_h_c
    if flip_h_c == 0:
        flip_h_c = 1
    else:
        flip_h_c = 0
def flip_v():
    """
    If the variable flip_v_c is 0, set it to 1. If it's 1, set it to 0
    """
    global flip_v_c
    if flip_v_c == 0:
        flip_v_c = 1
    else:
        flip_v_c = 0
def heq_f():
    """
    If apply_his_eq is True, set it to False. If apply_his_eq is False, set it to True
    """
    global apply_his_eq
    if apply_his_eq == True:
        apply_his_eq = False
    else:
        apply_his_eq = True
def dteh_f():
    """
    If apply_de_eh is True, set it to False. If apply_de_eh is False, set it to True
    """
    global apply_de_eh
    if apply_de_eh == True:
        apply_de_eh = False
    else:
        apply_de_eh = True
def ct_2_f():
    """
    If the checkbox is checked, then the checkbox is unchecked and the label and slider are destroyed.
    If the checkbox is unchecked, then the checkbox is checked and the label and slider are created.
    """
    global ct_2_c
    global lb
    global slipslim_1
    if ct_2_c == True:
        ct_2_c = False
        if ct_1_c == False:
            lb.destroy()
            slipslim_1.destroy()
    else:
        ct_2_c = True
        if ct_1_c == False:
            lb = customtkinter.CTkLabel(master=root.frame_left,
                                        text="clipLimit:",
                                        text_font=("Roboto Medium", -10))  # font name and size in px
            lb.grid(row=30, column=0)
            slipslim_1 = customtkinter.CTkSlider(master=root.frame_left,
                                                from_=0.0,
                                                to=30.0,
                                                number_of_steps=30,
                                                width=150
                                                )
            slipslim_1.grid(row=31, column=0)
            slipslim_1.set(3.0)
def ct_1_f():
    """
    If the checkbox is checked, then the checkbox is unchecked, and if the checkbox is unchecked, then
    the checkbox is checked.
    """
    global ct_1_c
    global lb
    global slipslim_1
    if ct_1_c == True:
        ct_1_c = False
        if ct_2_c == False:
            lb.destroy()
            slipslim_1.destroy()
    else:
        ct_1_c = True
        if ct_2_c == False:
            lb = customtkinter.CTkLabel(master=root.frame_left,
                                        text="clipLimit:",
                                        text_font=("Roboto Medium", -10))  # font name and size in px
            lb.grid(row=30, column=0)
            slipslim_1 = customtkinter.CTkSlider(master=root.frame_left,
                                                from_=0.0,
                                                to=30.0,
                                                number_of_steps=30,
                                                width=150
                                                )
            slipslim_1.grid(row=31, column=0)
            slipslim_1.set(3.0)

def snap_shot():
    """
    It creates a new window, displays an image, and has two buttons.
    """
    global new_win
    global img_new_win
    new_win = customtkinter.CTkToplevel()

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