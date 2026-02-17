"""Interface graphique Tkinter moderne pour le carnet d'adresses."""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

from address_book import (
    AddressBook,
    ajouter_contact,
    ajouter_numero,
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
        self.root.title("Carnet d'adresses • Interface moderne")
        self.root.geometry("980x620")
        self.root.minsize(900, 560)

        self.carnet: AddressBook = {}
        self.filtered: AddressBook | None = None

        self._setup_style()
        self._build_ui()
        self._refresh_table()

    def _setup_style(self) -> None:
        self.root.configure(bg="#0f172a")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Title.TLabel", background="#0f172a", foreground="#e2e8f0", font=("Segoe UI", 18, "bold"))
        style.configure("Subtitle.TLabel", background="#0f172a", foreground="#94a3b8", font=("Segoe UI", 10))
        style.configure("Card.TFrame", background="#1e293b")
        style.configure("CardTitle.TLabel", background="#1e293b", foreground="#f8fafc", font=("Segoe UI", 11, "bold"))
        style.configure("CardText.TLabel", background="#1e293b", foreground="#cbd5e1", font=("Segoe UI", 10))

        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("TButton", font=("Segoe UI", 10), padding=6)

        style.configure(
            "Treeview",
            background="#f8fafc",
            fieldbackground="#f8fafc",
            rowheight=30,
            font=("Segoe UI", 10),
        )
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=14)
        container.pack(fill="both", expand=True)

        self._build_header(container)
        self._build_form_card(container)
        self._build_toolbar(container)
        self._build_table(container)
        self._build_status_bar(container)

    def _build_header(self, parent: ttk.Frame) -> None:
        header = ttk.Frame(parent)
        header.pack(fill="x", pady=(0, 12))

        ttk.Label(header, text="📒 Carnet d'adresses", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Ajoutez, recherchez et sauvegardez vos contacts en JSON/CSV.",
            style="Subtitle.TLabel",
        ).pack(anchor="w")

    def _build_form_card(self, parent: ttk.Frame) -> None:
        card = ttk.Frame(parent, style="Card.TFrame", padding=14)
        card.pack(fill="x", pady=(0, 10))

        ttk.Label(card, text="Nouveau contact", style="CardTitle.TLabel").grid(row=0, column=0, columnspan=6, sticky="w")
        ttk.Label(card, text="Nom", style="CardText.TLabel").grid(row=1, column=0, sticky="w", pady=(10, 4))
        ttk.Label(card, text="Téléphones (séparés par ,)", style="CardText.TLabel").grid(row=1, column=2, sticky="w", pady=(10, 4))
        ttk.Label(card, text="Email", style="CardText.TLabel").grid(row=1, column=4, sticky="w", pady=(10, 4))

        self.entry_nom = ttk.Entry(card, width=26)
        self.entry_nom.grid(row=2, column=0, columnspan=2, sticky="ew", padx=(0, 8))

        self.entry_telephones = ttk.Entry(card, width=34)
        self.entry_telephones.grid(row=2, column=2, columnspan=2, sticky="ew", padx=(0, 8))

        self.entry_email = ttk.Entry(card, width=34)
        self.entry_email.grid(row=2, column=4, columnspan=2, sticky="ew")

        card.columnconfigure(0, weight=1)
        card.columnconfigure(2, weight=1)
        card.columnconfigure(4, weight=1)

    def _build_toolbar(self, parent: ttk.Frame) -> None:
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=(0, 10))

        ttk.Button(row, text="Ajouter contact", style="Accent.TButton", command=self._ajouter_contact).pack(side="left", padx=(0, 6))
        ttk.Button(row, text="Ajouter numéro", command=self._ajouter_numero).pack(side="left", padx=6)
        ttk.Button(row, text="Supprimer", command=self._supprimer_contact).pack(side="left", padx=6)

        ttk.Separator(row, orient="vertical").pack(side="left", fill="y", padx=10)

        ttk.Label(row, text="Recherche préfixe:").pack(side="left")
        self.entry_prefixe = ttk.Entry(row, width=24)
        self.entry_prefixe.pack(side="left", padx=6)
        ttk.Button(row, text="Rechercher", command=self._rechercher).pack(side="left", padx=4)
        ttk.Button(row, text="Tout afficher", command=self._reset_filter).pack(side="left", padx=4)

        ttk.Separator(row, orient="vertical").pack(side="left", fill="y", padx=10)

        ttk.Button(row, text="Sauver JSON", command=self._save_json).pack(side="left", padx=4)
        ttk.Button(row, text="Charger JSON", command=self._load_json).pack(side="left", padx=4)
        ttk.Button(row, text="Sauver CSV", command=self._save_csv).pack(side="left", padx=4)
        ttk.Button(row, text="Charger CSV", command=self._load_csv).pack(side="left", padx=4)

    def _build_table(self, parent: ttk.Frame) -> None:
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill="both", expand=True)

        columns = ("nom", "telephones", "email")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("nom", text="Nom")
        self.tree.heading("telephones", text="Téléphones")
        self.tree.heading("email", text="Email")
        self.tree.column("nom", width=220, anchor="w")
        self.tree.column("telephones", width=280, anchor="w")
        self.tree.column("email", width=300, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _build_status_bar(self, parent: ttk.Frame) -> None:
        self.status_var = tk.StringVar(value="Prêt")
        bar = ttk.Frame(parent)
        bar.pack(fill="x", pady=(10, 0))
        ttk.Label(bar, textvariable=self.status_var).pack(anchor="w")

    def _set_status(self, message: str) -> None:
        self.status_var.set(message)

    def _get_phones_list(self) -> list[str]:
        return [item.strip() for item in self.entry_telephones.get().split(",") if item.strip()]

    def _selected_name(self) -> str | None:
        selected = self.tree.selection()
        if not selected:
            return None
        return str(self.tree.item(selected[0], "values")[0])

    def _current_view(self) -> AddressBook:
        return self.filtered if self.filtered is not None else self.carnet

    def _refresh_table(self) -> None:
        for row_id in self.tree.get_children():
            self.tree.delete(row_id)

        source = self._current_view()
        for nom in sorted(source, key=lambda n: n.casefold()):
            telephones, email = source[nom]
            self.tree.insert("", "end", values=(nom, ", ".join(telephones), email))

        self._set_status(f"{len(source)} contact(s) affiché(s)")

    def _ajouter_contact(self) -> None:
        nom = self.entry_nom.get()
        telephones = self._get_phones_list()
        email = self.entry_email.get()

        try:
            if ajouter_contact(self.carnet, nom, telephones, email):
                self.filtered = None
                self._refresh_table()
                self._set_status("✅ Contact ajouté")
            else:
                messagebox.showwarning("Doublon", "Un contact avec ce nom existe déjà.")
        except ValueError as error:
            messagebox.showerror("Erreur", str(error))

    def _ajouter_numero(self) -> None:
        nom = self.entry_nom.get().strip() or self._selected_name()
        if not nom:
            messagebox.showinfo("Information", "Sélectionnez un contact ou saisissez son nom.")
            return

        numero = simpledialog.askstring("Nouveau numéro", "Numéro à ajouter:")
        if numero is None:
            return

        try:
            if ajouter_numero(self.carnet, nom, numero):
                self._refresh_table()
                self._set_status("✅ Numéro ajouté")
            else:
                messagebox.showwarning("Information", "Contact introuvable ou numéro déjà présent.")
        except ValueError as error:
            messagebox.showerror("Erreur", str(error))

    def _supprimer_contact(self) -> None:
        nom = self.entry_nom.get().strip() or self._selected_name()
        if not nom:
            messagebox.showinfo("Information", "Sélectionnez un contact ou saisissez son nom.")
            return

        confirmation = messagebox.askyesno(
            "Confirmation",
            f"Voulez-vous vraiment supprimer le contact '{nom}' ?",
            icon="warning",
        )
        if not confirmation:
            self._set_status("Suppression annulée")
            return

        try:
            if supprimer_contact(self.carnet, nom):
                self.filtered = None
                self._refresh_table()
                self._set_status("✅ Contact supprimé")
            else:
                messagebox.showwarning("Information", "Contact introuvable.")
        except ValueError as error:
            messagebox.showerror("Erreur", str(error))

    def _rechercher(self) -> None:
        prefixe = self.entry_prefixe.get().strip()
        self.filtered = rechercher_par_prefixe(self.carnet, prefixe) if prefixe else None
        self._refresh_table()

    def _reset_filter(self) -> None:
        self.filtered = None
        self.entry_prefixe.delete(0, tk.END)
        self._refresh_table()

    def _save_json(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not path:
            return
        sauvegarder_en_json(self.carnet, path)
        self._set_status("✅ Sauvegarde JSON effectuée")

    def _load_json(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not path:
            return
        self.carnet = charger_depuis_json(path)
        self.filtered = None
        self._refresh_table()
        self._set_status("✅ Chargement JSON effectué")

    def _save_csv(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not path:
            return
        sauvegarder_en_csv(self.carnet, path)
        self._set_status("✅ Sauvegarde CSV effectuée")

    def _load_csv(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if not path:
            return
        self.carnet = charger_depuis_csv(path)
        self.filtered = None
        self._refresh_table()
        self._set_status("✅ Chargement CSV effectué")


def main() -> None:
    root = tk.Tk()
    CarnetApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
