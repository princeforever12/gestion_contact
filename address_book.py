"""Carnet d'adresses avec stockage dict[nom] -> (telephones, email).

- nom: str
- telephones: tuple[str, ...] (plusieurs numéros)
- email: str
"""

from __future__ import annotations

import csv
import json
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


def _menu() -> str:
    return (
        "\nCarnet d'adresses - Menu\n"
        "1) Ajouter un contact\n"
        "2) Ajouter un numéro à un contact\n"
        "3) Supprimer un contact\n"
        "4) Rechercher un contact (nom exact)\n"
        "5) Rechercher des contacts par préfixe\n"
        "6) Afficher tous les contacts\n"
        "7) Sauvegarder en JSON\n"
        "8) Sauvegarder en CSV\n"
        "9) Charger depuis JSON\n"
        "10) Charger depuis CSV\n"
        "11) Quitter\n"
        "Votre choix: "
    )


def executer_application() -> None:
    carnet: AddressBook = {}
    print("Bienvenue dans ton carnet d'adresses ✨")

    while True:
        choix = input(_menu()).strip()

        try:
            if choix == "1":
                nom = input("Nom: ")
                telephones = [p.strip() for p in input("Téléphones (séparés par ','): ").split(",") if p.strip()]
                email = input("Email: ")
                if ajouter_contact(carnet, nom, telephones, email):
                    print("✅ Contact ajouté.")
                else:
                    print("⚠️ Un contact avec ce nom existe déjà.")

            elif choix == "2":
                nom = input("Nom du contact: ")
                numero = input("Nouveau numéro: ")
                if ajouter_numero(carnet, nom, numero):
                    print("✅ Numéro ajouté.")
                else:
                    print("⚠️ Contact introuvable ou numéro déjà présent.")

            elif choix == "3":
                nom = input("Nom à supprimer: ")
                print("✅ Contact supprimé." if supprimer_contact(carnet, nom) else "⚠️ Contact introuvable.")

            elif choix == "4":
                nom = input("Nom à rechercher: ")
                contact = rechercher_contact(carnet, nom)
                if contact is None:
                    print("⚠️ Contact introuvable.")
                else:
                    telephones, email = contact
                    print(f"✅ {nom.strip()} -> 📞 {', '.join(telephones)} | ✉️ {email}")

            elif choix == "5":
                prefixe = input("Début du nom: ")
                resultats = rechercher_par_prefixe(carnet, prefixe)
                if not resultats:
                    print("⚠️ Aucun résultat.")
                else:
                    print(afficher_tous_les_contacts(resultats))

            elif choix == "6":
                print(afficher_tous_les_contacts(carnet))

            elif choix == "7":
                chemin = input("Chemin JSON [contacts.json]: ").strip() or "contacts.json"
                sauvegarder_en_json(carnet, chemin)
                print(f"✅ Sauvegardé dans {chemin}")

            elif choix == "8":
                chemin = input("Chemin CSV [contacts.csv]: ").strip() or "contacts.csv"
                sauvegarder_en_csv(carnet, chemin)
                print(f"✅ Sauvegardé dans {chemin}")

            elif choix == "9":
                chemin = input("Chemin JSON [contacts.json]: ").strip() or "contacts.json"
                carnet = charger_depuis_json(chemin)
                print(f"✅ {len(carnet)} contact(s) chargé(s).")

            elif choix == "10":
                chemin = input("Chemin CSV [contacts.csv]: ").strip() or "contacts.csv"
                carnet = charger_depuis_csv(chemin)
                print(f"✅ {len(carnet)} contact(s) chargé(s).")

            elif choix == "11":
                print("Au revoir 👋")
                break

            else:
                print("Choix invalide. Essaie encore.")

        except (ValueError, KeyError) as error:
            print(f"❌ Erreur: {error}")


if __name__ == "__main__":
    executer_application()
