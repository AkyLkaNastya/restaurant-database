from tkinter import *
from tkinter import ttk
 
root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")
root.overrideredirect(True)
 
def dismiss(window):
    window.grab_release() 
    window.destroy()
 
root.protocol("WM_DELETE_WINDOW", lambda: dismiss(root)) # перехватываем нажатие на крестик
close_button = ttk.Button(root, text="X", command=lambda: dismiss(root))
close_button.pack(anchor="e", expand=0)
root.grab_set()       # захватываем пользовательский ввод
 
root.mainloop()