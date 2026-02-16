from pathlib import Path

import pytest

from address_book import (
    ajouter_contact,
    ajouter_numero,
    afficher_tous_les_contacts,
    charger_depuis_csv,
    charger_depuis_json,
    rechercher_contact,
    rechercher_par_prefixe,
    sauvegarder_en_csv,
    sauvegarder_en_json,
    supprimer_contact,
)


def test_ajouter_et_rechercher_contact_avec_plusieurs_numeros():
    carnet = {}

    ajoute = ajouter_contact(
        carnet,
        "Alice Martin",
        ["+33 6 12 34 56 78", "01 45 00 00 00"],
        "alice@mail.com",
    )

    assert ajoute is True
    assert rechercher_contact(carnet, "Alice Martin") == (
        ("+33 6 12 34 56 78", "01 45 00 00 00"),
        "alice@mail.com",
    )


def test_ajouter_numero_sur_contact_existant():
    carnet = {"Bob": (("0102030405",), "bob@mail.com")}

    ok = ajouter_numero(carnet, "Bob", "06 11 22 33 44")

    assert ok is True
    assert carnet["Bob"][0] == ("0102030405", "06 11 22 33 44")


def test_supprimer_contact():
    carnet = {"Bob": (("0102030405",), "bob@mail.com")}

    supprime = supprimer_contact(carnet, "Bob")

    assert supprime is True
    assert carnet == {}


def test_recherche_partielle_par_prefixe():
    carnet = {
        "Alice Martin": (("1",), "alice@mail.com"),
        "Alix": (("2",), "alix@mail.com"),
        "Benoit": (("3",), "benoit@mail.com"),
    }

    resultats = rechercher_par_prefixe(carnet, "Ali")

    assert list(resultats.keys()) == ["Alice Martin", "Alix"]


def test_persistance_json(tmp_path: Path):
    carnet = {"Zoé": (("01 02 03 04 05", "06 07 08 09 10"), "zoe@mail.com")}
    path = tmp_path / "contacts.json"

    sauvegarder_en_json(carnet, str(path))
    recharge = charger_depuis_json(str(path))

    assert recharge == carnet


def test_persistance_csv(tmp_path: Path):
    carnet = {
        "Alice": (("1", "2"), "alice@mail.com"),
        "Bob": (("3",), "bob@mail.com"),
    }
    path = tmp_path / "contacts.csv"

    sauvegarder_en_csv(carnet, str(path))
    recharge = charger_depuis_csv(str(path))

    assert recharge == carnet


def test_email_invalide_declenche_erreur():
    carnet = {}

    with pytest.raises(ValueError):
        ajouter_contact(carnet, "Bad Mail", ["0102030405"], "badmail.com")


def test_affichage_contacts_tries_et_multinumero():
    carnet = {
        "zoe": (("1", "9"), "zoe@mail.com"),
        "Alice": (("2",), "alice@mail.com"),
    }

    affichage = afficher_tous_les_contacts(carnet)
    lignes = [ligne for ligne in affichage.splitlines() if ligne.strip()]

    assert "Alice" in lignes[1]
    assert "zoe" in lignes[2]
    assert "1, 9" in affichage
