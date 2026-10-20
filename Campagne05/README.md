# Campagne 05 - Le Mage du Miroir

## État

La campagne est organisée à partir d'un seul livre de quêtes, `_ressource/Livre quete 2023/Livre des Quetes 5 -  Le Mage du Miroir.pdf` (scan de 40 pages, sans texte numérique). Le PDF est conservé tel quel. Les fichiers Markdown ci-dessous sont des synthèses reformulées, pas une reproduction du livre : le texte intégral, les illustrations et les cartes restent dans le PDF.

## Structure de travail

- `01-regles/regles-campagne.md` : principes, règles propres au pack, fin de campagne.
- `01-regles/elements-de-jeu.md` : tuiles et éléments de jeu, transformation en loup-garou.
- `01-regles/objets-et-artefacts.md` : boutique de l'alchimiste, artéfacts, autres objets.
- `01-regles/monstres.md` : monstres du pack, personnages nommés, monstres errants.
- `02-quetes/index.md` : les dix quêtes, avec les pages du PDF (carte et notes).
- `02-quetes/consequences.md` : récompenses et suites par quête.
- `03-suivi/fiche-campagne.md` : état de la campagne pendant les parties.
- `04-plateaux/` : cartes converties pour le jeu web Donjon (image, description JSON, `questNNN.js`). Seule la quête 1 est faite.

## Source et méthode

- Le PDF est un scan : le texte a été obtenu par reconnaissance de caractères (OCR) en français, puis relu sur les pages scannées pour les statistiques, les artéfacts et les lettres de notes. Les fiches restent à confronter au livre avant impression.
- Les cartes de quête (pages 14, 16, 18, 20, 22, 24, 26, 28, 30 et 32) ne sont pas transcrites : les notes de chaque fiche renvoient aux lettres de ces cartes.
- Le dépôt contient aussi l'ancien livre de 1989, « Le Mage du Miroir (Pack de l'Elfe) » : il n'a pas été comparé à cette version de 2023.

## Points à arbitrer avant impression définitive

Le livre ne décrit pas de conséquence d'échec ni de règle pour la mort de l'elfe en solo. Une référence de trappe de la quête 7 semble erronée. Les effets des cartes du jeu de base (Élixir de vie, trousse à outils, potion d'héroïsme) et les statistiques des monstres du jeu de base ne sont pas dans le livre. La liste est reprise dans `01-regles/regles-campagne.md`, `01-regles/objets-et-artefacts.md`, `01-regles/monstres.md` et `02-quetes/consequences.md`.
