---
name: importer-livre-quetes
description: Transforme un livre de quêtes HeroQuest en PDF (dossier _ressource/, souvent un scan sans texte) en une campagne Markdown CampagneNN avec 01-regles, 02-quetes (une fiche par quête, index, conséquences), 03-suivi (fiche de suivi) et README. À utiliser dès que l'utilisateur donne un PDF de _ressource comme source pour générer une campagne ou des fiches de quêtes, ou demande d'importer, lire, passer à l'OCR ou synthétiser un livre de quêtes (Le Mage du Miroir, La Horde des Ogres, L'Horreur des glaces...), même sans citer ce skill.
---

# Importer un livre de quêtes PDF dans une campagne

Produit, à partir d'un PDF de `_ressource/`, une campagne organisée comme Campagne01 à 04. Les conventions de structure sont celles du skill `structurer-campagne` ; ce skill couvre la lecture du PDF et la rédaction des fiches.

## Principe : synthèse, pas recopie

Un livre de quêtes du commerce est un contenu protégé. Le PDF reste la source de référence (jamais modifié ni déplacé). Les fichiers Markdown sont des **fiches reformulées** : garder les règles, chiffres, récompenses, pièges, monstres et statistiques, mais ne pas recopier les textes narratifs ni les messages « à lire à voix haute » (les résumer en une ou deux phrases). Renvoyer vers les pages du PDF pour les cartes, illustrations et textes complets.

## Procédure

1. **Cadrer.** Lire `CLAUDE.md` et le `README.md` racine. Choisir le dossier de sortie : prochain `CampagneNN` libre, ou le numéro que porte le livre ; annoncer l'hypothèse en une ligne.
2. **Inventorier le PDF.** `pdfinfo`, `pdffonts` (tableau vide = scan sans texte), `pdftotext` sur une page. PDF avec texte : `pdftotext -layout`. Scan : étape 3.
3. **OCR.** 
   ```
   python .claude/skills/importer-livre-quetes/scripts/ocr_pdf.py "_ressource/.../Livre.pdf" --out /tmp/livre --contact
   ```
   Le script rend chaque page, détecte son orientation, lit en français (données de langue téléchargées si besoin) et écrit `ocr/page-NNN.txt`. Il s'arrête avant la limite de temps des outils : **relancer la même commande** tant qu'il reste des pages. Ne pas le lancer en arrière-plan : le processus est tué à la fin de la commande. `--contact` crée `contact.jpg`, une planche-contact pour repérer la structure (couverture, règles, quêtes, artéfacts, monstres, création).
4. **Lire par blocs** : règles du pack, éléments de jeu, message de Mentor, chaque quête, conclusion, artéfacts, tableau des monstres.
5. **Relire visuellement** (`view` sur `pages/page-NNN.png`) tout ce que l'OCR rend mal : encadrés de statistiques, tableaux, cartes d'artéfacts, lettres de notes (A, B, C...) perdues, pages dont le texte est tourné. Ne jamais déduire un chiffre d'un OCR douteux.
6. **Repérer l'ordre carte / notes.** Dans Le Mage du Miroir, la carte précède la page de notes de sa quête, et le numéro de page du PDF est l'index de page + 1. Les cartes ne se transcrivent pas : les fiches donnent les pages du PDF et reprennent les lettres de notes.
7. **Rédiger** :
   - `01-regles/` : règles propres au pack, éléments de jeu, objets et artéfacts (avec boutique), monstres (tableau et personnages nommés), un fichier par ensemble cohérent.
   - `02-quetes/NN-slug.md` : mission en deux phrases, début, fin et monstres errants, tableau « Réf. / Contenu » des notes, récompense et suite. Une quête en deux parties donne deux fiches.
   - `02-quetes/index.md` avec les pages du PDF, et `consequences.md` (récompenses, dangers, éléments clés ; ne rien inventer si le livre ne décrit pas d'échec).
   - `03-suivi/fiche-campagne.md` : indicateurs réellement présents (objets avec utilisations restantes, alliés, boutique, résultats par quête).
   - `README.md` : source, méthode (OCR puis relecture), ce qui n'est pas transcrit, points à arbitrer.
8. **Vérifier** : `python .claude/skills/structurer-campagne/scripts/verifier_campagne.py CampagneNN`.
9. **Rendre compte** : fichiers créés, hypothèse de numérotation, ce qui a été relu visuellement, points à arbitrer.

## Points de vigilance

- Les extensions s'appuient sur le jeu de base : ne pas inventer les statistiques ou effets de cartes qui n'y sont pas (renvoyer au jeu de base dans les points à arbitrer).
- Noter les incohérences d'impression (renvoi vers une lettre de pièce qui est la pièce elle-même, ligne de monstres errants partagée entre deux quêtes) au lieu de les corriger.
- Un autre livre sur le même titre peut exister dans `_ressource/` (par exemple l'édition de 1989) : ne pas le comparer sans demande, le signaler dans le README.
- Un PDF de plusieurs dizaines de pages : lire d'abord le texte OCR, ne rendre en image que les pages utiles (environ 1 600 jetons par page).
- Préserver les originaux ; ne pas committer sauf demande.
