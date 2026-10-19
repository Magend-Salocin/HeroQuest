---
name: structurer-campagne
description: Organise une campagne HeroQuest du dépôt (Campagne02, 03, 04...) comme Campagne01, en trois dossiers Markdown ; 01-regles (règles, objets, calendriers, tables), 02-quetes (une quête par fichier, index, conséquences) et 03-suivi (fiche de suivi), plus un README de campagne et une liste de points à arbitrer. À utiliser dès que l'utilisateur demande de faire pour une campagne « les règles et le suivi », de structurer, migrer ou organiser une campagne comme Campagne01, de créer une fiche de suivi, ou de synthétiser des TXT de règles ou de support en Markdown, même sans citer ce skill. Pour la découpe du journal en quêtes, il s'appuie sur le skill decoupe-journal-quetes.
---

# Structurer une campagne comme Campagne01

Applique à une autre campagne l'organisation de `Campagne01/` : trois dossiers, des synthèses fidèles aux sources, et les incertitudes signalées plutôt que résolues.

## Avant de commencer

1. Lire `CLAUDE.md` et le `README.md` racine (consignes du dépôt), puis le `README.md` de la campagne s'il existe.
2. Lister les TXT de la campagne et lire **chacun en entier**. Ne pas se fier au nom : dans Campagne02, `regles-campagne.txt` décrit des objets (Carte de Grin, Anneau de Feu), pas un système de réputation, et `support_campagne_01.txt` contient un calendrier de siège.
3. Lire les fichiers modèles de `Campagne01/` seulement pour la forme : `01-regles/regles-campagne.md`, `01-regles/tables-voyage.md`, `02-quetes/consequences.md`, `03-suivi/fiche-campagne.md`, `README.md`.

## Principe clé : adapter, ne pas copier

Campagne01 suit réputation, corruption et table de voyage parce que ses sources les contiennent. Ne reprendre un indicateur que s'il existe dans les sources de la campagne traitée. Si une règle de Campagne01 manque dans l'autre campagne, le dire dans « Points à arbitrer » au lieu de l'importer.

## Structure à produire

| Fichier | Contenu |
| --- | --- |
| `README.md` | État, structure de travail, sources historiques (dire ce que contient vraiment chaque TXT), points à arbitrer. |
| `01-regles/regles-campagne.md` | Principes, tableau des éléments suivis avec liens, points à arbitrer. |
| `01-regles/<autres>.md` | Un fichier par ensemble cohérent : objets et artefacts, calendrier ou chronologie, tables. |
| `02-quetes/NN-slug.md`, `index.md` | Générés par le skill `decoupe-journal-quetes` (copie fidèle du journal). |
| `02-quetes/consequences.md` | Tableau N° / Réussite / Échec / Choix et effets à retenir, d'après les blocs de conséquences du journal. |
| `03-suivi/fiche-campagne.md` | Fiche vierge : Équipe, État de la campagne, Objets, Décisions et conséquences à reporter (une ligne par quête), Journal de partie. Indicateurs tirés des sources. |

## Règles de rédaction (dépôt HeroQuest)

- Français ; Markdown simple, titres hiérarchisés, tableaux lisibles à l'impression.
- Chaque synthèse commence par un bandeau `> Synthèse de ...` qui cite ses sources TXT.
- Ne rien inventer : ni règle, ni récompense, ni résultat, ni lien narratif absents des sources. Attribuer (« selon `regles-campagne.txt` », « selon le journal »).
- Quand deux sources se contredisent, conserver les deux variantes dans un tableau ou une phrase, et les signaler dans « Points à arbitrer ». Ne choisir aucune version.
- Les inscriptions et dialogues détaillés restent dans les TXT : renvoyer vers eux plutôt que tout recopier.
- Préserver les TXT et DOCX : ne rien supprimer, déplacer ni remplacer sans demande explicite. Ne pas committer sauf demande.
- Dans la fiche de suivi, ne pas pré-remplir de résultats : seules les colonnes de référence (origine, intitulé de quête) sont remplies.

## Procédure

1. Découper le journal avec le skill `decoupe-journal-quetes` (simulation, puis écriture).
2. Rédiger `01-regles/` à partir des TXT de règles et de support, en croisant avec les conséquences du journal pour repérer les contradictions (par exemple l'emplacement d'un objet de quête différent d'une source à l'autre).
3. Rédiger `02-quetes/consequences.md`, puis relancer le découpage seulement si `index.md` doit pointer vers lui (le script ajoute le lien si `consequences.md` existe).
4. Rédiger `03-suivi/fiche-campagne.md` avec les indicateurs réellement présents.
5. Rédiger `README.md`.
6. Vérifier :
   ```
   python .claude/skills/structurer-campagne/scripts/verifier_campagne.py Campagne02
   ```
   Le script contrôle que les liens Markdown relatifs pointent vers des fichiers existants, que `index.md` liste tous les fichiers de quêtes, et que chaque dossier attendu existe.
7. Rendre compte : fichiers créés, points à arbitrer trouvés, et ce qui n'a pas pu être fait (TXT absent, effets non définis).
