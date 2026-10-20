# Plateaux jouables

Cartes des quêtes converties pour le jeu web Donjon, au format décrit dans `.claude/FORMAT.md`. Pour chaque quête : `questNNN.jpg` (plateau recadré depuis le PDF, 731 x 534 px), `questNNN.json` (description lue sur la carte) et `questNNN.js` (généré depuis le JSON par le skill `plateau-quete-js`, ne pas le modifier à la main).

| Quête | Fichiers | Départ | Victoire |
| --- | --- | --- | --- |
| 1 - Le retour de l'Épée souveraine | `quest501.*` | case 0 (porte en fer) | fouiller la pièce D, puis revenir en case 0 |

## Points à arbitrer

- Numérotation `quest501` (livre 5, quête 1) : à valider avant l'ajout dans `seed.sql`.
- Quête 1 : les portes dessinées en biais (cases 86, 110 et 95) sont traitées comme des portes normales. Sans elles, les pièces E et C ne seraient pas accessibles.
- Quête 1 : éléments non modélisés par le moteur :
  - les trappes reliées (note A), si bien que la pièce B (Élixir de vie) et la pièce K sont inaccessibles ;
  - l'immobilité des monstres de C (note C) : ils s'activent quand l'elfe entre dans C ;
  - le coffre piégé de D (note D) ;
  - le piège à monstre errant en case 257 (momie) ;
  - l'oubliette longue (cases 272 et 298), remplacée par deux pièges ordinaires.
- Quête 1 : la fouille tire une carte au hasard. L'Épée souveraine, l'Élixir de vie et les Bracelets elfiques ne sont pas attribués. La récompense finale (cotte de mailles elfique) n'est pas gérée.
