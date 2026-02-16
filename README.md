# 📒 Carnet d'adresses en Python

Un mini-projet propre, clair et **présentable à l'oral**, basé exactement sur la consigne :

- structure de données : **dictionnaire**
- clé : **nom**
- valeur : **tuple `(telephone, email)`**
- fonctionnalités : **ajouter**, **supprimer**, **rechercher**, **afficher tous les contacts**

---

## 🎯 Objectifs pédagogiques

Ce projet montre que tu sais :

1. manipuler un dictionnaire Python,
2. stocker des données structurées avec des tuples,
3. découper ton code en fonctions réutilisables,
4. valider des entrées utilisateur,
5. tester automatiquement ton code.

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

Tu peux dire :

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
