import tkinter as tk
from tkinter import ttk
from copy import deepcopy

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

def is_operator(case):
    if(case in ["+","-","*","/"]):
       return True
    return False

need_reset=False

def calculator_text_enter(code, textlabel):
    global need_reset
    if(need_reset and not is_operator(code)):
        textlabel.configure(text="")
    need_reset=False

    value = textlabel.cget("text") 
    match str(code):
        case "ENTER":
            need_reset = True
            try:
                textlabel.configure(text=eval(value))
            except ZeroDivisionError as e:
                textlabel.configure(text="--ERROR--\nDIVIDE BY ZERO")
            except:
                textlabel.configure(text="--SYNTAX ERROR--")
        case "CLR":             
            need_reset = False
            textlabel.configure(text="")
        case _:
            value = f"{value}{code}" 
            textlabel.configure(text=value)
             
    print(code)

def main():
## CONFIG INIT

    
    _size_configs = {
        "frame_width"       : 410,
        "frame_height"      : 460,
        "num_width"         : 6,
        "num_height"        : 3,
        "num_bordersize"    : 100,
        "num_borderwidth"   : 2,
        "num_font_size"     : 12,
        "display_font_size" : 18

    }



    frame_color         = "#283A44"
    display_color       = "black"
    display_text_color  = "white"
    num_color           = "white"
    num_decimal_color   = "white"
    operator_color      = "#5F94A4"
    enter_button_color  = "#1D1B2E"

    clear_button_color  = "#1D1B2E"


    
## GUI INIT

    root = tk.Tk()
    root.resizable(False,False)
    root.geometry(f"{_size_configs["frame_width"]}x{_size_configs["frame_height"]}")

    

    display_frame = tk.Frame(root, height=100, width=_size_configs["frame_width"], bg=display_color)
    display_frame.pack_propagate(False)
    display_frame.pack(fill=tk.X)

    label_text = tk.StringVar()
    label_text.set("")
    display_label = tk.Label(display_frame,
                             anchor=tk.CENTER, 
                             borderwidth=0, 
                             fg=display_text_color, 
                             bg=display_color, 
                             text=label_text.get(), 
                             font=("Helvetica", _size_configs["display_font_size"]))
    display_label.pack_propagate(False)
    display_label.pack(fill=tk.BOTH)

    keypad_frame = tk.Frame(root, height=_size_configs["frame_height"], width=_size_configs["frame_width"])
    keypad_frame.pack_propagate(False)
    keypad_frame.pack()

    keypad_layout = [
        [7, 8, 9, "+", "CLR"],
        [4, 5, 6, "-"],
        [1, 2, 3, "*", "ENTER"],
        [0, -1, ".", "/"]
    ]

    keypad_buttons = []


    for i in range(len(keypad_layout)):
        temp = {}
        for j in range(len(keypad_layout[i])):
            if keypad_layout[i][j] == -1:
                continue
            
            buttontext = str(keypad_layout[i][j])
            button = (tk.Button(keypad_frame,
                                text=buttontext,
                                width=_size_configs["num_width"],
                                height=_size_configs["num_height"],
                                bg=num_color,
                                bd=_size_configs["num_borderwidth"],
                                command=lambda j=buttontext: calculator_text_enter(j, display_label)
                                ))
            button.config(font=("Helvetica",16))
            temp[str(buttontext)] = button

        keypad_buttons.append(temp)

    for i in range(len(keypad_layout)):
        for j in range(len(keypad_layout[i])):
            if keypad_layout[i][j] == -1:
                continue
            key = str(keypad_layout[i][j])
            keypad_buttons[i][key].grid(row=i, column=j)

    for i in range(len(keypad_layout)):
        keypad_buttons[i].get(keypad_layout[i][3]).configure(bg=operator_color)

    print(keypad_buttons[3][str(0)])

    button_zero = keypad_buttons[3].get("0")
    button_enter = keypad_buttons[2].get("ENTER")
    button_clr = keypad_buttons[0].get("CLR")
    button_decimal = keypad_buttons[3].get(".")

    button_zero.grid(row=3,column=0,columnspan=2, sticky="nsew")
    button_enter.grid(row=2, column=4, rowspan=2, sticky="nsew")
    button_clr.grid(row=0,column=4, rowspan=2, sticky="nsew")
        
    button_enter.configure(bg=enter_button_color, fg="white")
    button_clr.configure(bg=clear_button_color, fg="white")
    button_decimal.configure(bg=num_decimal_color)

    root.mainloop()
 
if __name__ == "__main__":
    main()
