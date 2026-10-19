---
name: decoupe-journal-quetes
description: Découpe le journal de quêtes TXT d'une campagne HeroQuest (journal_de_quete.txt, Journal_quete_LivreXX.txt) en un fichier Markdown par quête dans CampagneNN/02-quetes/, avec un index.md, exactement comme Campagne01/02-quetes. À utiliser dès que l'utilisateur demande de découper, séparer, scinder ou migrer un journal de quêtes en fichiers par quête, de refaire pour une autre campagne la structure de Campagne01, ou de créer 02-quetes pour Campagne02, 03 ou 04, même s'il ne cite pas ce skill.
---

# Découpe d'un journal de quêtes en un fichier par quête

Reproduit la découpe de `Campagne01/02-quetes/` sur le journal TXT d'une autre campagne.

## Règle de découpe (celle de Campagne01, vérifiée octet par octet)

- Une quête commence à une ligne qui débute par `⚔️ Quête N : Titre` (`QUÊTE` en capitales accepté).
- Le fichier reprend la tranche du journal jusqu'à la quête suivante, **sans aucune reformulation**.
- Seule la première ligne change : on ajoute `# ` pour en faire un titre Markdown.
- Les lignes vides de fin de tranche sont retirées ; le fichier se termine par un saut de ligne.
- Nom du fichier : `NN-slug.md` (numéro sur 2 chiffres, titre sans accents, en minuscules, sans article initial, sans sous-titre après « – »).
- Le TXT d'origine n'est jamais modifié, déplacé ni supprimé (consigne du dépôt).

`index.md` liste N°, titre (tel qu'écrit dans le journal) et lien vers le fichier, puis une section **Points à arbitrer** si des incohérences sont détectées.

## Procédure

1. Identifier le journal (ex. `Campagne02/journal_de_quete.txt`). Ne charger que ce fichier et le `README.md` de la campagne s'il existe.
2. Simuler : 
   ```
   python .claude/skills/decoupe-journal-quetes/scripts/decouper_journal.py Campagne02/journal_de_quete.txt --dry-run
   ```
   Lire le plan (noms de fichiers, nombre de lignes) et les avertissements.
3. Ajuster les noms si besoin avec `--slug N=mon-slug`. Les slugs de Campagne01 raccourcissent parfois à la main (`delivrance-sir-ragnar`, `epee-de-lesprit`) : proposer un slug court quand le titre automatique est long, mais ne jamais changer le titre dans le fichier.
4. Écrire (par défaut dans `<dossier du journal>/02-quetes/`) :
   ```
   python .claude/skills/decoupe-journal-quetes/scripts/decouper_journal.py Campagne02/journal_de_quete.txt
   ```
   Le script refuse d'écraser des fichiers existants sans `--force`, et vérifie après écriture que chaque fichier correspond à sa tranche du journal.
5. Rendre compte à l'utilisateur : nombre de quêtes, noms de fichiers, et **tous les points à arbitrer** (numéros manquants ou en double, renvois « Lien avec la Quête N (Titre) » dont le titre ne correspond pas à la quête N, renvois vers une quête absente).

## Règles du dépôt à respecter

- Répondre en français.
- Ne pas inventer de règles, récompenses, résultats ou liens narratifs absents des sources.
- Si des sources se contredisent, conserver les variantes et les signaler dans « Points à arbitrer » ; ne pas corriger sans validation (par exemple un renvoi vers une mauvaise quête).
- Ne pas committer sauf demande explicite.

## Hors périmètre

Le script ne produit pas `consequences.md` (issu d'un tableau de conséquences distinct dans Campagne01, `campagne2.txt`), ni `01-regles/`, ni `03-suivi/`. Si l'utilisateur les demande pour une autre campagne, repartir de ses sources TXT correspondantes en suivant la même prudence (synthèse fidèle, incertitudes signalées), et proposer de mettre à jour le `README.md` de la campagne.
