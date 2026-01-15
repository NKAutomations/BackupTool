import os
import shutil
import json
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

CONFIG_FILE = "config.json"


class BackupToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartBackup Tool")
        self.root.geometry("650x600")

        self.source_paths = ["", "", "", "", ""]
        self.target_path = ""
        self.backup_name = ""

        self.load_config()

        self.create_gui()

    # ---------------------------------------------------------
    # CONFIG LADEN/SPEICHERN
    # ---------------------------------------------------------
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.source_paths = config.get("source_paths", ["", "", "", "", ""])
                    self.target_path = config.get("target_path", "")
                    self.backup_name = config.get("backup_name", "")
            except:
                pass

    def save_config(self):
        config = {
            "source_paths": self.source_paths,
            "target_path": self.target_path,
            "backup_name": self.backup_name
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)

    # ---------------------------------------------------------
    # GUI
    # ---------------------------------------------------------
    def create_gui(self):
        frame_sources = tk.LabelFrame(self.root, text="Quellpfade (bis zu 5 Dateien)")
        frame_sources.pack(fill="x", padx=10, pady=10)

        self.source_entries = []
        for i in range(5):
            frame = tk.Frame(frame_sources)
            frame.pack(fill="x", pady=3)

            entry = tk.Entry(frame, width=60)
            entry.pack(side="left", padx=5)
            entry.insert(0, self.source_paths[i])
            self.source_entries.append(entry)

            btn = tk.Button(frame, text="Durchsuchen", command=lambda idx=i: self.choose_source(idx))
            btn.pack(side="left")

        # ZIELPFAD
        frame_target = tk.LabelFrame(self.root, text="Zielordner")
        frame_target.pack(fill="x", padx=10, pady=10)

        frame = tk.Frame(frame_target)
        frame.pack(fill="x", pady=3)

        self.target_entry = tk.Entry(frame, width=60)
        self.target_entry.pack(side="left", padx=5)
        self.target_entry.insert(0, self.target_path)

        btn_target = tk.Button(frame, text="Durchsuchen", command=self.choose_target)
        btn_target.pack(side="left")

        # BACKUP NAME
        frame_name = tk.LabelFrame(self.root, text="Backup-Name")
        frame_name.pack(fill="x", padx=10, pady=10)

        self.name_entry = tk.Entry(frame_name, width=50)
        self.name_entry.pack(padx=10, pady=5)
        self.name_entry.insert(0, self.backup_name)

        # BUTTON
        btn_start = tk.Button(self.root, text="Backup erstellen", command=self.start_backup, bg="#c3e6cb")
        btn_start.pack(pady=10)

        # LOGFENSTER
        frame_log = tk.LabelFrame(self.root, text="Protokoll")
        frame_log.pack(fill="both", expand=True, padx=10, pady=10)

        self.log_area = scrolledtext.ScrolledText(frame_log, height=15)
        self.log_area.pack(fill="both", expand=True)

    # ---------------------------------------------------------
    # PFAD DIALOGE
    # ---------------------------------------------------------
    def choose_source(self, index):
        path = filedialog.askopenfilename(title="Datei auswählen")
        if path:
            self.source_entries[index].delete(0, tk.END)
            self.source_entries[index].insert(0, path)

    def choose_target(self):
        path = filedialog.askdirectory(title="Zielordner auswählen")
        if path:
            self.target_entry.delete(0, tk.END)
            self.target_entry.insert(0, path)

    # ---------------------------------------------------------
    # BACKUP STARTEN
    # ---------------------------------------------------------
    def start_backup(self):
        self.source_paths = [entry.get().strip() for entry in self.source_entries]
        self.target_path = self.target_entry.get().strip()
        self.backup_name = self.name_entry.get().strip()

        self.save_config()

        if not self.backup_name:
            messagebox.showerror("Fehler", "Bitte einen Backup-Namen eingeben.")
            return

        if not self.target_path:
            messagebox.showerror("Fehler", "Bitte einen Zielordner auswählen.")
            return

        date_str = datetime.datetime.now().strftime("%d%m%Y")
        backup_folder_name = f"{self.backup_name}_{date_str}"
        backup_folder = os.path.join(self.target_path, backup_folder_name)

        try:
            os.makedirs(backup_folder, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Fehler", f"Konnte Backup-Ordner nicht erstellen:\n{e}")
            return

        log_file_path = os.path.join(backup_folder, "backup_log.txt")
        log_file = open(log_file_path, "w", encoding="utf-8")

        self.log("Starte Backup...\n")
        log_file.write("Backup gestartet.\n\n")

        for src in self.source_paths:
            if not src:
                continue

            if not os.path.exists(src):
                msg = f"Quelle nicht gefunden: {src}"
                self.log(msg)
                log_file.write(msg + "\n")
                continue

            try:
                filename = os.path.basename(src)
                dst = os.path.join(backup_folder, filename)
                shutil.copy2(src, dst)

                msg = f"Kopiert: {src} -> {dst}"
                self.log(msg)
                log_file.write(msg + "\n")

            except Exception as e:
                msg = f"Fehler beim Kopieren von {src}: {e}"
                self.log(msg)
                log_file.write(msg + "\n")

        log_file.close()

        self.log("\nBackup abgeschlossen!")
        messagebox.showinfo("Fertig", "Backup erfolgreich erstellt!")

    # ---------------------------------------------------------
    # LOGAUSGABE
    # ---------------------------------------------------------
    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.yview_moveto(1)


# ---------------------------------------------------------
# START
# ---------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = BackupToolGUI(root)
    root.mainloop()
