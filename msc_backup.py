import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font
import shutil
import os

# Uloží config do Dokumentů
CONFIG_FILE = os.path.join(os.path.expanduser("~"), "Documents", "mscbackupConfig.txt")

class FolderSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate MSC Backuper V2")
        self.root.geometry("600x250")
        self.root.resizable(False, False)

        # Fonty
        self.label_font = font.Font(family="Arial", size=11, weight="bold")
        self.button_font = font.Font(family="Arial", size=10)

        # Načtení uložených cest
        self.save_folder_var = tk.StringVar()
        self.mod_folder_var = tk.StringVar()
        self.backup_folder_var = tk.StringVar()
        self.load_config()

        # Save folder
        tk.Label(root, text="Save folder:", font=self.label_font).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.save_entry = tk.Entry(root, textvariable=self.save_folder_var, width=50)
        self.save_entry.grid(row=0, column=1, padx=10)
        tk.Button(root, text="Select", font=self.button_font, command=self.select_save_folder).grid(row=0, column=2, padx=10)

        # Mod folder
        tk.Label(root, text="Mod folder:", font=self.label_font).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.mod_entry = tk.Entry(root, textvariable=self.mod_folder_var, width=50)
        self.mod_entry.grid(row=1, column=1, padx=10)
        tk.Button(root, text="Select", font=self.button_font, command=self.select_mod_folder).grid(row=1, column=2, padx=10)

        # Backup folder
        tk.Label(root, text="Backup destination:", font=self.label_font).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.backup_entry = tk.Entry(root, textvariable=self.backup_folder_var, width=50)
        self.backup_entry.grid(row=2, column=1, padx=10)
        tk.Button(root, text="Select", font=self.button_font, command=self.select_backup_folder).grid(row=2, column=2, padx=10)

        # Confirm button
        self.btn_confirm = tk.Button(root, text="Confirm", width=40, font=self.button_font, bg="#4CAF50", fg="white", command=self.confirm)
        self.btn_confirm.grid(row=3, column=0, columnspan=3, pady=20)

        # Create Backup button (hidden at start)
        self.btn_create_backup = tk.Button(root, text="Create Backup", width=40, font=self.button_font, bg="#2196F3", fg="white", command=self.create_backup)
        self.btn_create_backup.grid(row=4, column=0, columnspan=3, pady=10)
        self.btn_create_backup.grid_remove()

    # --- Folder selection ---
    def select_save_folder(self):
        folder = filedialog.askdirectory(title="Select save folder")
        if folder:
            self.save_folder_var.set(folder)

    def select_mod_folder(self):
        folder = filedialog.askdirectory(title="Select mod folder")
        if folder:
            self.mod_folder_var.set(folder)

    def select_backup_folder(self):
        folder = filedialog.askdirectory(title="Select backup destination")
        if folder:
            self.backup_folder_var.set(folder)

    # --- Confirm ---
    def confirm(self):
        if not self.save_folder_var.get() or not self.mod_folder_var.get() or not self.backup_folder_var.get():
            messagebox.showwarning("Warning", "Please select all folders!")
            return
        # Uloží cesty do configu
        self.save_config()
        # Zobrazí Create Backup button
        self.btn_create_backup.grid()

    # --- Backup ---
    def create_backup(self):
        backup_name = simpledialog.askstring("Backup Name", "Enter a name for your backup folder:")
        if not backup_name:
            messagebox.showwarning("Cancelled", "Backup cancelled, no name provided.")
            return

        backup_path = os.path.join(self.backup_folder_var.get(), backup_name)
        save_dest = os.path.join(backup_path, "Save")
        mod_dest = os.path.join(backup_path, "Mod")

        try:
            os.makedirs(save_dest, exist_ok=True)
            os.makedirs(mod_dest, exist_ok=True)

            if os.path.exists(self.save_folder_var.get()):
                self.copy_folder_contents(self.save_folder_var.get(), save_dest)

            if os.path.exists(self.mod_folder_var.get()):
                self.copy_folder_contents(self.mod_folder_var.get(), mod_dest)

            messagebox.showinfo("Success", f"Backup created successfully at:\n{backup_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    @staticmethod
    def copy_folder_contents(src, dest):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dest, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

    # --- Config management ---
    def save_config(self):
        try:
            with open(CONFIG_FILE, "w") as f:
                f.write(self.save_folder_var.get() + "\n")
                f.write(self.mod_folder_var.get() + "\n")
                f.write(self.backup_folder_var.get() + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {e}")

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    lines = f.read().splitlines()
                    if len(lines) >= 3:
                        self.save_folder_var.set(lines[0])
                        self.mod_folder_var.set(lines[1])
                        self.backup_folder_var.set(lines[2])
            except:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderSelectorApp(root)
    root.mainloop()
