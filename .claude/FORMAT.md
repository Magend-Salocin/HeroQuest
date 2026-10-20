# Écrire une quête (`questN.js`) à partir de son image (`questN.jpg`)

Une aventure de code `N` (table `aventure`) charge deux fichiers de ce dossier ([jeu.php](../../../../templates/pages/jeu.php)) :

- `questN.jpg` : le fond du plateau, 731 x 534 px ;
- `questN.js` : la carte jouable. Elle définit les pièces, les murs, les portes, les pièges, les monstres et la condition de victoire.

Le moteur ne lit pas l'image. Tout ce qui compte pour le jeu doit être recopié dans le `.js`.

Pour une nouvelle quête, utiliser le format « avec murs » des quêtes 101 à 124 (voir [quest101.js](quest101.js)). L'ancien format de 2009 (quêtes 1 à 8) est décrit à la fin, uniquement pour pouvoir le relire.

## 1. Lire la grille sur l'image

Le plateau fait 26 colonnes sur 19 lignes, soit 494 cases. Chaque case fait 28 px de côté.

| Donnée | Formule |
|---|---|
| Numéro de case | `case = ligne * 26 + colonne` (de 0 à 493) |
| Colonne d'un pixel `x` | `floor((x - 1) / 28)` |
| Ligne d'un pixel `y` | `floor((y - 1) / 28)` |
| Centre de la case `(col, lig)` | `x = 15 + 28 * col`, `y = 15 + 28 * lig` |
| Voisines de `c` | haut `c - 26`, bas `c + 26`, gauche `c - 1`, droite `c + 1` |

Exemple : le pixel (300, 120) est en colonne 10, ligne 4, donc dans la case 114.

Ce qu'on repère sur l'image :

| Sur l'image | Dans le `.js` |
|---|---|
| Noir | case hors carte : `'0'` dans `MesPieces`, `15` dans `MesMurs` |
| Zone d'un même sol, entourée de murs | une pièce, avec la même lettre sur toutes ses cases |
| Couloirs (dalles grises) | une pièce comme les autres, souvent `'A'` |
| Trait rouge sur un bord, ou icône de porte | une porte : `MesPortes` et `MesPortesPieceActive` sur les deux cases |
| Éboulis, meuble (table, coffre, armoire…) | case bloquée : bit `16` dans `MesMurs` |
| Escalier 2 x 2 | départ ou sortie : `PositionDepart` ou `CasesSortie` |
| Squelettes et tonneaux dessinés au sol | décor seul, rien à écrire (ou bit `16` pour bloquer la case) |

Les pièges et les monstres n'apparaissent pas sur l'image. Ils viennent du livret de la quête.

## 2. Modèle de fichier

Chaque tableau contient 494 valeurs, écrites sur 19 lignes de 26 valeurs pour pouvoir les comparer à l'image.

```js
// Titre de la quête : origine (livret, création...).

var PieceDepart = 'A';            // = MesPieces[PositionDepart]
var PositionDepart = 220;         // case du héros au départ
var PieceFouiller = ['Null'];     // pièces déjà fouillées : toujours ['Null']
var PieceActiver = ['A'];         // pièces visibles au départ : [PieceDepart]

/* Murs de chaque case : 1 haut, 2 droite, 4 bas, 8 gauche, 16 case occupée par un meuble. */
var MesMurs = [ /* 494 nombres */ ];

var MesPieges = [ /* 494 chaînes : '0' ou 'X' */ ];

var MesPieces = [ /* 494 chaînes : '0' ou lettre de pièce */ ];

/* Case devant une porte : pièce de l'autre côté (MesPortes) et pièce de la case (MesPortesPieceActive). */
var MesPortes = [ /* 494 chaînes */ ];
var MesPortesPieceActive = [ /* 494 chaînes */ ];

/* Facultatif, vue isométrique : voir section 9. */
var MesZones = [ /* 494 nombres */ ];
var MesObjets = [];

var LesMonstres = [
	TabMonstre(2, 59, 'B'),
	TabMonstre(1, 178, 'G')
];
var NbMonstre = 2;

function Victoire(){
	for (var i=0;i<LesMonstres.length;i++){
		if (LesMonstres[i][8]!=-1){ return false; }
	}
	return true;
}
```

## 3. `MesPieces` : découper en pièces

- Une pièce est un ensemble de cases reliées sans mur ni porte entre elles. Toutes ses cases portent la même lettre.
- Les lettres vont de `A` à `Z`, puis de `a` à `z`. Leur ordre n'a pas d'importance.
- `'0'` désigne une case hors carte, où l'on ne peut pas marcher.
- Le héros ne passe d'une pièce à une autre que par une case dont `MesPortes` n'est pas `'0'`.
- Entrer dans une pièce la révèle (toutes ses cases) et active ses monstres.

Par habitude, `'A'` désigne le réseau de couloirs, qui forme une seule pièce s'il est d'un seul tenant.

## 4. `MesMurs` : murs et cases bloquées

Chaque case additionne les côtés fermés : `1` haut, `2` droite, `4` bas, `8` gauche, plus `16` si un meuble occupe la case.

| Valeur | Signification |
|---|---|
| `0` | case ouverte de tous les côtés |
| `9` | mur en haut et à gauche (coin haut-gauche d'une pièce) |
| `15` | case fermée de tous les côtés (hors carte) |
| `21` | `16 + 4 + 1` : meuble, avec des murs en haut et en bas |

Règles :

- Un mur se déclare des deux côtés. Un mur à droite de `c` (`2`) implique un mur à gauche de `c + 1` (`8`). Le moteur ne vérifie que la case de départ du mouvement.
- Un bord de porte n'a pas de bit de mur.
- Le bord extérieur du plateau est fermé : ligne 0 avec `1`, ligne 18 avec `4`, colonne 0 avec `8`, colonne 25 avec `2`.
- Une case avec `16` est infranchissable pour le héros comme pour les monstres. Ne pas y placer de monstre, de départ ni de sortie.

Exemple tiré de quest101 : en haut de la pièce `C`, les cases 35, 36 et 37 valent `9`, `0` et `3`. La case 36 vaut `0` parce qu'une porte s'ouvre vers le couloir, au-dessus d'elle.

## 5. `MesPortes` et `MesPortesPieceActive` : les portes

Une porte relie deux cases voisines, une de chaque côté. On renseigne les deux cases :

| Tableau | Valeur sur la case `c` |
|---|---|
| `MesPortes[c]` | la pièce de l'autre côté de la porte |
| `MesPortesPieceActive[c]` | la pièce de la case elle-même, donc `MesPieces[c]` |

Toutes les autres cases valent `'0'` dans les deux tableaux.

Exemple (quest101) : une porte entre le couloir `A` (case 10) et la pièce `C` (case 36, juste en dessous).

```
case 10 : MesPieces 'A', MesPortes 'C', MesPortesPieceActive 'A'
case 36 : MesPieces 'C', MesPortes 'A', MesPortesPieceActive 'C'
```

Une case qui touche deux portes ne peut en porter qu'une seule, la première rencontrée. Éviter ce cas en plaçant les portes autrement.

## 6. `MesPieges`

`'X'` marque une case piégée, `'0'` une case normale. Un piège est invisible. Marcher dessus coûte 1 point de Corps, puis le piège disparaît. L'action « Piège » désamorce tous les pièges de la pièce où se trouve le héros.

Les trésors ne se configurent pas par quête. Fouiller une pièce tire une carte au hasard ([MesItem.js](../MesItem.js), `TabObjet`), une seule fois par pièce et seulement quand plus aucun monstre actif n'y reste.

## 7. `LesMonstres`

```js
TabMonstre(type, case, piece)
```

- `case` : position de départ du monstre, sur une case libre (sans `16`).
- `piece` : doit valoir exactement `MesPieces[case]`. Sinon le monstre ne s'active jamais.
- Un monstre reste inactif jusqu'à ce que le héros entre dans sa pièce. Ceux de la pièce de départ jouent dès le premier tour. Une fois actifs, ils poursuivent le héros partout (format avec murs).
- `NbMonstre` : nombre d'entrées de `LesMonstres`, à titre informatif.
- Un type inconnu reprend le type du monstre précédent.

Les types sont définis dans `TabMonstre` ([MesItem.js](../MesItem.js)) :

| Type | Nom | Dépl. | Att. | Déf. | Corps |
|---|---|---|---|---|---|
| 1 | Lutin (gobelin) | 10 | 2 | 1 | 1 |
| 2 | Orc | 8 | 3 | 2 | 1 |
| 3 | Femir (fimir) | 6 | 3 | 3 | 1 |
| 4 | Gargouille | 6 | 4 | 4 | 1 |
| 5 | GuerrierChaos | 6 | 3 | 4 | 1 |
| 6 | ChamanOrc (chef orc) | 8 | 3 | 2 | 6 |
| 7 à 14 | Ogre, OgreAncien, OgreGuerrier, OgreChef, OgreNeige, Yeti, Loup, DemonNeige | 8 | 3 | 2 | 6 |
| 15 | Squellette | 6 | 2 | 2 | 1 |
| 16 | Zombie | 4 | 2 | 3 | 1 |
| 17 | Momie | 4 | 3 | 4 | 1 |
| 18 | MageSquellette (sorcier-roi, cavaliers spectraux) | 8 | 3 | 2 | 6 |
| 19 | Sorcier | 8 | 3 | 2 | 6 |

## 8. `Victoire()`

Le moteur appelle `Victoire()` après chaque déplacement du héros et chaque combat. La quête est gagnée dès que la fonction renvoie `true`.

Dans les exemples ci-dessous, `LesMonstres[i][8]` vaut `-1` quand le monstre est mort, et `LesJoueurs[ConstIdJoueur][5]` donne la case du héros.

Tuer tous les monstres :

```js
function Victoire(){
	for (var i=0;i<LesMonstres.length;i++){
		if (LesMonstres[i][8]!=-1){ return false; }
	}
	return true;
}
```

Tuer un monstre précis (son indice dans `LesMonstres`, à partir de 0) :

```js
function Victoire(){
	return LesMonstres[5][8]==-1;
}
```

Atteindre une sortie (l'escalier, par exemple) :

```js
var CasesSortie = [220, 221, 246, 247];

function Victoire(){
	return CasesSortie.indexOf(Number(LesJoueurs[ConstIdJoueur][5])) != -1;
}
```

Atteindre une pièce après avoir tué un chef :

```js
function Victoire(){
	return LesMonstres[3][8]==-1 && MesPieces[LesJoueurs[ConstIdJoueur][5]]=='R';
}
```

## 9. Vue isométrique (facultatif)

[ModuleIso.js](../ModuleIso.js) ne s'affiche que si `MesMurs` et `MesZones` existent tous les deux. Sans `MesZones`, la quête se joue uniquement sur le plateau 2D.

`MesZones` donne le sol de chaque case. Les valeurs suivent la numérotation de HeroQuest :

| Valeur | Sol |
|---|---|
| `0` | hors carte |
| `1` à `20` | couloir |
| `21` à `42` | pièce. Chaque pièce prend un numéro différent, et le sol vient de `IsoSols` dans [iso/atlas.js](../iso/atlas.js) |

`MesObjets` liste les objets dessinés : `[code, case1, case2...]`, avec toutes les cases occupées par l'objet.

| Code | Objet |
|---|---|
| `48` | éboulis (1 case) |
| `56`, `57`, `58`, `59` | escalier : cases haut-gauche, bas-gauche, haut-droite, bas-droite |
| `75` / `76` | table |
| `77` / `78` | chevalet |
| `79` / `80` | établi d'alchimiste |
| `83` | tombeau |
| `84`, `86`, `88`, `90` | armoire, bibliothèque |
| `85` / `91` | râtelier d'armes |
| `87` / `89` | cheminée |
| `92` | coffre |
| `93` | coffre 2 |
| `94` / `95` | trône |

Les meubles ont un code par orientation. Essayer le premier, puis l'autre si le dessin est tourné. Chaque case d'un meuble listée ici doit aussi avoir le bit `16` dans `MesMurs`.

## 10. Vérifier le fichier

Le script suivant contrôle la cohérence d'une carte. Lancer `python verifier-quete.py public/assets/game/quests/questN.js` depuis `donjon-v2` :

```python
import re, sys

src = open(sys.argv[1], encoding='utf-8').read()

def tableau(nom):
    corps = re.search(r'var ' + nom + r'\s*=\s*\[(.*?)\];', src, re.S).group(1)
    return [v.strip().strip("'\"") for v in corps.replace('\n', '').split(',')]

murs = [int(v) for v in tableau('MesMurs')]
pieces, portes, actives, pieges = (tableau(n) for n in ('MesPieces', 'MesPortes', 'MesPortesPieceActive', 'MesPieges'))
for nom, t in [('MesMurs', murs), ('MesPieces', pieces), ('MesPortes', portes),
               ('MesPortesPieceActive', actives), ('MesPieges', pieges)]:
    assert len(t) == 494, f'{nom} : {len(t)} valeurs au lieu de 494'

for c in range(494):
    x, y = c % 26, c // 26
    if x < 25 and bool(murs[c] & 2) != bool(murs[c + 1] & 8):
        print(f'mur incohérent entre {c} et {c + 1}')
    if y < 18 and bool(murs[c] & 4) != bool(murs[c + 26] & 1):
        print(f'mur incohérent entre {c} et {c + 26}')
    if portes[c] != '0' and actives[c] != pieces[c]:
        print(f'porte {c} : MesPortesPieceActive doit valoir {pieces[c]}')

depart = int(re.search(r'PositionDepart\s*=\s*(\d+)', src).group(1))
piece_depart = re.search(r"PieceDepart\s*=\s*'(\w+)'", src).group(1)
assert pieces[depart] == piece_depart, f'PieceDepart doit valoir {pieces[depart]}'
for type_, case, piece in re.findall(r"TabMonstre\((\d+),\s*(\d+),\s*'(\w+)'\)", src):
    c = int(case)
    if pieces[c] != piece:
        print(f'monstre en {c} : pièce {piece} au lieu de {pieces[c]}')
    if murs[c] & 16:
        print(f'monstre en {c} sur une case bloquée')
print('vérification terminée')
```

Tester ensuite en jeu : parcourir chaque porte, vérifier que chaque pièce se révèle entière et que la victoire se déclenche.

## 11. Ajouter l'aventure au jeu

1. Déposer `questN.jpg` et `questN.js` dans ce dossier.
2. Ajouter une ligne dans [seed.sql](../../../../database/seed.sql), section `INSERT INTO aventure` :
   ```sql
   (N, 'Titre', 'Résumé affiché dans la liste.', or_gagne, exp_gagnee, grade_requis, '', 'code_village'),
   ```
   `grade_requis` va de 1 (Facile) à 4 (Héroïque). `code_village` vaut `'01'`, `'02'` ou `'03'`.
3. Recréer la base avec `php -d extension=pdo_sqlite bin/reset-db.php`. Attention, toutes les parties en cours sont perdues.
4. Facultatif : ajouter une illustration dans `img/aventures/quetes/` (voir `adventure_illustration()` dans [helpers.php](../../../../src/helpers.php)). Sans illustration, l'aventure reçoit une image de thème.

## Annexe : ancien format de 2009 (quêtes 1 à 8)

Ces fichiers n'ont pas de `MesMurs`. Le moteur se rabat alors sur un comportement plus limité :

- `'$'` désigne les couloirs. `'*'` désigne une case de couloir bloquée (éboulis), révélée avec les couloirs mais où l'on ne peut pas marcher.
- Les murs ne sont pas décrits : seul un changement de lettre sépare deux pièces.
- Les monstres ne poursuivent le héros que dans leur propre pièce.
- Les monstres déclarés avec la pièce `"0"` ne s'activent jamais.
- `MesMonstres` existe dans certains fichiers mais n'est plus lu.

Pour refaire une de ces quêtes, la réécrire entièrement au format avec murs, en suivant les sections 1 à 8.
