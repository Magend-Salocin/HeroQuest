# Portraits des héros

Objectif : un portrait par héros et par sexe pour le jeu en ligne (`donjon-v2`), avec les mêmes personnages que les fiches de la campagne (`assets/Fiche_hero_*.png`).

| Type | Héros (h) | Héroïne (f) |
| --- | --- | --- |
| Barbare | `barbare-h` | `barbare-f` |
| Nain | `nain-h` | `nain-f` |
| Elfe | `elfe-h` | `elfe-f` |
| Enchanteur | `enchanteur-h` | `enchanteur-f` |

Chaque portrait sert trois fois dans le jeu :

| Usage | Fichier produit | Taille |
| --- | --- | --- |
| Portrait (fiche du héros, compte, niveau) | `img/personnages/<type>-<sexe>.png` | 480 px de haut |
| Combat (gros plan pendant une attaque) | `game/images/avatars/<type>-<sexe>-combat.png` | 180 px de haut |
| Pion du plateau (la tête) | `game/images/avatars/<type>-<sexe>-pion.png` | 24 × 24 |

La vue isométrique garde les sprites du HeroQuest PC : barbare, nain, elfe et magicien pour l'Enchanteur.

## Méthode

On génère une planche de 8 cases (4 colonnes × 2 rangées) au format 1536 × 1024. Chaque case fait 384 × 512, au format portrait 3:4.

- Colonnes, de gauche à droite : Barbare, Nain, Elfe, Enchanteur.
- Rangée du haut : les héros. Rangée du bas : les héroïnes.

Les personnages sont sur un fond vert uni, que le script de découpe retire. Les images sont donc détourées et se posent sur le parchemin du site comme sur l'écran de combat.

Le prompt est en anglais, parce que les modèles d'image le suivent mieux. L'image ne doit contenir aucun texte.

Contraintes à respecter, sinon la découpe se passe mal :

- **Personnage entier et debout, rien au-dessus de la tête.** Le pion est le carré du haut du personnage. Une hache levée ou un bâton plus haut que la tête prendrait la place du visage.
- **Fond vert pur et uni** (`#00FF00`), sans ombre au sol ni décor.
- **Pas de vert vif sur les personnages.** Le script efface le vert proche du fond. Les tons vert-de-gris ou olive restent sans problème.

Si le générateur accepte des images de référence, joindre la fiche du héros (`assets/Fiche_hero_<type>_<M|F>.png`) avec la case correspondante.

## Prompt de la planche

```
A character sheet of 8 separate full-body fantasy hero portraits arranged in a strict grid of 4 columns and 2 rows, on a 1536x1024 canvas. Each panel is exactly 384x512 pixels, portrait orientation. Panels are separated by a thin straight pure black gutter. Every panel has a plain flat solid pure green (#00FF00) background with no gradient, no floor, no cast shadow, no scenery. No frames, no borders, no text, no letters, no numbers, no captions, no watermark.

Each panel shows one hero, full body from head to feet, standing, three-quarter view facing the viewer, centered, filling about 85 percent of the panel height. Weapons and staffs are held low or at the side: nothing rises above the top of the head. No bright green on the characters.

Style: painterly dark fantasy, 1990s fantasy board game box art, oil painting texture, warm torchlight from the upper left, muted palette of stone grey, leather brown, iron and ember orange, high detail on faces and armor. Same art style, lighting, scale and color grading in all panels.

Top row, male heroes, left to right:
Panel 1, Barbarian: huge muscular man, long wild dark hair and beard, bare chest crossed with leather straps, fur shoulder pads, belt with a skull buckle, fur-wrapped boots, a great double-bladed battle axe held lowered in front of him, its head resting near his feet.
Panel 2, Dwarf: short stocky dwarf, long braided white beard, winged iron helmet with nose guard, heavy plate and chain armor with runic engravings, wide belt with pouches, a double-bladed axe held diagonally across his chest.
Panel 3, Elf: slender elf, long straight fair hair, pointed ears, fitted scale leather armor, hooded grey-brown cloak, a longbow held at his side, quiver of arrows on his back.
Panel 4, Wizard: tall bearded wizard with long hair, layered flowing robes with runic embroidery, an open spellbook in one hand, the other hand raised at shoulder height with a faint blue glow.

Bottom row, female heroes, left to right:
Panel 5, Barbarian: tall athletic warrior woman, long wavy hair with small braids, leather and scale armor, fur-lined cloak, a round iron-rimmed wooden shield on one arm, a broadsword held low in the other hand.
Panel 6, Dwarf: short sturdy dwarf woman, two long braids, horned iron helmet, ornate plate armor with runic patterns, a two-handed axe held diagonally across her chest.
Panel 7, Elf: slender elf woman, long wavy fair hair, pointed ears, scale-patterned mail, hooded grey-brown cloak, a slender elven sword held low, a longbow slung on her back.
Panel 8, Sorceress: hooded sorceress, fitted robes with a laced corset and runic hems, a staff topped with a glowing orb held at her side and no taller than her shoulder, the other hand open with a faint blue glow.
```

## Découpe

Ranger la planche dans `Campagne01/assets/illustrations/heros.png`, puis depuis `donjon-v2/` :

```
python bin/decouper-heros.py ../Campagne01/assets/illustrations/heros.png
```

Le script repère les gouttières noires, retire le fond vert de chaque case, recadre sur le personnage et écrit les 3 fichiers par héros (voir le tableau plus haut). Le site les lit avec `hero_image()` (`src/helpers.php`) : les 8 héros doivent avoir leurs 3 fichiers, il n'y a plus d'image de secours.

Vérifier ensuite :

- **Portraits :** pas de liseré vert, et aucune partie du personnage effacée (un vert trop vif sur un vêtement).
- **Pions :** le visage est bien cadré. Au besoin, retoucher le pion à la main (PNG 24 × 24 transparent).

## Si une case est ratée

Régénérer la case seule. Utiliser le prompt de la planche en remplaçant le premier paragraphe par :

```
A single full-body fantasy hero portrait, 768x1024, portrait orientation, on a plain flat solid pure green (#00FF00) background with no gradient, no floor, no cast shadow, no scenery. No frame, no text, no watermark.
```

Garder le deuxième paragraphe (cadrage) et le style, puis ajouter la description du héros. Découper ensuite cette image seule :

```
python bin/decouper-heros.py ../Campagne01/assets/illustrations/heros-elfe-f.png elfe f
```
