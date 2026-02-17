# 📒 Carnet d'adresses Python (version avancée)

Projet Python scolaire **propre + impressionnant** ✅

Ce carnet d'adresses respecte la base demandée (dictionnaire) tout en ajoutant des fonctionnalités avancées :

- stockage des contacts dans un `dict`
- clé : `nom`
- valeur : tuple `(telephones, email)` où `telephones` est un tuple de numéros
- ajout / suppression / recherche / affichage
- sauvegarde et chargement en **JSON** et **CSV**
- **recherche partielle** (par début de nom)
- **interface graphique Tkinter**

---

## 🧱 Structure des données

```python
carnet = {
    "Alice Martin": (("+33 6 12 34 56 78", "01 45 00 00 00"), "alice@mail.com"),
    "Bob Dupont": (("01 44 55 66 77",), "bob@ecole.fr"),
}
```

---

## ⚙️ Fonctions principales (`address_book.py`)

- `ajouter_contact(carnet, nom, telephones, email)`
- `ajouter_numero(carnet, nom, nouveau_numero)`
- `supprimer_contact(carnet, nom)`
- `rechercher_contact(carnet, nom)`
- `rechercher_par_prefixe(carnet, prefixe)`
- `afficher_tous_les_contacts(carnet)`
- `sauvegarder_en_json(...)` / `charger_depuis_json(...)`
- `sauvegarder_en_csv(...)` / `charger_depuis_csv(...)`

Il y a aussi une application console via `executer_application()`.

---

## ▶️ Exécuter l'application console

```bash
python3 address_book.py
```

Menu disponible :
1. Ajouter un contact
2. Ajouter un numéro
3. Supprimer
4. Rechercher exact
5. Rechercher par préfixe
6. Afficher tous
7. Sauvegarder JSON
8. Sauvegarder CSV
9. Charger JSON
10. Charger CSV
11. Quitter

---

## 🖼️ Exécuter l'interface graphique (Tkinter)

```bash
python3 gui_tkinter.py
```

Nouvelle interface visuelle :
- thème moderne (couleurs, typographie plus lisible)
- tableau de contacts avec colonnes (nom, téléphones, email)
- sélection directe dans la liste pour supprimer/ajouter un numéro
- barre d'actions claire (recherche, sauvegarde/chargement)
- barre de statut en bas pour feedback rapide
- confirmation avant suppression (sécurité UX)

---

## ✅ Lancer les tests

```bash
pytest -q
```

Les tests couvrent :
- ajout/recherche contact avec plusieurs numéros
- ajout de numéro
- recherche partielle
- persistance JSON
- persistance CSV
- validations
- affichage trié

---

## 🗣️ Pitch rapide pour impressionner le prof

> "J'ai commencé avec la consigne minimale (dictionnaire de tuples), puis j'ai transformé ça en mini-application complète : gestion multi-numéros, persistance JSON/CSV, recherche intelligente par préfixe, interface console et interface graphique Tkinter, avec tests automatisés pour valider la fiabilité."

---

## 🚀 Idées bonus

- export/import Excel
- tri par domaine email
- statistiques (nombre de contacts, indicatifs, etc.)
- packaging en exécutable
