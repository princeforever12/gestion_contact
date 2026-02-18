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
        self.root.geometry("1020x640")
        self.root.minsize(920, 560)

        self.carnet: AddressBook = {}
        self.filtered: AddressBook | None = None

        self._setup_style()
        self._build_ui()
        self._refresh_table()

    def _setup_style(self) -> None:
        self.root.configure(bg="#0b1220")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("App.TFrame", background="#0b1220")
        style.configure("Panel.TFrame", background="#111b2f")

        style.configure("Title.TLabel", background="#0b1220", foreground="#f8fafc", font=("Segoe UI", 20, "bold"))
        style.configure("Subtitle.TLabel", background="#0b1220", foreground="#9ca3af", font=("Segoe UI", 10))

        style.configure("PanelTitle.TLabel", background="#111b2f", foreground="#e5e7eb", font=("Segoe UI", 10, "bold"))
        style.configure("PanelText.TLabel", background="#111b2f", foreground="#cbd5e1", font=("Segoe UI", 10))

        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("Action.TButton", font=("Segoe UI", 10), padding=7)

        style.configure(
            "Treeview",
            background="#f8fafc",
            foreground="#0f172a",
            fieldbackground="#f8fafc",
            rowheight=30,
            font=("Segoe UI", 10),
        )
        style.map("Treeview", background=[("selected", "#bfdbfe")], foreground=[("selected", "#0f172a")])
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#e2e8f0", foreground="#0f172a")

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=14, style="App.TFrame")
        container.pack(fill="both", expand=True)

        self._build_header(container)
        self._build_top_panel(container)
        self._build_table(container)
        self._build_status_bar(container)

    def _build_header(self, parent: ttk.Frame) -> None:
        header = ttk.Frame(parent, style="App.TFrame")
        header.pack(fill="x", pady=(0, 12))

        ttk.Label(header, text="📒 Carnet d'adresses", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Gérez vos contacts rapidement : ajout, recherche et sauvegarde en un clic.",
            style="Subtitle.TLabel",
        ).pack(anchor="w")

    def _build_top_panel(self, parent: ttk.Frame) -> None:
        panel = ttk.Frame(parent, style="Panel.TFrame", padding=12)
        panel.pack(fill="x", pady=(0, 10))

        ttk.Label(panel, text="Actions", style="PanelTitle.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 8))

        ttk.Button(panel, text="➕ Ajouter contact", style="Accent.TButton", command=self._open_add_contact_dialog).grid(
            row=1, column=0, padx=(0, 6), pady=2
        )
        ttk.Button(panel, text="☎ Ajouter numéro", style="Action.TButton", command=self._ajouter_numero).grid(
            row=1, column=1, padx=6, pady=2
        )
        ttk.Button(panel, text="🗑 Supprimer", style="Action.TButton", command=self._supprimer_contact).grid(
            row=1, column=2, padx=6, pady=2
        )

        ttk.Separator(panel, orient="vertical").grid(row=1, column=3, sticky="ns", padx=12)

        ttk.Label(panel, text="Recherche préfixe", style="PanelText.TLabel").grid(row=1, column=4, padx=(0, 6))
        self.entry_prefixe = ttk.Entry(panel, width=24)
        self.entry_prefixe.grid(row=1, column=5, padx=(0, 6))
        ttk.Button(panel, text="Rechercher", style="Action.TButton", command=self._rechercher).grid(row=1, column=6, padx=4)
        ttk.Button(panel, text="Tout afficher", style="Action.TButton", command=self._reset_filter).grid(row=1, column=7, padx=4)

        ttk.Separator(panel, orient="vertical").grid(row=1, column=8, sticky="ns", padx=12)

        io_frame = ttk.Frame(panel, style="Panel.TFrame")
        io_frame.grid(row=1, column=9, columnspan=4, sticky="w")
        ttk.Button(io_frame, text="Sauver JSON", style="Action.TButton", command=self._save_json).grid(row=0, column=0, padx=3, pady=2)
        ttk.Button(io_frame, text="Charger JSON", style="Action.TButton", command=self._load_json).grid(row=0, column=1, padx=3, pady=2)
        ttk.Button(io_frame, text="Sauver CSV", style="Action.TButton", command=self._save_csv).grid(row=1, column=0, padx=3, pady=2)
        ttk.Button(io_frame, text="Charger CSV", style="Action.TButton", command=self._load_csv).grid(row=1, column=1, padx=3, pady=2)

    def _build_table(self, parent: ttk.Frame) -> None:
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill="both", expand=True)

        columns = ("nom", "telephones", "email")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("nom", text="Nom")
        self.tree.heading("telephones", text="Téléphones")
        self.tree.heading("email", text="Email")
        self.tree.column("nom", width=230, anchor="w")
        self.tree.column("telephones", width=320, anchor="w")
        self.tree.column("email", width=340, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _build_status_bar(self, parent: ttk.Frame) -> None:
        self.status_var = tk.StringVar(value="Prêt")
        bar = ttk.Frame(parent, style="App.TFrame")
        bar.pack(fill="x", pady=(10, 0))
        ttk.Label(bar, textvariable=self.status_var, style="Subtitle.TLabel").pack(anchor="w")

    def _set_status(self, message: str) -> None:
        self.status_var.set(message)

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
            self.tree.insert("", "end", values=(nom, " ".join(telephones), email))

        self._set_status(f"{len(source)} contact(s) affiché(s)")

    def _parse_phone_input(self, raw: str) -> list[str]:
        """Numéros séparés par espace, ex: '0611223344 0788990011'."""
        return [item.strip() for item in raw.split() if item.strip()]

    def _open_add_contact_dialog(self) -> None:
        dialog = tk.Toplevel(self.root)
        dialog.title("Ajouter un contact")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.geometry("460x220")
        dialog.resizable(False, False)

        frame = ttk.Frame(dialog, padding=14)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Nom").grid(row=0, column=0, sticky="w", pady=(0, 4))
        entry_nom = ttk.Entry(frame, width=48)
        entry_nom.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(frame, text="Téléphones (séparés par espace)").grid(row=2, column=0, sticky="w", pady=(0, 4))
        entry_phones = ttk.Entry(frame, width=48)
        entry_phones.grid(row=3, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(frame, text="Email").grid(row=4, column=0, sticky="w", pady=(0, 4))
        entry_email = ttk.Entry(frame, width=48)
        entry_email.grid(row=5, column=0, sticky="ew", pady=(0, 10))

        def submit() -> None:
            nom = entry_nom.get().strip()
            telephones = self._parse_phone_input(entry_phones.get())
            email = entry_email.get().strip()
            try:
                if ajouter_contact(self.carnet, nom, telephones, email):
                    self.filtered = None
                    self._refresh_table()
                    self._set_status("✅ Contact ajouté")
                    dialog.destroy()
                else:
                    messagebox.showwarning("Doublon", "Un contact avec ce nom existe déjà.", parent=dialog)
            except ValueError as error:
                messagebox.showerror("Erreur", str(error), parent=dialog)

        actions = ttk.Frame(frame)
        actions.grid(row=6, column=0, sticky="e")
        ttk.Button(actions, text="Annuler", command=dialog.destroy).pack(side="left", padx=6)
        ttk.Button(actions, text="Ajouter", style="Accent.TButton", command=submit).pack(side="left")

        entry_nom.focus_set()

    def _ajouter_numero(self) -> None:
        nom = self._selected_name() or simpledialog.askstring("Contact", "Nom du contact:", parent=self.root)
        if not nom:
            self._set_status("Ajout numéro annulé")
            return

        numero = simpledialog.askstring(
            "Ajouter numéro",
            "Nouveau numéro (un seul numéro, sans virgule):",
            parent=self.root,
        )
        if numero is None:
            self._set_status("Ajout numéro annulé")
            return

        try:
            if ajouter_numero(self.carnet, nom, numero):
                self._refresh_table()
                self._set_status("✅ Numéro ajouté")
            else:
                messagebox.showwarning("Information", "Contact introuvable ou numéro déjà présent.", parent=self.root)
        except ValueError as error:
            messagebox.showerror("Erreur", str(error), parent=self.root)

    def _supprimer_contact(self) -> None:
        nom = self._selected_name() or simpledialog.askstring("Supprimer", "Nom du contact à supprimer:", parent=self.root)
        if not nom:
            self._set_status("Suppression annulée")
            return

        confirmation = messagebox.askyesno(
            "Confirmation",
            f"Voulez-vous vraiment supprimer le contact '{nom}' ?",
            icon="warning",
            parent=self.root,
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
                messagebox.showwarning("Information", "Contact introuvable.", parent=self.root)
        except ValueError as error:
            messagebox.showerror("Erreur", str(error), parent=self.root)

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
