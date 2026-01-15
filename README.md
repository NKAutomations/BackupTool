# SmartBackup Tool
**Version 1.0.0**

SmartBackup ist ein einfaches, zuverlässiges und benutzerfreundliches Backup‑Tool mit grafischer Oberfläche (GUI).  
Es ermöglicht das Kopieren von bis zu fünf ausgewählten Dateien in einen automatisch erzeugten Backup‑Ordner mit Datumsstempel.  
Alle Pfade und Einstellungen werden dauerhaft in einer config.json gespeichert.

Ideal für schnelle tägliche Backups von Projektdateien, Dokumenten oder Logs.

---

## ✨ Funktionen

- GUI mit bis zu **5 auswählbaren Quelldateien**
- **Zielordner-Auswahl** über Dateidialog
- Eingabefeld für eigenen **Backup‑Namen**
- Automatische Speicherung aller Einstellungen in **config.json**
- Backup‑Ordner wird erzeugt im Format:  
  `NAME_TTMMJJJJ`
- Jede Datei wird kopiert, fehlende Dateien werden protokolliert
- Log wird sowohl im Fenster als auch im Backup‑Ordner gespeichert
- Robust gegen Fehler (keine Abstürze)
- Lässt sich leicht zu einer **.exe** kompilieren (PyInstaller)

---

## 📦 Anforderungen

- Python 3.14 oder neuer  
- Standardbibliotheken (tkinter, shutil, json etc.)  
- Optional: PyInstaller zum Erzeugen der .exe

---

## 🚀 Installation

1. Repository klonen:
```bash
   git clone https://github.com/DEINNAME/SmartBackupTool.git
