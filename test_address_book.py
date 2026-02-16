import pytest

from address_book import (
    ajouter_contact,
    afficher_tous_les_contacts,
    rechercher_contact,
    supprimer_contact,
)


def test_ajouter_et_rechercher_contact():
    carnet = {}

    ajoute = ajouter_contact(carnet, "Alice Martin", "+33 6 12 34 56 78", "alice@mail.com")

    assert ajoute is True
    assert rechercher_contact(carnet, "Alice Martin") == (
        "+33 6 12 34 56 78",
        "alice@mail.com",
    )


def test_ajout_doublon_refuse():
    carnet = {"Alice Martin": ("+33 6 12 34 56 78", "alice@mail.com")}

    ajoute = ajouter_contact(carnet, "Alice Martin", "0102030405", "autre@mail.com")

    assert ajoute is False
    assert len(carnet) == 1


def test_supprimer_contact():
    carnet = {"Bob": ("0102030405", "bob@mail.com")}

    supprime = supprimer_contact(carnet, "Bob")

    assert supprime is True
    assert carnet == {}


def test_affichage_contacts_tries():
    carnet = {
        "zoe": ("1", "zoe@mail.com"),
        "Alice": ("2", "alice@mail.com"),
    }

    affichage = afficher_tous_les_contacts(carnet)

    lignes = [ligne for ligne in affichage.splitlines() if ligne.strip()]
    assert "Alice" in lignes[1]
    assert "zoe" in lignes[2]


def test_email_invalide_declenche_erreur():
    carnet = {}

    with pytest.raises(ValueError):
        ajouter_contact(carnet, "Bad Mail", "0102030405", "badmail.com")
