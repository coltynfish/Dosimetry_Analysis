import tkinter as tk
from tkinter import filedialog
import pandas as pd

def save_values():
    grid_values = []
    for i in range(rows):
        row_values = []
        for j in range(columns):
            value = grid_entries[i][j].get()
            if value == "":
                value = "0"  # Set empty values as zero
            row_values.append(value)
        grid_values.append(row_values)

    df = pd.DataFrame(grid_values)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        df.to_csv(file_path, index=False, header=False, sep=' ', na_rep='0')
        #with open(file_path, "w") as file:
        #    file.write(df.to_string(index=False, header=False))

def insert_barcode(event):
    scanned_serial = event.widget.get()
    grid_entries[0][0].delete(0, tk.END)
    grid_entries[0][0].insert(0, scanned_serial)

rows = 10
columns = 11

root = tk.Tk()

# Create a 2D list to store the Entry widgets
grid_entries = []
for i in range(rows):
    row_entries = []
    for j in range(columns):
        entry = tk.Entry(root, width=10)
        entry.grid(row=i, column=j, sticky="ew")  # Use sticky="ew" to make cells expand horizontally
        row_entries.append(entry)
    grid_entries.append(row_entries)

# Configure column weight to ensure left column fills properly
for j in range(columns):
    root.grid_columnconfigure(j, weight=1)

# Button to save the values
button_save_values = tk.Button(root, text="Save Values", command=save_values)
button_save_values.grid(row=rows, column=0, columnspan=columns, sticky="ew")  # Use sticky="ew" for button

# Entry for barcode scanner
barcode_entry = tk.Entry(root, width=10)
barcode_entry.grid(row=0, column=0, sticky="ew")  # Use sticky="ew" for barcode entry
barcode_entry.bind("<Return>", insert_barcode)  # Capture barcode scanner event

root.mainloop()
