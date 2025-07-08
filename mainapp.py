import cv2
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import os
import datetime
from tkinter import filedialog
from ultralytics import YOLO


class Lung_detect:
    def __init__(self, root):
        self.root = root
        self.root.title("Lung_detect")
        self.root.geometry("800x600")
        self.root.config(bg = "#333")
        self.showing = False
        self.root.iconphoto(False, ImageTk.PhotoImage(file = 'icon.webp') )
        button_frame = tk.Frame(root, bg="#333")
        
        self.vid = cv2.VideoCapture(0)
        AI_model = YOLO('Lungai.pt')
        self.model = AI_model 
        

        
        self.label = Label(root)
        self.label.pack()
        
        #Capture
        self.capture_button = Button(button_frame, text="Capture", command=self.capture_image)
        self.capture_button.pack(side=tk.LEFT, padx=10,pady=20)
        #import
        self.import_button = Button(button_frame, text="Import", command=self.import_pic)
        self.import_button.pack(side=tk.LEFT, padx=10,pady=20)
        #clear
        self.clear_button = Button(button_frame, text="Clear", command=self.clear_image)
        self.clear_button.pack(side=tk.LEFT, padx=10,pady=20)
        button_frame.pack(anchor="center")



        self.update_frame()


    def update_frame(self):
        if not self.showing:
            ret, frame = self.vid.read()
            if ret:
                results = self.model.predict(source=frame, imgsz=640, conf=0.25, verbose=False)
                result = results[0]

                class_ids  = result.boxes.cls.cpu().numpy() if result.boxes else []

                num_NSCLC = 0
                num_SCLC = 0

                for class_id in class_ids:
                    if int(class_id) == 0:
                        num_NSCLC += 1 
                    elif int(class_id) == 1:
                        num_SCLC += 1



                y_pos = 30
                cv2.putText(frame, f"NSCLC: {num_NSCLC}", (10, y_pos),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 87, 255), 2  )
                y_pos += 30
                cv2.putText(frame, f"SCLC: {num_SCLC}", (10, y_pos),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 195, 255), 2  )





                detected_frame = result.plot()
                frame_RGB = cv2.cvtColor(detected_frame, cv2.COLOR_BGR2RGB)
                self.current_frame = Image.fromarray(frame_RGB)
                self.photo = ImageTk.PhotoImage(image=self.current_frame)
                self.label.config(image=self.photo)
        self.root.after(10, self.update_frame)

    def capture_image(self):
        if hasattr(self, 'current_frame') and self.current_frame:
            way_save = "pic"
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(way_save, f"{timestamp}.jpg")

            if file_path: 
                self.current_frame.save(file_path)
                print(f"Image saved at {file_path}")

    def import_pic(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image File","*.jpg;*.jpeg;*.png;*.bmp;*.gif")])

        if file_path:
            image_bgr = cv2.imread(file_path)
            image_resized = cv2.resize(image_bgr, (640, 480))
            results = self.model.predict(source=image_resized, imgsz=640, conf=0.25, verbose=False)
            result = results[0]

            class_ids  = result.boxes.cls.cpu().numpy() if result.boxes else []

            num_NSCLC = 0
            num_SCLC = 0

            for class_id in class_ids:
                if int(class_id) == 0:
                    num_NSCLC += 1 
                elif int(class_id) == 1:
                    num_SCLC += 1



            y_pos = 30
            cv2.putText(image_resized, f"NSCLC: {num_NSCLC}", (10, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 87, 255), 2 )
            y_pos += 30
            cv2.putText(image_resized, f"SCLC: {num_SCLC}", (10, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 195, 255), 2 )


            detected_frame = results[0].plot()

            detected_RGB = cv2.cvtColor(detected_frame, cv2.COLOR_BGR2RGB)
            self.current_frame = Image.fromarray(detected_RGB)  
            self.photo = ImageTk.PhotoImage(image=self.current_frame)
            
            self.label.config(image= self.photo)
            self.showing = True
    
    def clear_image(self):
        self.showing = False

    

        




if __name__ == "__main__":
    root = tk.Tk()
    app = Lung_detect(root)
    root.mainloop()