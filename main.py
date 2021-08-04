import tkinter as tk
import random
from playsound import playsound

data = {}
chances = []


def add_to_list():
    global data
    name = entry_name.get()
    qty = entry_qty.get()
    data[name] = qty
    txt_list.delete(1.0, tk.END)
    for key in data:
        txt_list.insert(tk.END, (key + ": " + data[key] + "\n"))
    entry_name.delete(0, tk.END)
    entry_qty.delete(0, tk.END)


def pick_a_winner():
    global data
    global chances
    try:
        for key in data:
            for value in range(int(data[key])):
                chances.append(key)
        winner = random.choice(chances)
        winner_text = "The winner is: " + winner
        txt_list.delete(1.0, tk.END)
        playsound("winner.mp3", 0)
        txt_list.insert(tk.END, winner_text)
    except ValueError:
        txt_list.delete(1.0, tk.END)
        txt_list.insert(tk.END, "Blank entry entered, clearing entries")
        data.clear()
    except IndexError:
        txt_list.delete(1.0, tk.END)
        txt_list.insert(tk.END, "No entries entered")


app = tk.Tk()
app.title("Raffle Winner")
app.resizable(False, False)

frm_name = tk.Frame()
frm_qty = tk.Frame()

lbl_name = tk.Label(frm_name, text="Colleague")
lbl_name.pack()
lbl_qty = tk.Label(frm_qty, text="Entries")
lbl_qty.pack()

btn_winner = tk.Button(app, text="Pick a winner!", command=pick_a_winner)
btn_winner.pack(side="bottom")

txt_list = tk.Text(app, height=10, width=30, wrap="word")
txt_list.pack(side="bottom", fill="both", expand=True)

btn_add = tk.Button(app, text="Add to list", command=add_to_list)
btn_add.pack(side="bottom")

entry_name = tk.Entry(frm_name)
entry_name.pack(fill="both")
entry_qty = tk.Entry(frm_qty, width=5)
entry_qty.pack()

frm_name.pack(side="left", fill="both")
frm_qty.pack(side="left")
app.mainloop()
