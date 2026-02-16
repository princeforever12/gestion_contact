"""Carnet d'adresses simple en Python.

Les contacts sont stockés dans un dictionnaire:
- clé   : nom (str)
- valeur: tuple (telephone, email)
"""

from __future__ import annotations

from typing import Dict, Optional, Tuple

ContactValue = Tuple[str, str]
AddressBook = Dict[str, ContactValue]


def _normalize_name(name: str) -> str:
    """Nettoie le nom pour éviter les doublons de type espaces."""
    normalized = " ".join(name.strip().split())
    if not normalized:
        raise ValueError("Le nom ne peut pas être vide.")
    return normalized


def _validate_phone(phone: str) -> str:
    """Validation légère d'un numéro de téléphone."""
    phone = phone.strip()
    allowed = set("+0123456789 -()")
    if not phone or any(ch not in allowed for ch in phone):
        raise ValueError("Numéro de téléphone invalide.")
    return phone


def _validate_email(email: str) -> str:
    """Validation minimale d'un email."""
    email = email.strip()
    if "@" not in email or email.startswith("@") or email.endswith("@"):
        raise ValueError("Adresse email invalide.")
    local, domain = email.split("@", 1)
    if not local or "." not in domain:
        raise ValueError("Adresse email invalide.")
    return email


def ajouter_contact(carnet: AddressBook, nom: str, telephone: str, email: str) -> bool:
    """Ajoute un contact.

    Retourne:
        True si le contact a été ajouté,
        False si un contact avec le même nom existe déjà.
    """
    nom = _normalize_name(nom)
    if nom in carnet:
        return False

    carnet[nom] = (_validate_phone(telephone), _validate_email(email))
    return True


def supprimer_contact(carnet: AddressBook, nom: str) -> bool:
    """Supprime un contact par son nom."""
    nom = _normalize_name(nom)
    if nom not in carnet:
        return False
    del carnet[nom]
    return True


def rechercher_contact(carnet: AddressBook, nom: str) -> Optional[ContactValue]:
    """Recherche un contact par son nom exact et retourne son tuple (telephone, email)."""
    nom = _normalize_name(nom)
    return carnet.get(nom)


def afficher_tous_les_contacts(carnet: AddressBook) -> str:
    """Retourne une représentation formatée de tous les contacts triés par nom."""
    if not carnet:
        return "Carnet vide."

    lines = ["\n=== Liste des contacts ==="]
    for nom in sorted(carnet, key=lambda n: n.casefold()):
        telephone, email = carnet[nom]
        lines.append(f"- {nom}: 📞 {telephone} | ✉️ {email}")
    return "\n".join(lines)


def _menu() -> str:
    return (
        "\nCarnet d'adresses - Menu\n"
        "1) Ajouter un contact\n"
        "2) Supprimer un contact\n"
        "3) Rechercher un contact\n"
        "4) Afficher tous les contacts\n"
        "5) Quitter\n"
        "Votre choix: "
    )


def executer_application() -> None:
    """Lance une interface console simple."""
    carnet: AddressBook = {}
    print("Bienvenue dans ton carnet d'adresses ✨")

    while True:
        choix = input(_menu()).strip()

        try:
            if choix == "1":
                nom = input("Nom: ")
                telephone = input("Téléphone: ")
                email = input("Email: ")
                if ajouter_contact(carnet, nom, telephone, email):
                    print("✅ Contact ajouté.")
                else:
                    print("⚠️ Un contact avec ce nom existe déjà.")

            elif choix == "2":
                nom = input("Nom à supprimer: ")
                if supprimer_contact(carnet, nom):
                    print("✅ Contact supprimé.")
                else:
                    print("⚠️ Contact introuvable.")

            elif choix == "3":
                nom = input("Nom à rechercher: ")
                contact = rechercher_contact(carnet, nom)
                if contact is None:
                    print("⚠️ Contact introuvable.")
                else:
                    telephone, email = contact
                    print(f"✅ {nom.strip()} -> 📞 {telephone} | ✉️ {email}")

            elif choix == "4":
                print(afficher_tous_les_contacts(carnet))

            elif choix == "5":
                print("Au revoir 👋")
                break

            else:
                print("Choix invalide. Essaie encore.")

        except ValueError as error:
            print(f"❌ Erreur: {error}")


if __name__ == "__main__":
    executer_application()
