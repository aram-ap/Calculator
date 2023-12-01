import tkinter as tk

class RoundedButton(tk.Canvas):

    def __init__(self, master=None, text:str="", radius=25, btnforeground="#000000", btnbackground="#ffffff", clicked=None, *args, **kwargs):
        super(RoundedButton, self).__init__(master, *args, **kwargs)
        self.config(bg=self.master["bg"])
        self.btnbackground = btnbackground
        self.clicked = clicked

        self.radius = radius        
        
        self.rect = self.round_rectangle(0, 0, 0, 0, tags="button", radius=radius, fill=btnbackground)
        self.text = self.create_text(0, 0, text=text, tags="button", fill=btnforeground, font=("Times", 30), justify="center")

        self.tag_bind("button", "<ButtonPress>", self.border)
        self.tag_bind("button", "<ButtonRelease>", self.border)
        self.bind("<Configure>", self.resize)
        
        text_rect = self.bbox(self.text)
        if int(self["width"]) < text_rect[2]-text_rect[0]:
            self["width"] = (text_rect[2]-text_rect[0]) + 10
        
        if int(self["height"]) < text_rect[3]-text_rect[1]:
            self["height"] = (text_rect[3]-text_rect[1]) + 10
          
    def round_rectangle(self, x1, y1, x2, y2, radius=25, update=False, **kwargs): # if update is False a new rounded rectangle's id will be returned else updates existing rounded rect.
        # source: https://stackoverflow.com/a/44100075/15993687
        points = [x1+radius, y1,
                x1+radius, y1,
                x2-radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1]

        if not update:
            return self.create_polygon(points, **kwargs, smooth=True)
        
        else:
            self.coords(self.rect, points)

    def resize(self, event):
        text_bbox = self.bbox(self.text)

        if self.radius > event.width or self.radius > event.height:
            radius = min((event.width, event.height))

        else:
            radius = self.radius

        width, height = event.width, event.height

        if event.width < text_bbox[2]-text_bbox[0]:
            width = text_bbox[2]-text_bbox[0] + 30
        
        if event.height < text_bbox[3]-text_bbox[1]:  
            height = text_bbox[3]-text_bbox[1] + 30
        
        self.round_rectangle(5, 5, width-5, height-5, radius, update=True)

        bbox = self.bbox(self.rect)

        x = ((bbox[2]-bbox[0])/2) - ((text_bbox[2]-text_bbox[0])/2)
        y = ((bbox[3]-bbox[1])/2) - ((text_bbox[3]-text_bbox[1])/2)

        self.moveto(self.text, x, y)

    def border(self, event):
        if event.type == "4":
            self.itemconfig(self.rect, fill="#d2d6d3")
            if self.clicked is not None:
                self.clicked()

        else:
            self.itemconfig(self.rect, fill=self.btnbackground)

def func():
    print("Button pressed")


def main():
    root = tk.Tk()
    root.resizable(False,False) 
        
    # main frame 

    frame = tk.Frame(root, width=400,height=700, background="blue")
    frame.pack_propagate(False)

    frame.pack()

    digit_box = tk.Frame(frame, background="black", width=400,height=50)
    digit_box.pack_propagate(False)
    digit_box.grid(row=0,column=0,columnspan=4)
    digit_box.pack() 

    textBox = tk.Label(digit_box,text="1+1",background="black", font=10,fg='white')
    textBox.grid(row=0,column=0,columnspan=4)
    textBox.pack()
   
   
    btn_four= RoundedButton(frame,text="4",radius=45,btnbackground="gray",btnforeground="white")
    btn_four.grid(row=2,column=0, padx=5, pady=10)
    btn_four.pack(fill="both")
   
    btn_five= RoundedButton(frame,text="5",radius=45,btnbackground="gray",btnforeground="white")
    btn_five.grid(row=2,column=1, padx=5, pady=10)
    btn_five.pack(fill="both")

    btn_six = RoundedButton(frame,text="6",radius=45,btnbackground="gray",btnforeground="white")
    btn_six.grid(row=2,column=2, padx=5, pady=10)
    btn_six.pack(fill="both")
     
    btn_seven = RoundedButton(frame,text="7",radius=45,btnbackground="gray",btnforeground="white")
    btn_seven.grid(row=1,column=0, padx=5, pady=10)
    btn_seven.pack(fill="both")

    btn_eight= RoundedButton(frame,text="8",radius=45,btnbackground="gray",btnforeground="white")
    btn_eight.grid(row=1,column=1, padx=5, pady=10)
    btn_eight.pack(fill="both")

    btn = RoundedButton(frame,text="Button", radius=100,btnbackground="gray", btnforeground="white", clicked=func)
    btn.grid(row=1,column=0)
    btn.pack(expand=True,fill="both")

    # btn = RoundedButton(text="This is a \n rounded button", radius=1000, btnbackground="#0078ff", btnforeground="#ffffff", clicked=func)
    # btn.pack(expand=True, fill="both")


    root.mainloop()
if __name__ == "__main__":
    main()
