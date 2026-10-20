# Variante : Melar, PNJ actif

> Synthèse de `../system_campagne.txt` et de `../assets/todo.txt`. Cette version est une variante : elle ne concorde pas avec le rôle de Melar dans `../support_campagne_01.txt` (voir « Points à arbitrer »).

## Concept

Melar, piégé dans le Talisman de la Connaissance, devient un PNJ jouable au sein de l'équipe. Ses pouvoirs et ses malus évoluent avec son alignement. Au départ, c'est un esprit lié au Talisman porté par un héros : une voix neutre qui donne des conseils ambigus. Les joueurs peuvent négocier avec lui, le protéger ou le combattre selon ses actions.

## Pouvoirs et malus selon l'alignement

| Alignement | Pouvoirs | Malus |
| --- | --- | --- |
| Neutre | Conseils ambigus : peut révéler un piège ou un trésor caché. Les joueurs doivent deviner s'il dit vrai. | Aucun malus direct. |
| Corrompu | Sorts de la Terreur (Éclair, Tempête de Feu), 1 utilisation par quête. +1 aux jets d'attaque du porteur. Vision des ténèbres : le porteur voit les monstres à travers les murs, 1 utilisation par quête. | Monstres renforcés : ils se déplacent d'une case de plus pendant leur tour. Les pièges non détectés se déclenchent automatiquement. Corruption progressive : le porteur perd 1 PV par quête si Melar reste corrompu. |
| Lumineux | Vision lointaine : révèle une pièce éloignée sur la carte, 1 utilisation par quête. Résistance aux pièges pour le porteur et ses alliés (jet de sauvegarde avantageux). Bénédiction d'Agrain : +1 en Défense pour tous les héros adjacents. | Le porteur ne peut pas utiliser de sorts de la Terreur. Les monstres sont plus rusés : ils évitent les pièges posés par les héros. Fatigue magique : un seul pouvoir par quête. |

## Faire évoluer l'alignement

| Action des joueurs | Effet sur Melar |
| --- | --- |
| Utiliser un sort de la Terreur offert par Melar. | +1 niveau de corruption. |
| Refuser un pouvoir de la Terreur et utiliser une potion de purification. | +1 niveau de lumière. |
| Protéger le porteur du Talisman (par exemple une potion de guérison sur lui). | +1 niveau de lumière (Melar gagne confiance). |
| Ignorer les conseils de Melar ou le traiter avec méfiance. | +1 niveau de corruption (Melar se sent rejeté). |
| Sacrifier des ressources (par exemple un artefact rare pour purifier Melar). | Alignement lumineux pour 1 quête. |
| Laisser le porteur subir des dégâts sans l'aider. | +2 niveaux de corruption. |

## Exemples donnés par la source

- **Quête 5, Les Appartements de Melar.** Grimoire rouge : si les joueurs acceptent, Melar devient corrompu, le porteur gagne Tempête de Feu (1 utilisation), les autres héros deviennent orcs (2 PV, pas de magie) et les orcs et gobelins se déplacent d'une case de plus. S'ils refusent, Melar devient lumineux, révèle une porte secrète et les héros voient une pièce éloignée. Abominations (3 PV) : attaquent en premier avec +1 dégât si Melar est corrompu ; vulnérables au Fer de l'Esprit s'il est lumineux. Grimoire bleu : annule la transformation ; Melar corrompu le cache et propose un pouvoir de plus, Melar lumineux guide vers lui et offre un bonus de défense.
- **Quête 8, La Trahison de Melar.** Pour vaincre un boss, Melar propose un artefact maudit. Accepter : ombres qui affaiblissent le boss (-2 PV), mais monstres +1 case et +1 en attaque pendant 3 tours, et Melar gagne 2 niveaux de corruption. Refuser et purifier Melar : passage secret révélé, +1 en Défense pour l'équipe, Melar gagne 2 niveaux de lumière. Accepter trop souvent : Melar devient Fellmarak à la fin ; résister : Melar aide à vaincre Zargon.

Les choix de Melar à chaque quête sont dans [choix-melar.md](../02-quetes/choix-melar.md).

## Fins selon l'alignement final

| Alignement final | Fin de campagne | Conséquences |
| --- | --- | --- |
| Lumineux | Melar est libéré et rejoint les héros comme allié ; Fellmarak ne se lève jamais. | Victoire totale : le Royaume est sauvé, Melar devient un guide spirituel. |
| Neutre | Melar disparaît dans le Talisman ; Fellmarak reste une menace lointaine. | Victoire ambiguë : le Royaume est temporairement sauvé, Melar pourrait revenir. |
| Corrompu (mais vaincu) | Melar est expulsé du Talisman, son esprit erre toujours ; Fellmarak est affaibli. | Victoire partielle : Zargon prépare sa revanche. |
| Corrompu (triomphe) | Melar devient Fellmarak et plonge le Royaume dans les ténèbres. | Défaite tragique : les héros doivent fuir ou se sacrifier pour sceller Fellmarak. |

## Cartes de Melar

`../assets/todo.txt` décrit trois cartes (apparence, ambiance, texte de carte). Les textes complets restent dans le TXT.

| Version | Titre | Aspect indiqué |
| --- | --- | --- |
| Neutre | Melar l'Expérimentateur (« L'Expérimentateur Fou ») | Vieil enchanteur aux cheveux gris ébouriffés, robe tachée de potions, fioles et orbes flottants ; laboratoire en désordre. |
| Corrompu | Melar l'Enchanteur Noir | Silhouette imposante, robe noire et argentée à runes rouges, yeux rouges, bâton noir ; salle grandiose de livres maudits. La source l'indique « inspiré de Saruman ». |
| Lumineux | Melar le Rédimé (« Le Sage de la Nature ») | Robe verte et brune ornée de lianes, yeux dorés, petites créatures de la forêt, bâton à cristal ; clairière paisible. La source l'indique « inspiré de Radagast ». |

## Points à arbitrer

- **Rôle de Melar.** Variante (allié possible, libéré) contre support (esprit hostile qui devient Fellmarak) : voir [regles-campagne.md](regles-campagne.md).
- **Niveaux de corruption et de lumière.** Aucune valeur de départ, aucun seuil pour passer de Neutre à Corrompu ou Lumineux, aucun maximum.
- **Fins corrompues.** Rien ne dit ce qui distingue « Corrompu (mais vaincu) » de « Corrompu (triomphe) ».
- **Fin lumineuse.** « Melar rejoint les héros comme allié » contredit le support, où Melar libéré devient Fellmarak (quête 11).
- **Alignement dans les tableaux de choix.** Les icônes ⚖️, 🐍 et 🌟 ne sont pas expliquées ; leur correspondance avec Neutre, Corrompu et Lumineux est déduite du contenu.
- **Texte de conversation.** Le TXT contient des passages adressés à l'auteur (« Nicolas, cette version... », propositions de développement) : ils ne sont pas repris.
