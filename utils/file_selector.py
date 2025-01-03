import tkinter as tk
from tkinter import filedialog
import os


def select_files():
    # Crée une fenêtre principale cachée
    root = tk.Tk()
    root.withdraw()  # Cache la fenêtre principale

    # Ouvre la boîte de dialogue pour sélectionner un dossier
    files_selected = filedialog.askopenfiles("r")

    # Retourne le chemin du dossier sélectionné
    return files_selected


def get_and_select_files():
    current_path = os.getcwd()

    selected_files = select_files()
    files = []
    if selected_files:
        for file in selected_files:
            new_file_path = file.name.replace(current_path, "")
            if new_file_path.startswith("/"):
                new_file_path = new_file_path[1:]
            files.append(new_file_path)
    return files


# Exemple d'utilisation
if __name__ == "__main__":
    current_path = os.getcwd()
    print(current_path)
    selected_files = select_files()
    if selected_files:
        for file in selected_files:
            new_file_path = file.name.replace(current_path, "")
            if new_file_path.startswith("/"):
                new_file_path = new_file_path[1:]
            print(new_file_path)
