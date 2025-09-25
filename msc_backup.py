import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# --- Global Variables ---
mods_folder = ""
save_folder = ""
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
base_folder = os.path.join(desktop, "Ultimate MSC Backuper")
backup_base = os.path.join(base_folder, "Backups")

# Ensure base folders exist
os.makedirs(backup_base, exist_ok=True)

# --- Functions ---
def select_mods_folder():
    global mods_folder
    folder = filedialog.askdirectory(title="Select My Summer Car Mods folder")
    if folder:
        mods_folder = folder
        lbl_mods.config(text=f"Mods folder: {mods_folder}")

def select_save_folder():
    global save_folder
    folder = filedialog.askdirectory(title="Select My Summer Car Save folder")
    if folder:
        save_folder = folder
        lbl_save.config(text=f"Save folder: {save_folder}")

def create_backup():
    if not mods_folder or not save_folder:
        messagebox.showerror("Error", "Please select both Mods and Save folders first!")
        return
    
    # Ask user for backup name
    backup_name = simpledialog.askstring("Backup Name", "Enter a name for this backup:")
    if not backup_name:
        return

    # Create backup folder
    backup_path = os.path.join(backup_base, backup_name)
    if os.path.exists(backup_path):
        messagebox.showerror("Error", "Backup with this name already exists!")
        return
    os.makedirs(backup_path, exist_ok=True)

    # Copy Mods folder recursively
    mods_backup_path = os.path.join(backup_path, "Mods")
    shutil.copytree(mods_folder, mods_backup_path)

    # Copy Save folder recursively
    save_backup_path = os.path.join(backup_path, "Save")
    shutil.copytree(save_folder, save_backup_path)

    messagebox.showinfo("Done", f"Backup created: {backup_path}")
    update_backup_list()

def load_backup():
    selection = listbox.get(listbox.curselection()) if listbox.curselection() else None
    if not selection or selection == "No backups found":
        messagebox.showerror("Error", "Select a backup from the list!")
        return
    
    backup_path = os.path.join(backup_base, selection)
    
    # Restore Mods
    mods_backup_path = os.path.join(backup_path, "Mods")
    if mods_folder and os.path.exists(mods_backup_path):
        # Remove existing content in mods_folder
        if os.path.exists(mods_folder):
            shutil.rmtree(mods_folder)
        shutil.copytree(mods_backup_path, mods_folder)

    # Restore Save
    save_backup_path = os.path.join(backup_path, "Save")
    if save_folder and os.path.exists(save_backup_path):
        if os.path.exists(save_folder):
            shutil.rmtree(save_folder)
        shutil.copytree(save_backup_path, save_folder)

    messagebox.showinfo("Done", f"Backup loaded: {selection}")

def update_backup_list():
    listbox.delete(0, tk.END)
    # Ensure backup folder exists
    os.makedirs(backup_base, exist_ok=True)
    # List only folders
    items = [d for d in os.listdir(backup_base) if os.path.isdir(os.path.join(backup_base, d))]
    if not items:
        listbox.insert(tk.END, "No backups found")
    else:
        for item in sorted(items, reverse=True):
            listbox.insert(tk.END, item)

def refresh_list():
    update_backup_list()

# --- GUI ---
root = tk.Tk()
root.title("Ultimate MSC Backuper")

lbl_mods = tk.Label(root, text="Mods folder: not selected", wraplength=400)
lbl_mods.pack(pady=5)
btn_mods = tk.Button(root, text="Select Mods folder", command=select_mods_folder)
btn_mods.pack(pady=5)

lbl_save = tk.Label(root, text="Save folder: not selected", wraplength=400)
lbl_save.pack(pady=5)
btn_save = tk.Button(root, text="Select Save folder", command=select_save_folder)
btn_save.pack(pady=5)

btn_backup = tk.Button(root, text="Create Backup", command=create_backup)
btn_backup.pack(pady=5)

btn_refresh = tk.Button(root, text="Refresh Backup List", command=refresh_list)
btn_refresh.pack(pady=5)

lbl_backups = tk.Label(root, text="List of backups:")
lbl_backups.pack(pady=5)

listbox = tk.Listbox(root, width=60)
listbox.pack(pady=5)

btn_load = tk.Button(root, text="Load Selected Backup", command=load_backup)
btn_load.pack(pady=5)

lbl_credit = tk.Label(root, text="Created by: Dave14", font=("Arial", 8), fg="gray")
lbl_credit.pack(pady=5)

update_backup_list()
root.mainloop()
