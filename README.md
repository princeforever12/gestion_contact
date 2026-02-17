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
# 📒 Carnet d'adresses en Python

Un mini-projet propre, clair et **présentable à l'oral**, basé exactement sur la consigne :

- structure de données : **dictionnaire**
- clé : **nom**
- valeur : **tuple `(telephone, email)`**
- fonctionnalités : **ajouter**, **supprimer**, **rechercher**, **afficher tous les contacts**

---

## 🎯 Objectifs pédagogiques

Ce projet montre que ont sais :

1. manipuler un dictionnaire Python,
2. stocker des données structurées avec des tuples,
3. découper ton code en fonctions réutilisables,
4. valider des entrées utilisateur,
5. tester automatiquement le code.

---

## 🧠 Structure des données

```python
carnet = {
    "Alice Martin": ("+33 6 12 34 56 78", "alice@mail.com"),
    "Bob Dupont": ("01 44 55 66 77", "bob@ecole.fr"),
}
```

- `"Alice Martin"` → clé du dictionnaire
- `("+33 6 12 34 56 78", "alice@mail.com")` → tuple `(telephone, email)`

---

## ⚙️ Fonctions principales

Le fichier `address_book.py` contient :

- `ajouter_contact(carnet, nom, telephone, email)`
- `supprimer_contact(carnet, nom)`
- `rechercher_contact(carnet, nom)`
- `afficher_tous_les_contacts(carnet)`
- `executer_application()` : menu console interactif

Bonus qualité :
- normalisation des noms,
- validation basique du téléphone,
- validation basique de l'email,
- tri alphabétique à l'affichage.

---

## ▶️ Lancer le programme

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
- thème moderne (palette plus élégante, boutons plus lisibles)
- formulaire d'ajout qui apparaît en popup (pas affiché en permanence)
- numéros saisis séparés par espace (ex: `0611223344 0788990011`)
- thème moderne (couleurs, typographie plus lisible)
- tableau de contacts avec colonnes (nom, téléphones, email)
- sélection directe dans la liste pour supprimer/ajouter un numéro
- barre d'actions claire (recherche, sauvegarde/chargement)
- barre de statut en bas pour feedback rapide
- confirmation avant suppression (sécurité UX)
Fonctionnalités GUI :
- formulaire pour ajouter contact
- ajout d'un numéro à un contact
- suppression d'un contact
- recherche partielle par préfixe
- sauvegarde/chargement JSON et CSV via fenêtres de fichiers

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
Tu verras un menu :

1. Ajouter un contact
2. Supprimer un contact
3. Rechercher un contact
4. Afficher tous les contacts
5. Quitter

---

## ✅ Lancer les tests

```bash
pytest -q
```

Les tests vérifient :
- ajout + recherche,
- refus des doublons,
- suppression,
- affichage trié,
- erreur sur email invalide.

---

## 🗣️ Idée de présentation (pour impressionner le prof)

ont peux dire :

> "J'ai respecté la consigne de base avec un dictionnaire de tuples, puis j'ai amélioré la robustesse : validation des données, fonctions claires, tri des contacts et tests automatisés. Le code est modulaire et prêt à évoluer (sauvegarde fichier, interface graphique, etc.)."

---

## 🚀 Pistes d'amélioration

- sauvegarder les contacts dans un fichier JSON/CSV,
- ajouter une recherche partielle (par début de nom),
- gérer plusieurs numéros par contact,
- créer une interface graphique avec Tkinter.

---

## 👨‍💻 Auteur

Projet réalisé pour un devoir de programmation Python.
