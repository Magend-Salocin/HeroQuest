#!/usr/bin/env python3
"""Génère questN.js (format « avec murs », voir .claude/FORMAT.md) à partir d'une description JSON.

Usage :
  python generer_quete.py questN.json [--out questN.js]

Description JSON (cases numérotées ligne * 26 + colonne, rectangles [col0, lig0, col1, lig1] inclus) :
  {
    "titre": "Le retour de l'Épée souveraine",
    "origine": "Le Mage du Miroir (2023), quête 1, carte p. 14 du PDF",
    "depart": 0,
    "pieces": {"A": [[0, 0, 25, 0], [0, 1, 0, 9]], "B": [[9, 13, 11, 17]]},
    "portes": [[52, 53]],            paires de cases voisines, une de chaque côté
    "bloquees": [14, 35, 36],        meubles et éboulis (bit 16)
    "pieges": [272],                 cases piégées ('X')
    "monstres": [[1, 28], [17, 137]],  [type, case] ; la pièce est déduite de la case
    "victoire": {"tuer": "tous" | [indices], "fouiller": ["D"], "sortie": [0]},
    "remarques": ["texte recopié en commentaire en tête du fichier"]
  }

Les murs sont déduits des pièces : un mur sépare deux cases de pièces différentes, sauf aux
portes ; le bord du plateau et les cases hors carte ('0') sont fermés.
Le script vérifie ensuite la carte (contrôles de FORMAT.md, section 10, et accessibilité des pièces).
"""
import argparse
import json
from collections import deque
from pathlib import Path

COLS, ROWS = 26, 19
N = COLS * ROWS
# bit de mur, décalage vers la voisine
DIRECTIONS = [(1, -COLS), (2, 1), (4, COLS), (8, -1)]


def voisine(c, decalage):
    x, y = c % COLS, c // COLS
    if decalage == 1 and x == COLS - 1 or decalage == -1 and x == 0:
        return None
    v = c + decalage
    return v if 0 <= v < N else None


def construire(desc):
    pieces = ["0"] * N
    for lettre, rects in desc["pieces"].items():
        for c0, r0, c1, r1 in rects:
            for r in range(r0, r1 + 1):
                for c in range(c0, c1 + 1):
                    case = r * COLS + c
                    if pieces[case] not in ("0", lettre):
                        raise SystemExit(f"case {case} dans {pieces[case]} et {lettre}")
                    pieces[case] = lettre

    paires = set()
    portes, actives = ["0"] * N, ["0"] * N
    for a, b in desc.get("portes", []):
        if b - a not in (1, -1, COLS, -COLS) or voisine(a, b - a) != b:
            raise SystemExit(f"porte {a}-{b} : cases non voisines")
        if "0" in (pieces[a], pieces[b]) or pieces[a] == pieces[b]:
            raise SystemExit(f"porte {a}-{b} : doit relier deux pièces différentes")
        for c, autre in ((a, b), (b, a)):
            if portes[c] != "0":
                raise SystemExit(f"case {c} : déjà devant une autre porte")
            portes[c], actives[c] = pieces[autre], pieces[c]
        paires |= {(a, b), (b, a)}

    murs = [0] * N
    for c in range(N):
        if pieces[c] == "0":
            murs[c] = 15
            continue
        for bit, dec in DIRECTIONS:
            v = voisine(c, dec)
            if v is None or pieces[v] != pieces[c] and (c, v) not in paires:
                murs[c] |= bit
    for c in desc.get("bloquees", []):
        murs[c] |= 16

    pieges = ["0"] * N
    for c in desc.get("pieges", []):
        pieges[c] = "X"
    return pieces, murs, portes, actives, pieges


def victoire_js(v):
    tests = []
    tuer = v.get("tuer")
    if tuer == "tous":
        tests.append("TousMorts()")
    elif tuer:
        tests += [f"LesMonstres[{i}][8]==-1" for i in tuer]
    tests += [f"PieceFouiller.indexOf('{p}')!=-1" for p in v.get("fouiller", [])]
    if v.get("sortie"):
        tests.append("CasesSortie.indexOf(Number(LesJoueurs[ConstIdJoueur][5]))!=-1")
    if not tests:
        raise SystemExit("victoire : préciser tuer, fouiller ou sortie")
    lignes = []
    if v.get("sortie"):
        lignes.append(f"var CasesSortie = [{', '.join(map(str, v['sortie']))}];\n")
    if tuer == "tous":
        lignes.append("function TousMorts(){\n\tfor (var i=0;i<LesMonstres.length;i++){\n"
                      "\t\tif (LesMonstres[i][8]!=-1){ return false; }\n\t}\n\treturn true;\n}\n")
    lignes.append("function Victoire(){\n\treturn " + " && ".join(tests) + ";\n}\n")
    return "\n".join(lignes)


def tableau(nom, valeurs, chaine):
    rangs = []
    for r in range(ROWS):
        ligne = valeurs[r * COLS:(r + 1) * COLS]
        rangs.append(",".join(f"'{v}'" if chaine else str(v) for v in ligne))
    return f"var {nom} = [\n" + ",\n".join(rangs) + "\n];\n"


def verifier(desc, pieces, murs, portes, actives):
    erreurs = []
    for c in range(N):
        x, y = c % COLS, c // COLS
        if x < COLS - 1 and bool(murs[c] & 2) != bool(murs[c + 1] & 8):
            erreurs.append(f"mur incohérent entre {c} et {c + 1}")
        if y < ROWS - 1 and bool(murs[c] & 4) != bool(murs[c + COLS] & 1):
            erreurs.append(f"mur incohérent entre {c} et {c + COLS}")
    depart = desc["depart"]
    if pieces[depart] == "0" or murs[depart] & 16:
        erreurs.append(f"départ {depart} hors carte ou bloqué")
    for type_, case in desc.get("monstres", []):
        if pieces[case] == "0" or murs[case] & 16:
            erreurs.append(f"monstre en {case} hors carte ou sur une case bloquée")
    for c in desc.get("victoire", {}).get("sortie", []):
        if pieces[c] == "0" or murs[c] & 16:
            erreurs.append(f"sortie {c} hors carte ou bloquée")

    # Accessibilité : déplacements du héros (même pièce ou passage par une porte, cases libres).
    vues, file = {depart}, deque([depart])
    while file:
        c = file.popleft()
        for bit, dec in DIRECTIONS:
            v = voisine(c, dec)
            if v is None or v in vues or murs[c] & bit or murs[v] & 16:
                continue
            if pieces[v] == pieces[c] or portes[v] != "0":
                vues.add(v)
                file.append(v)
    atteintes = {pieces[c] for c in vues}
    isolees = sorted(set(pieces) - atteintes - {"0"})
    return erreurs, isolees


def main():
    p = argparse.ArgumentParser()
    p.add_argument("description")
    p.add_argument("--out")
    a = p.parse_args()
    src = Path(a.description)
    desc = json.loads(src.read_text(encoding="utf-8"))
    out = Path(a.out) if a.out else src.with_suffix(".js")

    pieces, murs, portes, actives, pieges = construire(desc)
    depart = desc["depart"]
    monstres = [(t, c, pieces[c]) for t, c in desc.get("monstres", [])]

    entete = [f"// {desc['titre']} : {desc['origine']}."]
    entete.append(f"// Fichier généré par generer_quete.py depuis {src.name}, ne pas modifier à la main.")
    entete += [f"// {r}" for r in desc.get("remarques", [])]
    js = "\n".join(entete) + "\n\n"
    js += (f"var PieceDepart = '{pieces[depart]}';\nvar PositionDepart = {depart};\n"
           f"var PieceFouiller = ['Null'];\nvar PieceActiver = ['{pieces[depart]}'];\n\n")
    js += "/* Murs de chaque case : 1 haut, 2 droite, 4 bas, 8 gauche, 16 case occupée par un meuble. */\n"
    js += tableau("MesMurs", murs, False) + "\n"
    js += tableau("MesPieges", pieges, True) + "\n"
    js += tableau("MesPieces", pieces, True) + "\n"
    js += "/* Case devant une porte : pièce de l'autre côté (MesPortes) et pièce de la case (MesPortesPieceActive). */\n"
    js += tableau("MesPortes", portes, True) + "\n"
    js += tableau("MesPortesPieceActive", actives, True) + "\n"
    js += "var LesMonstres = [\n" + ",\n".join(f"\tTabMonstre({t}, {c}, '{l}')" for t, c, l in monstres) + "\n];\n"
    js += f"var NbMonstre = {len(monstres)};\n\n"
    js += victoire_js(desc["victoire"])
    out.write_text(js, encoding="utf-8")
    print(f"{out} écrit : {len(set(pieces)) - 1} pièces, {len(desc.get('portes', []))} portes, {len(monstres)} monstres")

    erreurs, isolees = verifier(desc, pieces, murs, portes, actives)
    for e in erreurs:
        print("ERREUR", e)
    if isolees:
        print("pièces inaccessibles depuis le départ :", ", ".join(isolees))
    print("vérification terminée" if not erreurs else f"{len(erreurs)} erreur(s)")


if __name__ == "__main__":
    main()
