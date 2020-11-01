from tkinter import Tk,ttk,filedialog,BooleanVar, Toplevel, TOP,BOTH, Label
from PIL import Image, ImageTk
import random
import os
import sys
import csv

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Root(Tk):
    def __init__(self):
        super(Root,self).__init__()
        self.title("Main")
        self.style = ttk.Style()
        self.style.configure(
            'JK.TLabelframe',borderwidth=0,highlightthickness=0
        )
        self.button()
        ### Image selection ###
        self.imgH = 512
        self.imgW = 512
        self.images_count = len(os.listdir(resource_path('images\\real\\'))) + len(os.listdir(resource_path('images\\fake\\')))
        self.images_n = 0 # total images shown
        self.c_image = None # is current image real or fake
        self.TP = 0
        self.FP = 0
        self.TN = 0
        self.FN = 0
        self.real = os.listdir(resource_path('images\\real\\'))
        self.fake = os.listdir(resource_path('images\\fake\\'))
        self.individual_items = [] # To be filled with answers
        #print(self.real)
        #print(self.fake)


    
    def button(self):
        self.button = ttk.Button(self,text="Start",command=self.start_study,width=16)
        self.button.grid(row = 1,padx=200,pady=200)

    
    def start_study(self):
        #print("start")
        self.button.destroy()
        """
        first_image = Image.open()
        first_image = first_image.resize((250,250),Image.ANTIALIAS)
        first_image = ImageTk.PhotoImage(first_image)
        """
        first_image = self.pick_img()
        self.img = Label(self,image=first_image)
        self.img.image = first_image # keep reference
        self.img.pack()
        self.realB = ttk.Button(self,text="Real",command=self.push_real,width=16)
        self.realB.pack(pady=10)
        self.fakeB = ttk.Button(self,text="Fake",command=self.push_fake,width=16)
        self.fakeB.pack(pady=10)

    def pick_img(self):
        p = random.random() # float 0-1
        if self.images_n < self.images_count:
            if (p > 0.5 and len(self.real)) or len(self.fake) == 0:
                index = random.randint(0,len(self.real)-1)
                #print(index,len(self.real))
                self.individual_items.append([str(self.real[index]),"real"]) # prepare new row for results
                img_path = resource_path("images\\real\\" + str(self.real[index]))
                #print(img_path)
                self.images_n += 1 # total images counter
                self.c_image = True # current image is a real one
                del self.real[index]
                #print(self.real)
            else:
                index = random.randint(0,len(self.fake)-1)
                #print(index,len(self.fake))
                self.individual_items.append([str(self.fake[index]),"fake"]) # prepare new row for results
                img_path = resource_path("images\\fake\\" + str(self.fake[index]))
                #print(img_path)
                self.images_n += 1 # total images counter
                self.c_image = False # current image is a fake one
                del self.fake[index]
                #print(self.fake)

            image = Image.open(img_path)
            #image = image.resize((self.imgW,self.imgH),Image.ANTIALIAS)
            image = ImageTk.PhotoImage(image)
            return image
        else:
            self.c_image = None
            self.realB.destroy()
            self.fakeB.destroy()
            self.img.destroy()
            acc = ((self.TP + self.TN) / (self.TP + self.TN + self.FP + self.FN)) if (self.TP + self.TN + self.FP + self.FN) else "/"
            S = (self.TP / (self.TP + self.FN)) if (self.TP + self.FN) else "/"
            SP = (self.TN / (self.TN + self.FP)) if (self.TN + self.FP) else "/"
            PPV = (self.TP / (self.TP + self.FP)) if (self.TP + self.FP) else "/"
            NPV = (self.TN / (self.TN + self.FN)) if (self.TN + self.FN) else "/"
            label = "Accuracy = " + str(acc) + "\n" + "Sensitivity = " + str(S) + "\n" + "Specificity = " + str(SP) + "\n" + "PPV = " + str(PPV) + "\n" + "NPV = " + str(NPV) + "\n"
            self.acc_label = Label(self,text=label)
            self.acc_label.pack(padx=250,pady=250)
            #print("### ACCURACY: ###")
            #print(acc)
            with open("results.csv","w",newline="") as csvfile:
                writer = csv.writer(csvfile,delimiter=",")
                writer.writerow(["img","value","score"])
                for row in self.individual_items:
                    writer.writerow(row)
            return None


    def push_real(self):
        if self.c_image == True:
            self.TP += 1
            self.individual_items[-1].append(1)
        elif self.c_image == False:
            self.FP += 1
            self.individual_items[-1].append(0)
        next_img = self.pick_img()
        if next_img:
            self.img.configure(image=next_img)
            self.img.image = next_img

    def push_fake(self):
        if self.c_image == False:
            self.TN += 1
            self.individual_items[-1].append(1)
        elif self.c_image == True:
            self.FN += 1
            self.individual_items[-1].append(0)
        next_img = self.pick_img()
        if next_img:
            self.img.configure(image=next_img)
            self.img.image = next_img


if __name__ == "__main__":
    root = Root()
    root.mainloop()
    