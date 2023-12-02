import tkinter as tk


_val = 0
_actions = []

class Calculator:

    def __init__(self):
        pass
        

    def val(self):
        return _val

    def breakString(self, str):
        str.replace(" ", "")
        global _actions
        _actions = str.split(",")
        return str

    def stringToNum(self, str):
        return float(self)


    def clear(self):
        global _val
        global _actions
        _val = 0
        _actions = []

    def calc(self, case, num ):
        global _val

        temp = _val
        
        match case:
            case "+":                 #ADDITION
                _val += num 
            case "-":                 #SUBTRACTION
                _val -= num
            case "*":                 #MULTIPLICATION
                _val *= num
            case "/":                 #DIVISION
                if(num==0):
                    val = -1
                else:
                    _val /= num

    

    def executeCalculation(self, str):
        global _val
        global _actions

        _actions = self.breakString(str)

        for i in range(len(_actions)):
            item = _actions[i]
            
            if(item.isnumeric()) and i == 0:    
                _val += self.stringToNum(item)
                
            else:
                if(i + 1 in range(len(_actions))):
                    self.calc(item, self.stringToNum(_actions[i+1]))
                else:
                    self.calc(item, 0)


def main():


    #INITIALIZE WINDOW
    #INITIALIZE GRID
    #INIT BUTTONS + LABELS

    root = tk.Tk()
    root.configure(background="white")

    #root.resizable(False, False)
##    canvas = tk.Canvas(root, width=300, height=400, background="white")
##    canvas.pack()

    frame = tk.Frame(root, width=400,height=400,background="white")
    frame.pack_propagate(False)

    frame.grid_propagate(False)
    
##    button_labels = ["1","2","3"]
##
##    
##    buttons = []
##
##    
##    for i in range(len(button_labels)):
##        buttons.append(tk.Button(frame,text=button_labels[i], width=10))
##
##        
##    for i in range(len(buttons)):
##        buttons[i].grid(row=0,column=i, padx=5, pady=5)
##
##    buttons[0].configure(command=lambda:print(str(1)))
##    buttons[1].configure(command=lambda:print(str(2)))
##    buttons[2].configure(command=lambda:print(str(3)))
##
##    zero_button = tk.Button(frame,text="0",width=10,bd=0, highlightthickness=0)
##    zero_button.grid(row=1,column=0, columnspan=3, padx=10, pady=10)
##    
##    zero_button['command'] = lambda : print(str(0))

    
    show_pw = [False]
    toggle_show_pw = tk.Button(frame,text='show password', command=lambda: toggle_pw(show_pw))

    username_var = tk.StringVar()
    password_var = tk.StringVar()

    username_label = tk.Label(frame, text="Username")
    password_label = tk.Label(frame, text="Password", height=1)

    username_text = tk.Entry(frame,width=12,textvariable=username_var)
    password_text = tk.Entry(frame,width=12,textvariable=password_var,show="*")
    

    username_label.grid(row=0,column=0, padx=5, pady=10)
    username_text.grid(row=0,column=1, padx=5, pady=10)
    
    username_label.grid(row=0,column=0, padx=5, pady=10)
    username_text.grid(row=0,column=1, padx=5, pady=10)

    password_label.grid(row=1,column=0, padx=5, pady=10)
    password_text.grid(row=1,column=1, padx=5, pady=10)

    toggle_show_pw.grid(row=1,column=2,padx=5,pady=10)
    
    frame.pack()
    username_label.pack()
    password_label.pack()


    

def toggle_pw(param):
    param[0] = not param[0]
    if param[0]:
        password_text.configure(show="")
        toggle_show_pw.configure(text="hide password")
    else:
        password_text.configure(show="*")
        toggle_show_pw.configure(text="show password")



    

if __name__=="__main__":
    main()



