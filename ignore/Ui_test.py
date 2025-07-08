import cv2
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import os
import datetime
from tkinter import filedialog

#ignore this file pls


class WebcamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Webcam Capture")
        self.root.geometry("800x600")
        self.root.config(bg = "#333")
        self.showing = False
        button_frame = tk.Frame(root, bg="#333")
        
        self.vid = cv2.VideoCapture(0)
        
        self.label = Label(root)
        self.label.pack()
        
        
        self.capture_button = Button(button_frame, text="Capture", command=self.capture_image)
        self.capture_button.pack(side=tk.LEFT, padx=10,pady=20)

        self.import_button = Button(button_frame, text="Import", command=self.import_pic)
        self.import_button.pack(side=tk.LEFT, padx=10,pady=20)

        self.clear_button = Button(button_frame, text="Clear", command=self.clear_image)
        self.clear_button.pack(side=tk.LEFT, padx=10,pady=20)
        button_frame.pack(anchor="center")

        self.update_frame()


    def update_frame(self):
        if not self.showing:
            ret, frame = self.vid.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.label.config(image=self.photo)
        self.root.after(10, self.update_frame)

    def capture_image(self):
        ret, frame = self.vid.read()
        if ret:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")],
                title="Save captured image as..."
            )

            if file_path: 
                cv2.imwrite(file_path, frame)
                print(f"Image saved at {file_path}")

    def import_pic(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image File","*.jpg;*.jpeg;*.png;*.bmp;*.gif")])

        if file_path:
            image = Image.open(file_path).resize((640,480))
            self.photo = ImageTk.PhotoImage(image=image)
            self.label.config(image= self.photo)
            self.showing = True
    
    def clear_image(self):
        self.showing = False

        




if __name__ == "__main__":
    root = tk.Tk()
    app = WebcamApp(root)
    root.mainloop()