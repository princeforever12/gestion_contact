"""Carnet d'adresses avec stockage dict[nom] -> (telephones, email).

- nom: str
- telephones: tuple[str, ...] (plusieurs numéros)
- email: str
"""

from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PhoneNumbers = Tuple[str, ...]
ContactValue = Tuple[PhoneNumbers, str]
AddressBook = Dict[str, ContactValue]


def _normalize_name(name: str) -> str:
    normalized = " ".join(name.strip().split())
    if not normalized:
        raise ValueError("Le nom ne peut pas être vide.")
    return normalized


def _validate_phone(phone: str) -> str:
    phone = phone.strip()
    allowed = set("+0123456789 -()")
    if not phone or any(ch not in allowed for ch in phone):
        raise ValueError(f"Numéro de téléphone invalide: {phone!r}")
    return phone


def _validate_phones(phones: List[str] | Tuple[str, ...]) -> PhoneNumbers:
    if not phones:
        raise ValueError("Au moins un numéro est requis.")
    normalized: List[str] = []
    for phone in phones:
        clean = _validate_phone(phone)
        if clean not in normalized:
            normalized.append(clean)
    return tuple(normalized)


def _validate_email(email: str) -> str:
    email = email.strip()
    if "@" not in email or email.startswith("@") or email.endswith("@"):
        raise ValueError("Adresse email invalide.")
    local, domain = email.split("@", 1)
    if not local or "." not in domain:
        raise ValueError("Adresse email invalide.")
    return email


def ajouter_contact(carnet: AddressBook, nom: str, telephones: List[str] | Tuple[str, ...], email: str) -> bool:
    """Ajoute un contact. Retourne False si doublon de nom."""
    nom = _normalize_name(nom)
    if nom in carnet:
        return False
    carnet[nom] = (_validate_phones(telephones), _validate_email(email))
    return True


def ajouter_numero(carnet: AddressBook, nom: str, nouveau_numero: str) -> bool:
    """Ajoute un numéro à un contact existant, sans doublon."""
    nom = _normalize_name(nom)
    if nom not in carnet:
        return False

    telephones, email = carnet[nom]
    numero = _validate_phone(nouveau_numero)
    if numero in telephones:
        return False

    carnet[nom] = (telephones + (numero,), email)
    return True


def supprimer_contact(carnet: AddressBook, nom: str) -> bool:
    nom = _normalize_name(nom)
    if nom not in carnet:
        return False
    del carnet[nom]
    return True


def rechercher_contact(carnet: AddressBook, nom: str) -> Optional[ContactValue]:
    nom = _normalize_name(nom)
    return carnet.get(nom)


def rechercher_par_prefixe(carnet: AddressBook, prefixe: str) -> AddressBook:
    """Recherche partielle par début de nom (insensible à la casse)."""
    prefixe = prefixe.strip().casefold()
    if not prefixe:
        return {}

    resultats: AddressBook = {}
    for nom, valeur in carnet.items():
        if nom.casefold().startswith(prefixe):
            resultats[nom] = valeur
    return dict(sorted(resultats.items(), key=lambda item: item[0].casefold()))


def afficher_tous_les_contacts(carnet: AddressBook) -> str:
    if not carnet:
        return "Carnet vide."

    lines = ["=== Liste des contacts ==="]
    for nom in sorted(carnet, key=lambda n: n.casefold()):
        telephones, email = carnet[nom]
        numeros = ", ".join(telephones)
        lines.append(f"- {nom}: 📞 {numeros} | ✉️ {email}")
    return "\n".join(lines)


def sauvegarder_en_json(carnet: AddressBook, chemin: str) -> None:
    data = {
        nom: {"telephones": list(telephones), "email": email}
        for nom, (telephones, email) in carnet.items()
    }
    Path(chemin).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def charger_depuis_json(chemin: str) -> AddressBook:
    path = Path(chemin)
    if not path.exists():
        return {}

    raw = json.loads(path.read_text(encoding="utf-8"))
    carnet: AddressBook = {}
    for nom, payload in raw.items():
        carnet[_normalize_name(nom)] = (
            _validate_phones(payload["telephones"]),
            _validate_email(payload["email"]),
        )
    return carnet


def sauvegarder_en_csv(carnet: AddressBook, chemin: str) -> None:
    with Path(chemin).open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["nom", "telephones", "email"])
        for nom in sorted(carnet, key=lambda n: n.casefold()):
            telephones, email = carnet[nom]
            writer.writerow([nom, "|".join(telephones), email])


def charger_depuis_csv(chemin: str) -> AddressBook:
    path = Path(chemin)
    if not path.exists():
        return {}

    carnet: AddressBook = {}
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            telephones = tuple(filter(None, row["telephones"].split("|")))
            carnet[_normalize_name(row["nom"])] = (
                _validate_phones(telephones),
                _validate_email(row["email"]),
            )
    return carnet


def _draw_panel(title: str, lines: List[str]) -> str:
    width = min(max(shutil.get_terminal_size(fallback=(90, 24)).columns, 70), 110)
    inner_width = width - 4
    top = f"┌{'─' * (width - 2)}┐"
    bottom = f"└{'─' * (width - 2)}┘"
    title_line = f"│ {title[:inner_width].ljust(inner_width)} │"
    body = [f"│ {line[:inner_width].ljust(inner_width)} │" for line in lines]
    return "\n".join([top, title_line, f"├{'─' * (width - 2)}┤", *body, bottom])


def _menu() -> str:
    menu_lines = [
        "1) 👤 Ajouter un contact",
        "2) ☎️  Ajouter un numéro à un contact",
        "3) 🗑️  Supprimer un contact",
        "4) 🔎 Rechercher un contact (nom exact)",
        "5) 🔍 Rechercher des contacts par préfixe",
        "6) 📋 Afficher tous les contacts",
        "7) 💾 Sauvegarder en JSON",
        "8) 🧾 Sauvegarder en CSV",
        "9) 📂 Charger depuis JSON",
        "10) 📂 Charger depuis CSV",
        "11) 🚪 Quitter",
    ]
    return _draw_panel("Carnet d'adresses - Menu principal", menu_lines)


def _print_info(message: str) -> None:
    print(_draw_panel("Information", [message]))


def executer_application() -> None:
    carnet: AddressBook = {}
    print(
        _draw_panel(
            "Bienvenue ✨",
            [
                "Application Carnet d'adresses",
                "Astuce: lance gui_tkinter.py pour une interface graphique moderne.",
            ],
        )
    )

    while True:
        print()
        print(_menu())
        choix = input("\n👉 Votre choix: ").strip()

        try:
            if choix == "1":
                nom = input("Nom: ")
                telephones = [p.strip() for p in input("Téléphones (séparés par ','): ").split(",") if p.strip()]
                email = input("Email: ")
                if ajouter_contact(carnet, nom, telephones, email):
                    _print_info("✅ Contact ajouté.")
                else:
                    _print_info("⚠️ Un contact avec ce nom existe déjà.")

            elif choix == "2":
                nom = input("Nom du contact: ")
                numero = input("Nouveau numéro: ")
                if ajouter_numero(carnet, nom, numero):
                    _print_info("✅ Numéro ajouté.")
                else:
                    _print_info("⚠️ Contact introuvable ou numéro déjà présent.")

            elif choix == "3":
                nom = input("Nom à supprimer: ")
                confirmer = input(f"Voulez-vous vraiment supprimer '{nom.strip()}' ? (o/n): ").strip().lower()
                if confirmer not in {"o", "oui", "y", "yes"}:
                    _print_info("Suppression annulée.")
                else:
                    _print_info("✅ Contact supprimé." if supprimer_contact(carnet, nom) else "⚠️ Contact introuvable.")
                _print_info("✅ Contact supprimé." if supprimer_contact(carnet, nom) else "⚠️ Contact introuvable.")

            elif choix == "4":
                nom = input("Nom à rechercher: ")
                contact = rechercher_contact(carnet, nom)
                if contact is None:
                    _print_info("⚠️ Contact introuvable.")
                else:
                    telephones, email = contact
                    _print_info(f"✅ {nom.strip()} -> 📞 {', '.join(telephones)} | ✉️ {email}")

            elif choix == "5":
                prefixe = input("Début du nom: ")
                resultats = rechercher_par_prefixe(carnet, prefixe)
                if not resultats:
                    _print_info("⚠️ Aucun résultat.")
                else:
                    print(_draw_panel("Résultats de recherche", afficher_tous_les_contacts(resultats).splitlines()))

            elif choix == "6":
                print(_draw_panel("Tous les contacts", afficher_tous_les_contacts(carnet).splitlines()))

            elif choix == "7":
                chemin = input("Chemin JSON [contacts.json]: ").strip() or "contacts.json"
                sauvegarder_en_json(carnet, chemin)
                _print_info(f"✅ Sauvegardé dans {chemin}")

            elif choix == "8":
                chemin = input("Chemin CSV [contacts.csv]: ").strip() or "contacts.csv"
                sauvegarder_en_csv(carnet, chemin)
                _print_info(f"✅ Sauvegardé dans {chemin}")

            elif choix == "9":
                chemin = input("Chemin JSON [contacts.json]: ").strip() or "contacts.json"
                carnet = charger_depuis_json(chemin)
                _print_info(f"✅ {len(carnet)} contact(s) chargé(s).")

            elif choix == "10":
                chemin = input("Chemin CSV [contacts.csv]: ").strip() or "contacts.csv"
                carnet = charger_depuis_csv(chemin)
                _print_info(f"✅ {len(carnet)} contact(s) chargé(s).")

            elif choix == "11":
                _print_info("Au revoir 👋")
                break

            else:
                _print_info("Choix invalide. Essaie encore.")

        except (ValueError, KeyError) as error:
            _print_info(f"❌ Erreur: {error}")


if __name__ == "__main__":
    executer_application()
