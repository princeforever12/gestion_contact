"""Interface graphique Tkinter pour le carnet d'adresses."""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

from address_book import (
    AddressBook,
    ajouter_contact,
    ajouter_numero,
    afficher_tous_les_contacts,
    charger_depuis_csv,
    charger_depuis_json,
    rechercher_par_prefixe,
    sauvegarder_en_csv,
    sauvegarder_en_json,
    supprimer_contact,
)


class CarnetApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Carnet d'adresses")
        self.root.geometry("760x520")

        self.carnet: AddressBook = {}

        self._build_ui()
        self._refresh_output()

    def _build_ui(self) -> None:
        frame_top = tk.Frame(self.root)
        frame_top.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_top, text="Nom").grid(row=0, column=0, sticky="w")
        self.entry_nom = tk.Entry(frame_top, width=25)
        self.entry_nom.grid(row=1, column=0, padx=5)

        tk.Label(frame_top, text="Téléphones (séparés par ,)").grid(row=0, column=1, sticky="w")
        self.entry_telephones = tk.Entry(frame_top, width=30)
        self.entry_telephones.grid(row=1, column=1, padx=5)

        tk.Label(frame_top, text="Email").grid(row=0, column=2, sticky="w")
        self.entry_email = tk.Entry(frame_top, width=30)
        self.entry_email.grid(row=1, column=2, padx=5)

        frame_actions = tk.Frame(self.root)
        frame_actions.pack(fill="x", padx=10, pady=5)

        tk.Button(frame_actions, text="Ajouter contact", command=self._ajouter_contact).pack(side="left", padx=4)
        tk.Button(frame_actions, text="Ajouter numéro", command=self._ajouter_numero).pack(side="left", padx=4)
        tk.Button(frame_actions, text="Supprimer contact", command=self._supprimer_contact).pack(side="left", padx=4)

        frame_search = tk.Frame(self.root)
        frame_search.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_search, text="Recherche préfixe").pack(side="left")
        self.entry_prefixe = tk.Entry(frame_search, width=25)
        self.entry_prefixe.pack(side="left", padx=6)
        tk.Button(frame_search, text="Rechercher", command=self._rechercher).pack(side="left")
        tk.Button(frame_search, text="Réinitialiser", command=self._refresh_output).pack(side="left", padx=6)

        frame_io = tk.Frame(self.root)
        frame_io.pack(fill="x", padx=10, pady=5)

        tk.Button(frame_io, text="Sauvegarder JSON", command=self._save_json).pack(side="left", padx=4)
        tk.Button(frame_io, text="Charger JSON", command=self._load_json).pack(side="left", padx=4)
        tk.Button(frame_io, text="Sauvegarder CSV", command=self._save_csv).pack(side="left", padx=4)
        tk.Button(frame_io, text="Charger CSV", command=self._load_csv).pack(side="left", padx=4)

        self.output = tk.Text(self.root, wrap="word")
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

    def _get_phones_list(self) -> list[str]:
        return [item.strip() for item in self.entry_telephones.get().split(",") if item.strip()]

    def _ajouter_contact(self) -> None:
        nom = self.entry_nom.get()
        telephones = self._get_phones_list()
        email = self.entry_email.get()

        try:
            if ajouter_contact(self.carnet, nom, telephones, email):
                messagebox.showinfo("Succès", "Contact ajouté.")
                self._refresh_output()
            else:
                messagebox.showwarning("Doublon", "Un contact avec ce nom existe déjà.")
        except ValueError as error:
            messagebox.showerror("Erreur", str(error))

    def _ajouter_numero(self) -> None:
        nom = self.entry_nom.get()
        numero = simpledialog.askstring("Nouveau numéro", "Numéro à ajouter:")
        if numero is None:
            return

        try:
            if ajouter_numero(self.carnet, nom, numero):
                messagebox.showinfo("Succès", "Numéro ajouté.")
                self._refresh_output()
            else:
                messagebox.showwarning("Information", "Contact introuvable ou numéro déjà présent.")
        except ValueError as error:
            messagebox.showerror("Erreur", str(error))

    def _supprimer_contact(self) -> None:
        nom = self.entry_nom.get()
        try:
            if supprimer_contact(self.carnet, nom):
                messagebox.showinfo("Succès", "Contact supprimé.")
                self._refresh_output()
            else:
                messagebox.showwarning("Information", "Contact introuvable.")
        except ValueError as error:
            messagebox.showerror("Erreur", str(error))

    def _rechercher(self) -> None:
        prefixe = self.entry_prefixe.get()
        resultats = rechercher_par_prefixe(self.carnet, prefixe)
        self._show_text(afficher_tous_les_contacts(resultats) if resultats else "Aucun résultat.")

    def _show_text(self, value: str) -> None:
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, value)

    def _refresh_output(self) -> None:
        self._show_text(afficher_tous_les_contacts(self.carnet))

    def _save_json(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not path:
            return
        sauvegarder_en_json(self.carnet, path)
        messagebox.showinfo("Succès", "Sauvegarde JSON effectuée.")

    def _load_json(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not path:
            return
        self.carnet = charger_depuis_json(path)
        self._refresh_output()
        messagebox.showinfo("Succès", "Chargement JSON effectué.")

    def _save_csv(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not path:
            return
        sauvegarder_en_csv(self.carnet, path)
        messagebox.showinfo("Succès", "Sauvegarde CSV effectuée.")

    def _load_csv(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if not path:
            return
        self.carnet = charger_depuis_csv(path)
        self._refresh_output()
        messagebox.showinfo("Succès", "Chargement CSV effectué.")


def main() -> None:
    root = tk.Tk()
    CarnetApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
