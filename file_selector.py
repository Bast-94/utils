import tkinter as tk
from tkinter import filedialog
import os
import tkinter as tk
from tkinter import filedialog, messagebox  # Ajout de messagebox
import os
import tkinter as tk
from tkinter import ttk
import os


import tkinter as tk
from tkinter import ttk
import os


class FileBrowser(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sélection de fichiers - Vue en arbre")
        self.geometry("800x600")

        # Variables pour stocker les fichiers sélectionnés
        self.selected_files = []

        # Création du Treeview
        self.tree = ttk.Treeview(self, columns=("Type", "Selected"), selectmode="extended")
        self.tree.heading("#0", text="Nom")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Selected", text="Selected")

        self.tree.column("#0", stretch=True, width=300)
        self.tree.column("Type", stretch=False, width=100)
        self.tree.column("Selected", stretch=False, width=100)

        # add a button to select a file on each row


        self.tree.pack(fill="both", expand=True)

        # Associer l'événement pour charger les sous-dossiers lorsqu'un dossier est développé
        self.tree.bind("<<TreeviewOpen>>", self.on_folder_open)
        self.tree.bind("<<TreeviewSelect>>", self.on_item_selected)
        # Ajouter le Treeview à une barre de défilement
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Boutons
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(side="bottom", fill="x", pady=10)

        ttk.Button(
            self.button_frame,
            text="Valider la sélection",
            command=self.validate_selection,
        ).pack(side="left", padx=10)
        ttk.Button(self.button_frame, text="Annuler", command=self.quit).pack(
            side="right", padx=10
        )

        # Charger les fichiers à partir du répertoire actuel
        self.load_directory(".", "")

    def load_directory(self, path, parent):
        """Charge les fichiers et dossiers dans le Treeview"""
        try:

            # sort by dir first and then by name
            key_function = lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower())

            for item in sorted(os.listdir(path), key=key_function):

                item_path = os.path.join(path, item)
                is_dir = os.path.isdir(item_path)

                # Ajouter un noeud à l'arbre
                node_id = self.tree.insert(
                    parent,
                    "end",
                    text=item,
                    values=("Dossier" if is_dir else "Fichier", item_path),
                )

                # Si c'est un dossier, ajoutez un placeholder pour permettre le chargement à la demande
                if is_dir:
                    self.tree.insert(node_id, "end", text="(chargement...)")
        except PermissionError:
            pass

    def on_folder_open(self, event):
        """Charge les sous-dossiers lorsque l'utilisateur développe un dossier"""

        # Récupérer l'élément ouvert
        item_id = self.tree.focus()
        item_path = self.tree.item(item_id, "values")[1]

        # Supprimer le placeholder
        children = self.tree.get_children(item_id)
        if children and self.tree.item(children[0], "text") == "(chargement...)":
            self.tree.delete(children[0])

        # Charger les sous-dossiers et fichiers
        self.load_directory(item_path, item_id)

    def on_item_selected(self, event):
        """Met à jour la liste des fichiers sélectionnés"""

        self.selected_files.clear()
        for item in self.tree.selection():

            values = self.tree.item(item, "values")
            if values:
                self.selected_files.append(values[1])




    def validate_selection(self):
        """Affiche les fichiers sélectionnés et quitte"""


        self.quit()
        print("Fichiers sélectionnés:")
        for file in self.selected_files:
            print(file)


def get_and_select_files():
    current_path = os.getcwd()
    root = FileBrowser()
    root.mainloop()

    selected_files = root.selected_files
    files = []
    if selected_files:
        for file in selected_files:

            new_file_path = file.replace(current_path, "")
            if new_file_path.startswith("/"):
                new_file_path = new_file_path[1:]
            files.append(new_file_path)
    return files


# Exemple d'utilisation
if __name__ == "__main__":
    current_path = os.getcwd()
    print(current_path)
    selected_files = get_and_select_files()
    if selected_files:
        for file in selected_files:
            new_file_path = file.replace(current_path, "")
            if new_file_path.startswith("/"):
                new_file_path = new_file_path[1:]
