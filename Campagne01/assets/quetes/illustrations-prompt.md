# Illustrations des quêtes

Objectif : produire une illustration par quête, au même format que `donjon-v2/public/assets/img/donjon/aventure-labyrinthe.jpg` (bandeau horizontal, ratio 2,3:1, 234 × 102 px aujourd'hui).

## Méthode

Un générateur d'images ne tient pas 14 scènes distinctes sur une seule planche : les cases se mélangent et les détails disparaissent. On génère donc 3 planches de 6 cases (2 colonnes × 3 rangées) au format 1536 × 1024. Chaque case fait 768 × 341 px, soit le ratio 2,25:1 du bandeau.

| Planche | Cases (gauche → droite, haut → bas) |
| --- | --- |
| 1 | Quêtes 1 à 6 |
| 2 | Quêtes 7 à 12 |
| 3 | Quêtes 13 et 14, puis les 4 thèmes génériques (feu, glace, marais, labyrinthe) utilisés par `adventure_illustration()` |

Le prompt est en anglais : les modèles d'image le suivent mieux. Aucun texte dans l'image, les titres sont affichés par le site.

## Bloc de style (commun aux 3 planches)

```
A sprite sheet of 6 separate fantasy illustrations arranged in a strict grid of 2 columns and 3 rows, on a 1536x1024 canvas. Each panel is exactly 768x341 pixels, a wide horizontal banner. Panels are separated by a thin straight pure black gutter, no frames, no borders, no ornaments, no text, no letters, no numbers, no captions, no watermark. Every panel is an independent scene that can be cropped on its own.

Style: dark painterly dungeon fantasy, 1990s fantasy board game box art, oil painting texture, dramatic chiaroscuro, warm torchlight against cold shadows, muted palette of stone grey, deep blue and ember orange, high detail, cinematic wide shot. Recurring composition: a small group of adventurers (a barbarian, a dwarf, an elf, a wizard) seen from behind or in three-quarter view in the foreground, the threat or objective of the quest in the middle distance, strong depth. Same art style, lighting and color grading in all panels.
```

## Planche 1 : quêtes 1 à 6

```
[BLOC DE STYLE]

Panel 1 (top left), The Trial: ancient underground catacombs, rows of skull niches and broken sarcophagi, a single torch held by an adventurer, at the far end a stone gargoyle crouched on a pillar, its eyes faintly glowing, dust in the torchlight.

Panel 2 (top right), The Rescue of Sir Ragnar: crude orc lair carved in rock, bones and spiked palisades, a wounded human knight in torn surcoat chained to a wall inside an iron cage, orc guards silhouetted by a campfire, adventurers sneaking in from the shadows.

Panel 3 (middle left), The Orc Warlord's Lair: vast mountain cavern, huge war drums, banners of skulls, a massive orc warlord on a throne of bones raising a cleaver, horde of orcs in torchlight, snowy grey peaks visible through an opening.

Panel 4 (middle right), The Gold of Prince Magnus: cavern in black mountains, three heavy iron-bound treasure chests marked with a golden imperial seal glowing softly, a towering warrior in black runic plate armor with a cursed sword standing beside them, orcs banging axes on shields.

Panel 5 (bottom left), The Maze of Melar: stone labyrinth corridors covered with ancient runes glowing pale blue, cold mist on the floor, at the end a circular chamber lit green where an undead sorcerer in tattered enchanter robes stands before an altar covered with scrolls.

Panel 6 (bottom right), The Legacy of the Orc Warlord: damp dungeon cells, black water dripping on the walls, rusty chains and iron bars, a rat with a key near the bars, a snoring orc jailer, in the shadows an orc shaman with a staff crackling with red sparks.
```

## Planche 2 : quêtes 7 à 12

```
[BLOC DE STYLE]

Panel 1 (top left), The Stone Hunter: silent forest of grey trees, ground scattered with petrified statues of villagers frozen in terror, cold mist between the trunks, a hooded serpent-like creature with glowing eyes watching from between the statues.

Panel 2 (top right), The Fire Mage: volcanic peaks and rivers of lava, an obsidian lair, a theatrical fire mage in crimson robes juggling a fireball, an open grimoire floating in flames, sparks and ash filling the air.

Panel 3 (middle left), The Trap: overgrown stone maze deep in a dark forest, walls oozing black slime, a traitorous guide running away after blowing out his torch, only a green glow remaining, revealing three carved doors with strange symbols facing the adventurers.

Panel 4 (middle right), The Castle of Mysteries: gothic castle hall, tall cracked mirrors with reflections that do not match reality, torches going out one by one, pale blue ghost lights, behind a broken mirror a hidden cell with a ragged cursed prisoner.

Panel 5 (bottom left), The Chaos Bastion: underground chaos fortress, torches burning with green flames, sulfur smoke, spiked black walls, a gargoyle statue with glowing red eyes guarding a golden chest engraved with runes, chaos warriors in the distance.

Panel 6 (bottom right), The Witch Lord's Tomb: ruined necropolis under a blood-red moon, howling wind, trembling tombstones, a black mausoleum with three stone doors covered in runes, the middle door slightly open with a sickly light inside.
```

## Planche 3 : quêtes 13 et 14, thèmes génériques

```
[BLOC DE STYLE]

Panel 1 (top left), The Spirit Swords: moonlit ruins of an ancient temple, half dwarven stonework, half elven arches, two altars side by side, on the left a massive black dwarven blade glowing red-hot with runes, on the right a slender elven sword glowing icy blue, a translucent ghost priest standing between them.

Panel 2 (top right), Return to Barak Tor: apocalyptic sky torn by purple lightning, black rain on ruins, a throne room open to the storm, an undead sorcerer king on his throne raising a hand with a ring pulsing dark energy, adventurers charging with a glowing sword, legions of chaos on the horizon.

Panel 3 (middle left), Fire: dungeon hall lit by burning braziers and lava cracks in the floor, heat haze, adventurers shielding their faces.

Panel 4 (middle right), Ice: frozen crypt, icicles and frost-covered pillars, cold blue light, breath vapor of the adventurers.

Panel 5 (bottom left), Swamp: flooded sewer tunnel, stagnant green water, roots and moss, will-o'-the-wisps, adventurers wading knee-deep.

Panel 6 (bottom right), Labyrinth: long vaulted stone corridor with arches, an adventurer holding a torch in the foreground, a silhouette at the far end, a beast lurking at the side.
```

## Découpe

Ranger la planche dans `Campagne01/assets/illustrations/planche-N.png`, puis depuis `donjon-v2/` :

```
python bin/decouper-planche.py ../Campagne01/assets/illustrations/planche-2.png 7
```

Le second argument est le numéro de la première quête de la planche (1, 7 ou 13). Le script repère les gouttières noires, recadre chaque case au ratio du bandeau (744 × 324) et écrit `public/assets/img/donjon/quetes/quete-NN.jpg`. `adventure_illustration()` affiche `quete-NN.jpg` pour l'aventure 100 + NN quand le fichier existe, sinon l'image de thème.

| Fichier | Quête | Aventure |
| --- | --- | ---: |
| quete-01.jpg | L'Épreuve | 101 |
| quete-02.jpg | Le sauvetage de Sir Ragnar | 102 |
| quete-03.jpg | Le repaire du chef orc | 103 |
| quete-04.jpg | L'or du Prince Magnus | 104 |
| quete-05.jpg | Le labyrinthe de Melar | 105 (pas en base) |
| quete-06.jpg | L'héritage du chef orc | 106 |
| quete-07.jpg | Le chasseur de pierres | 107 |
| quete-08.jpg | Le mage du feu | 108 |
| quete-09.jpg | Course contre la montre (Le Piège) | 109 |
| quete-10.jpg | Le château des mystères | 110 (pas en base) |
| quete-11.jpg | Le bastion du Chaos | 111 |
| quete-12.jpg | Barak Tor, le tombeau du Sorcier-Roi | 112 |
| quete-13.jpg | La quête de l'Épée des Esprits | 113 |
| quete-14.jpg | Le retour à Barak Tor | 114 |

Planche 3 : les cases 3 à 6 (thèmes génériques) sortent en `quete-15.jpg` à `quete-18.jpg`. Les renommer à la main en `aventure-feu.jpg`, `aventure-glace.jpg`, `aventure-marais.jpg`, `aventure-labyrinthe.jpg` dans `img/donjon/`, sinon elles s'afficheraient pour les aventures 115 à 118.

## Si une case ratée

Régénérer la case seule : bloc de style, en remplaçant la première phrase par `A single wide horizontal banner illustration, 1536x672, no text.`, suivi de la description de la case.
