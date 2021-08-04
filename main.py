import tkinter as tk
import random
from playsound import playsound
import json

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
        playsound("winner.mp3", 0)
        txt_list.insert(tk.END, winner_text)
    except ValueError:
        txt_list.delete(1.0, tk.END)
        txt_list.insert(tk.END, "Blank entry entered")
    except IndexError:
        txt_list.delete(1.0, tk.END)
        txt_list.insert(tk.END, "No entries entered")


# Set up the app
app = tk.Tk()
app.title("Raffle Winner")
app.resizable(False, False)

# Create all the frames to hold UI elements
frm_name = tk.Frame(app)
frm_qty = tk.Frame(app)
frm_file_opts = tk.Frame(app)
frm_clear_delete = tk.Frame(app)

# Set up the labels
lbl_name = tk.Label(frm_name, text="Colleague")
lbl_qty = tk.Label(frm_qty, text="Entries")

# Pack labels
lbl_name.pack()
lbl_qty.pack()

# Set up buttons
btn_add = tk.Button(app, text="Add to list", command=add_to_list)
btn_clear = tk.Button(frm_clear_delete, text="Clear Entries", command=clear_data)
btn_delete = tk.Button(frm_clear_delete, text="Delete Entry", command=delete_last)
btn_save_json = tk.Button(frm_file_opts, text="Save Data", command=save_json)
btn_load_json = tk.Button(frm_file_opts, text="Load Data", command=load_json)
btn_winner = tk.Button(app, text="Pick a winner!", command=pick_a_winner)

# Pack all buttons
btn_clear.pack(side="left", fill="both", expand=True)
btn_delete.pack(side="left", fill="both", expand=True)
btn_save_json.pack(side="left", fill="both", expand=True)
btn_load_json.pack(side="left", fill="both", expand=True)

# Set up text box
txt_list = tk.Text(app, height=15, width=25, wrap="word")

# Set up entry boxes
entry_name = tk.Entry(frm_name)
entry_qty = tk.Entry(frm_qty, width=5)

# Pack entry boxes
entry_name.pack()
entry_qty.pack()

# Pack in order of displayed on app
btn_winner.pack(side="bottom", padx=5, pady=2)
frm_file_opts.pack(side="bottom", fill="both", expand=True, padx=5, pady=2)
frm_clear_delete.pack(side="bottom", fill="both", expand=True, padx=5, pady=2)
txt_list.pack(side="bottom", fill="both", expand=True)
btn_add.pack(side="bottom", padx=5, pady=2)
frm_name.pack(side="left", fill="both", expand=True, padx=5, pady=2)
frm_qty.pack(side="left", fill="both", expand=True, padx=5, pady=2)

# Keep the app running until close
app.mainloop()
