import tkinter as tk
from tkinter import ttk
import random
from playsound import playsound
import json
from ttkthemes import ThemedTk

# Global variables
data = {}
chances = []


# Read data and format into readable list
def format_list():
    for key in data:
        txt_list.insert(tk.END, (key + ": " + data[key] + "\n"))


# Delete the last entry and re-display list
def delete_last():
    global data
    data.popitem()
    txt_list.delete(1.0, tk.END)
    format_list()


# Clear all the data in variables
def clear_data():
    data.clear()
    chances.clear()
    txt_list.delete(1.0, tk.END)


# Save the list to a JSON file
def save_json():
    with open("output.json", "w") as filename:
        json.dump(data, filename)


# Load the JSON, parse it into a dict and display
def load_json():
    global data
    try:
        with open("output.json", "r") as filename:
            try:
                txt_list.delete(1.0, tk.END)
                data = json.load(filename)
                format_list()
            except json.decoder.JSONDecodeError:
                txt_list.delete(1.0, tk.END)
    except FileNotFoundError:
        with open("output.json", "w") as new_file:
            new_file.write("{}")


# Add the entered Colleague and Qty into a dict
def add_to_list():
    global data
    name = entry_name.get()
    qty = entry_qty.get()
    data[name] = qty
    txt_list.delete(1.0, tk.END)
    format_list()
    entry_name.delete(0, tk.END)
    entry_qty.delete(0, tk.END)


# Copy the Colleague name as many times as Qty shows, then pick a winner
def pick_a_winner():
    global data
    global chances
    try:
        for key in data:
            for value in range(int(data[key])):
                chances.append(key)
        winner = random.choice(chances)
        winner_text = "\nThe winner is: " + winner
        if check_sound.get() == 1:
            playsound("winner.mp3", 0)
        txt_list.insert(tk.END, winner_text)
    except ValueError:
        txt_list.delete(1.0, tk.END)
        txt_list.insert(tk.END, "Blank entry entered")
    except IndexError:
        txt_list.delete(1.0, tk.END)
        txt_list.insert(tk.END, "No entries entered")


# Set up the app
app = ThemedTk(theme="arc")
app.title("Raffle Winner")
app.resizable(False, False)
check_sound = tk.IntVar()

# Set up surrounding frame
frm_app = ttk.Frame(app)

# Set up the labels
lbl_name = ttk.Label(frm_app, text="Colleague")
lbl_qty = ttk.Label(frm_app, text="Entries")
lbl_options = ttk.Label(frm_app, text="Options")

# Set up buttons
btn_add = ttk.Button(frm_app, text="Add to list", command=add_to_list)
btn_clear = ttk.Button(frm_app, text="Clear Entries", command=clear_data)
btn_delete = ttk.Button(frm_app, text="Delete Entry", command=delete_last)
btn_save_json = ttk.Button(frm_app, text="Save Data", command=save_json)
btn_load_json = ttk.Button(frm_app, text="Load Data", command=load_json)
btn_winner = ttk.Button(frm_app, text="Pick a winner!", command=pick_a_winner)

# Set up text box
txt_list = tk.Text(frm_app, height=15, width=25, wrap="word", bg="white", fg="black",
                   insertbackground="black", font=("Arial", 13), borderwidth=1, relief="sunken", highlightthicknes=0)

# Set up entry boxes
entry_name = ttk.Entry(frm_app, width=15)
entry_qty = ttk.Entry(frm_app, width=10)

# Set up checkbox for sound
sound_on_off = ttk.Checkbutton(frm_app, text="Sound?", variable=check_sound)

# Set up a grid layout
lbl_name.grid(row=0, column=0, sticky="w", padx=5, pady=5)
lbl_qty.grid(row=0, column=1, sticky="w", padx=5, pady=5)
entry_name.grid(row=1, column=0, sticky="w", padx=5, pady=0)
entry_qty.grid(row=1, column=1, sticky="w", padx=5, pady=0)
btn_add.grid(row=2, column=0, columnspan=2, padx=5, pady=7)
txt_list.grid(row=3, rowspan=15, column=0, sticky="w", padx=5, pady=5)
lbl_options.grid(row=7, column=1, padx=5, pady=0)
btn_save_json.grid(row=8, column=1, padx=5, pady=1)
btn_load_json.grid(row=9, column=1, padx=5, pady=1)
btn_clear.grid(row=10, column=1, padx=5, pady=1)
btn_delete.grid(row=11, column=1, padx=5, pady=1)
sound_on_off.grid(row=12, column=1, padx=5, pady=0)
btn_winner.grid(row=18, column=0, columnspan=2, padx=5, pady=5)

# Pack the frame
frm_app.pack(fill="both", expand=True)

# Keep the app running until close
app.mainloop()
