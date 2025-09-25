import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

# --- Functions ---
def select_folder():
    global save_folder
    folder = filedialog.askdirectory(title="Select My Summer Car save folder")
    if folder:
        save_folder = folder
        lbl_folder.config(text=f"Current save folder: {save_folder}")

def create_backup():
    if not save_folder:
        messagebox.showerror("Error", "Please select the save folder first!")
        return
    
    # desktop MSC Saves folder
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    backup_base = os.path.join(desktop, "MSC Saves")
    os.makedirs(backup_base, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = f"Backup_{timestamp}"
    backup_path = os.path.join(backup_base, backup_name)
    os.makedirs(backup_path, exist_ok=True)
    
    # copy all save files
    for f in os.listdir(save_folder):
        full_path = os.path.join(save_folder, f)
        if os.path.isfile(full_path):
            shutil.copy(full_path, backup_path)
    
    messagebox.showinfo("Done", f"Backup created: {backup_path}")
    update_backup_list()

def load_backup():
    selection = listbox.get(listbox.curselection())
    if not selection:
        messagebox.showerror("Error", "Select a backup from the list!")
        return
    backup_path = os.path.join(desktop, "MSC Saves", selection)
    
    # overwrite current save files
    for f in os.listdir(backup_path):
        shutil.copy(os.path.join(backup_path, f), save_folder)
    
    messagebox.showinfo("Done", f"Backup loaded: {selection}")

def update_backup_list():
    listbox.delete(0, tk.END)
    backup_base = os.path.join(desktop, "MSC Saves")
    if os.path.exists(backup_base):
        for item in sorted(os.listdir(backup_base), reverse=True):
            listbox.insert(tk.END, item)

# --- GUI ---
save_folder = ""
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

root = tk.Tk()
root.title("My Summer Car - Save Backup")

lbl_folder = tk.Label(root, text="Current save folder: not selected", wraplength=400)
lbl_folder.pack(pady=5)

btn_select = tk.Button(root, text="Select save folder", command=select_folder)
btn_select.pack(pady=5)

btn_backup = tk.Button(root, text="Backup current save", command=create_backup)
btn_backup.pack(pady=5)

lbl_backups = tk.Label(root, text="List of backups:")
lbl_backups.pack(pady=5)

listbox = tk.Listbox(root, width=60)
listbox.pack(pady=5)

btn_load = tk.Button(root, text="Load selected backup", command=load_backup)
btn_load.pack(pady=5)

# Mini credit label
lbl_credit = tk.Label(root, text="Created by: Dave14", font=("Arial", 8), fg="gray")
lbl_credit.pack(pady=5)

update_backup_list()
root.mainloop()
