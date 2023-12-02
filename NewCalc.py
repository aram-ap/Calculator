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


class Calculator:

    def __init__(self):
        self._val = 0
        self._actions = []
        pass

    def get_result_value(self):
        return self._val

    def set_actions_by_string(self, param):
        param.replace(" ", "")
        self._actions = param.split(",")
        return param



    def string_to_num(self, str):
        return float(str)

    def clear_all(self):
        self._val = 0
        self._actions = []

    def do_calculation(self, case, num):
        temp = self._val

        match case:
            case "+":  # ADDITION
                self._val += num
            case "-":  # SUBTRACTION
                self._val -= num
            case "*":  # MULTIPLICATION
                self._val *= num
            case "/":  # DIVISION
                if (num == 0):
                    self.val = -1
                else:
                    self._val /= num

    def execute_calculation(self, str):
        self._actions = self.set_actions_by_string(str)

        for i in range(len(self._actions)):
            item = self._actions[i]

            if (item.isnumeric()) and i == 0:
                self._val += self.string_to_num(item)

            else:
                if (i + 1 in range(len(self._actions))):
                    self.do_calculation(item, self.string_to_num(self._actions[i + 1]))
                else:
                    self.do_calculation(item, 0)


def command(d):
    print(d)

def main():
## CALCULATOR INIT
    c = Calculator()

## CONFIG INIT
    frame_width = 500

    num_width = 7
    num_height = num_width
    num_borderwidth = 1
    num_bordersize = 100

    frame_color         = "white"
    display_color       = "black"
    display_text_color  = "white"
    num_color           = "white"
    num_decimal_color   = "white"
    operator_color      = "#283A44"
    enter_button_color  = "#CFEBF3"
    clear_button_color  = "#1D1B2E"

    ttk.Style().configure('operators', background="#283A44")


## GUI INIT

    root = tk.Tk()
    root.resizable(False,False)
    root.geometry(f"{frame_width}x600")


    display_frame = tk.Frame(root, height=100, width=frame_width, bg=display_color)
    display_frame.pack_propagate(False)
    display_frame.pack(fill=tk.X)

    display_label = tk.Label(display_frame,anchor=tk.CENTER, borderwidth=0, fg=display_text_color)

    keypad_frame = tk.Frame(root, height=500, width=frame_width)
    # keypad_frame.grid_propagate(False)
    keypad_frame.pack_propagate(False)
    keypad_frame.pack()

    keypad_layout = [
        [7, 8, 9, "+", "ENTER"],
        [4, 5, 6, "-"],
        [1, 2, 3, "*", "CLR"],
        [0, -1, ".", "/"]
    ]

    keypad_buttons = []

    for i in range(len(keypad_layout)):
        temp = {}
        for j in range(len(keypad_layout[i])):
            if keypad_layout[i][j] == -1:
                continue

            button = (tk.Button(keypad_frame,
                                text=keypad_layout[i][j],
                                width=num_width,
                                height=num_height,
                                bg=num_color,
                                bd=num_borderwidth,
                                command=lambda j=keypad_layout[i][j]: command(j)
                                ))
            temp[str(keypad_layout[i][j])] = button
        keypad_buttons.append(temp)

    for i in range(len(keypad_layout)):
        for j in range(len(keypad_layout[i])):
            if keypad_layout[i][j] == -1:
                continue
            key = str(keypad_layout[i][j])
            keypad_buttons[i][key].grid(row=i, column=j)

    print(keypad_buttons[3][str(0)])

    button_zero = keypad_buttons[3].get("0")
    button_enter = keypad_buttons[0].get("ENTER")
    button_clr = keypad_buttons[2].get("CLR")


    button_zero.grid(row=3,column=0,columnspan=2, sticky="nsew")
    button_enter.grid(row=0, column=4, rowspan=2, sticky="nsew")
    button_clr.grid(row=2,column=4, rowspan=2, sticky="nsew")

    button_enter.configure(highlightbackground=operator_color)
    button_clr.configure(highlightbackground=operator_color)

    # keypad_buttons[3][button_decimal_key].grid(row=3,column=2, sticky="nsew")
    root.mainloop()
    # main frame

    # frame = tk.Frame(root, width=50,height=700, background="blue")
    # frame.pack_propagate(False)






    # frame.pack()
    #
    # digit_box = tk.Frame(frame, background="black", width=50,height=50)
    # digit_box.pack_propagate(False)
    # digit_box.pack()
    #
    # textBox = tk.Label(digit_box,text="1+1",background="black", font=10,fg='white')
    # textBox.grid(row=0,column=0)
    # textBox.pack_propagate(False)
    # textBox.pack()
    #
    # btn_seven = tk.Button(frame, text="7", width=5, background="white")
    # btn_seven.grid(row=1, column=0, padx=5, pady=10)
    # btn_seven.pack(fill="both")
    #
    #
    # btn_eight = tk.Button(frame, text="8", width=5, background="white")
    # btn_eight.grid(row=1, column=1, padx=5, pady=10)
    # btn_eight.pack(fill="both")
    #
    # btn_nine = tk.Button(frame, text="9", width=5, background="white")
    # btn_nine.grid(row=1, column=2, padx=5, pady=10)
    # btn_nine.pack(fill="both")
    #
    # btn_four= tk.Button(frame,text="4", width=5, background="white")
    # btn_four.grid(row=2,column=0, padx=5, pady=10)
    # btn_four.pack(fill="both")
    #
    # btn_five= tk.Button(frame,text="5", width=5, background="white")
    # btn_five.grid(row=2,column=1, padx=5, pady=10)
    # btn_five.pack(fill="both")
    #
    # btn_six = tk.Button(frame,text="6", width=5, background="white")
    # btn_six.grid(row=2,column=2, padx=5, pady=10)
    # btn_six.pack(fill="both")
    #
    #
    #
    # btn = RoundedButton(frame,text="Button", radius=100,btnbackground="gray", btnforeground="white", clicked=func)
    # btn.grid(row=1,column=0)
    # btn.pack(expand=False,fill="both")

    # btn = RoundedButton(text="This is a \n rounded button", radius=1000, btnbackground="#0078ff", btnforeground="#ffffff", clicked=func)
    # btn.pack(expand=True, fill="both")


if __name__ == "__main__":
    main()
