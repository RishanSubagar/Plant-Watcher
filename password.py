from tkinter import *
import RPi.GPIO as GPIO
from matplotlib.pyplot import text
from mfrc522 import SimpleMFRC522
import time

reader = SimpleMFRC522()

def id_scan():
    try:
        id, text = reader.read()
        print(id)
        print(text)

        if str(id) == "634214288427":
            root.destroy()
        else:
            pass_msg.config(text="Invalid ID.", fg="red", bg="whitesmoke")
            pass_msg.place(x=120, y=110)

    finally:
        GPIO.cleanup()


def destroy_win():
    if pass_val.get() == "password":
        root.destroy()
    else:
        pass_msg.config(text="Incorrect. Try Again.", fg="red", bg="whitesmoke")
        pass_msg.place(x=120, y=110)

# Create window
root = Tk()
root.title("Enter Password")
root.geometry("400x200")
root.resizable(False, False)
root.config(bg="#2e2e2e")

# Labels
enter_text = Label(root, text=' Scan ID or Enter Password ', font=30, justify="center", bg="whitesmoke", fg="black")
enter_text.pack(pady=10, anchor=N)

password = Label(root, text='Password:', font=30, justify="center", bg="#2e2e2e", fg="whitesmoke")
password.place(x=50, y=70)

pass_msg = Label(root, font=30, justify="center")

# Entry box
pass_val = StringVar()

pass_entry = Entry(root, textvariable=pass_val, bg="whitesmoke", fg="black", show="*", width=15)
pass_entry.place(x=140, y=70)

# Button
enter = Button(root, text='Enter', command=destroy_win)
enter.place(x=300, y=70)

enter_id = Button(root, text='Use ID', command=id_scan)
enter_id.place(x=170, y=140)


root.mainloop()
