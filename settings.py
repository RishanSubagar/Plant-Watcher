from tkinter import *

root = Tk()
settings = Toplevel(root, height=300, width=450)
settings.title("Settiings")

bg = "#2e2e2e"
fg= "white"
settings.config(bg=bg)

# Labels
device_lbl = Label(settings, text="Device:", font=24, bg=bg, fg=fg)
device_lbl.place(x=10, y=10)

change_lbl = Label(settings, text="Change:", font=24, bg=bg, fg=fg)
change_lbl.place(x=200, y=10)

temp = Label(settings, text="Temperature", font=24, bg=bg, fg=fg)
temp.place(x=10, y=50)

humid = Label(settings, text="Humidity", font=24, bg=bg, fg=fg)
humid.place(x=10, y=90)

dist = Label(settings, text="Distance", font=24, bg=bg, fg=fg)
dist.place(x=10, y=130)

# Entry Labels
ts = Label(settings, text="Set:", font=24, bg=bg, fg=fg)
ts.place(x=200, y=50)

tr = Label(settings, text="Range:", font=24, bg=bg, fg=fg)
tr.place(x=300, y=50)

hs = Label(settings, text="Set:", font=24, bg=bg, fg=fg)
hs.place(x=200, y=90)

hr = Label(settings, text="Range:", font=24, bg=bg, fg=fg)
hr.place(x=300, y=90)

ds = Label(settings, text="Set:", font=24, bg=bg, fg=fg)
ds.place(x=200, y=130)

# Entry boxes
ts_val = StringVar()
hs_val = StringVar()
tr_val = StringVar()
hr_val = StringVar()
ds_val = StringVar()

ts_entry = Entry(settings, textvariable=ts_val, width=4)
ts_entry.place(x=245, y=50)

tr_entry = Entry(settings, textvariable=tr_val, width=4)
tr_entry.place(x=370, y=50)

hs_entry = Entry(settings, textvariable=hs_val, width=4)
hs_entry.place(x=245, y=90)

hr_entry = Entry(settings, textvariable=hr_val, width=4)
hr_entry.place(x=370, y=90)

ds_entry = Entry(settings, textvariable=ds_val, width=4)
ds_entry.place(x=245, y=130)

# Set button
set_btn = Button(settings, text="Set", command="")
set_btn.place(x=200, y=200)

root.mainloop()
