---
name: plateau-quete-js
description: Transforme la carte d'une quête d'un livre PDF HeroQuest (_ressource/) en plateau jouable pour le jeu web Donjon - image questN.jpg (731 x 534) et carte questN.js au format « avec murs » décrit dans .claude/FORMAT.md. À utiliser dès que l'utilisateur demande d'extraire une carte ou un plateau de quête, de générer un questN.js, de rendre une quête jouable dans le jeu, ou de convertir les cartes d'un livre de quêtes (Le Mage du Miroir, La Horde des Ogres...), même sans citer ce skill.
---

# Plateau de quête : PDF vers questN.jpg et questN.js

Le format cible est décrit dans [.claude/FORMAT.md](../../FORMAT.md) : le lire avant de commencer (grille 26 x 19, bits de murs, portes, types de monstres, `Victoire()`). Le moteur ne lit pas l'image : tout ce qui compte doit être dans le `.js`.

## Procédure

1. **Repérer les pages.** La page de la carte et celle des notes sont dans `CampagneNN/02-quetes/index.md` (colonne « Pages du PDF »). Lire la fiche de la quête pour les notes, le début, la fin et les monstres errants.
2. **Extraire le plateau.**
   ```
   python .claude/skills/plateau-quete-js/scripts/extraire_plateau.py "_ressource/.../Livre.pdf" --page 14 --out <scratchpad>/qN --nom questNNN
   ```
   Le script détecte la grille, écrit `questNNN.jpg` au format du jeu, `grille.png` (numéro de chaque case), quatre `zoom-*.png` et `bords.txt` (épaisseur du trait de chaque bord : 4 ou plus = mur, 0 ou 1 sur un mur = porte ou icône posée dessus). Prérequis : `pip install pymupdf numpy pillow`.
3. **Lire la carte** sur les zooms (`Read` sur chaque image), en croisant avec `bords.txt` :
   - cases brunes : hors carte (pièces et couloirs non utilisés) ;
   - pièces : rectangles de sol clair entourés de murs ; couloirs : dalles beiges, pièce `A` ;
   - portes : rectangle blanc posé en travers d'un mur, ou porte ouverte dessinée en biais (trait à 0 dans `bords.txt`) ;
   - éboulis (pierres, 1 ou 2 cases) et meubles : cases bloquées ;
   - monstres : gobelin (oreilles pointues), orc (crocs), squelette, zombie, momie (bandelettes) ;
   - flèches en bord de carte : entrée (vers l'intérieur) ou sortie (vers l'extérieur).
4. **Écrire la description** `CampagneNN/04-plateaux/questNNN.json` (format en tête de [generer_quete.py](scripts/generer_quete.py)) : pièces en rectangles, paires de portes, cases bloquées, pièges, monstres `[type, case]`, condition de victoire. Garder les lettres de pièce du livre quand une note désigne une pièce (B, C, D...), `A` pour les couloirs, les lettres suivantes pour les autres pièces.
5. **Générer et vérifier.**
   ```
   python .claude/skills/plateau-quete-js/scripts/generer_quete.py CampagneNN/04-plateaux/questNNN.json
   ```
   Les murs sont déduits des pièces. Le script signale les erreurs de cohérence (contrôles de FORMAT.md, section 10) et les pièces inaccessibles depuis le départ. Puis superposer la carte générée sur l'image et la relire : c'est ce contrôle qui détecte les erreurs de lecture.
   ```
   python .claude/skills/plateau-quete-js/scripts/controler_plateau.py CampagneNN/04-plateaux/questNNN.js CampagneNN/04-plateaux/questNNN.jpg --out <scratchpad>/controle.png
   ```
6. **Noter les écarts** dans `CampagneNN/04-plateaux/README.md` : une ligne par quête (fichiers, départ, victoire) et la liste « Points à arbitrer ».

## Ce que le moteur ne sait pas faire

Ne pas inventer de mécanisme : modéliser au plus près, et noter l'écart dans le champ `remarques` du JSON (recopié en tête du `.js`) et dans le README.

| Élément du livre | Approche par défaut |
|---|---|
| Trappes reliées, téléportation | non modélisé ; les pièces qui ne sont accessibles que par là restent isolées |
| Oubliette, fosse | piège `X` (le moteur retire 1 point de Corps au lieu de la règle du livre) |
| Piège à monstre errant | non modélisé |
| Coffre piégé, trésor précis | non modélisé (la fouille tire une carte au hasard) |
| Monstres immobiles, activation par un autre événement | non modélisé (activation à l'entrée dans la pièce) |
| Objet à trouver puis sortir | `"victoire": {"fouiller": ["D"], "sortie": [case]}` |

## Points de vigilance

- Numérotation : les codes 101 à 124 sont pris par les quêtes du HeroQuest PC. Convention retenue pour les livres : `questLQQ` (livre L, quête QQ), par exemple `quest501` pour Le Mage du Miroir, quête 1. La faire valider avant d'ajouter la quête à `seed.sql`.
- Les fichiers produits restent dans `CampagneNN/04-plateaux/`. La copie dans le jeu (`donjon-v2/public/assets/game/quests/`) et l'ajout dans `seed.sql` (FORMAT.md, section 11) se font à la demande.
- Une case ne peut être devant qu'une seule porte : le générateur refuse le cas, déplacer alors l'une des portes d'une case.
- Ne pas placer de monstre, de départ ou de sortie sur une case bloquée.
- Les icônes masquent parfois un trait (`bords.txt` à 0 sous un monstre) : ne pas en déduire une porte sans la voir sur l'image.
