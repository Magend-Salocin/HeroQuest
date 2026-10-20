#!/usr/bin/env python3
"""Extrait le plateau d'une carte de quête d'un livre PDF et prépare sa lecture.

Sorties dans DOSSIER :
  page.png      la page rendue (rotation du PDF appliquée) ;
  questN.jpg    le plateau recadré au format du jeu, 731 x 534 px (si --nom) ;
  grille.png    le plateau agrandi (60 px par case) avec le numéro de chaque case ;
  zoom-*.png    quatre quarts de grille.png, à lire un par un ;
  bords.txt     épaisseur du trait sur chaque bord de case (>= 4 : mur, 0 ou 1 : ouvert ou porte).

Usage :
  python extraire_plateau.py LIVRE.pdf --page 14 --out DOSSIER [--nom quest501] [--dpi 200]
         [--cadre X0 Y0 X1 Y1]

La grille (26 x 19 cases) est détectée sur les traits bordeaux de la carte. Si la détection
échoue, donner --cadre : pixels de page.png du coin haut-gauche de la case 0 et du coin
bas-droit de la case 493.

Prérequis : pymupdf, numpy, Pillow (pip install pymupdf numpy pillow).
"""
import argparse
from pathlib import Path

import numpy as np
import pymupdf
from PIL import Image, ImageDraw

COLS, ROWS = 26, 19


def masque_traits(im):
    rgb = np.asarray(im).astype(int)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    return (r < 170) & (g < 110) & (b < 130)


def pics(profil, seuil):
    groupes = []
    for i in np.nonzero(profil > seuil)[0]:
        if groupes and i - groupes[-1][-1] <= 2:
            groupes[-1].append(i)
        else:
            groupes.append([i])
    return [(g[0] + g[-1]) / 2 for g in groupes]


def meilleure_grille(positions, n_cases):
    """Cherche n_cases + 1 traits régulièrement espacés parmi les pics détectés."""
    meilleur = None
    for i, debut in enumerate(positions):
        for fin in positions[i + 1:]:
            pas = (fin - debut) / n_cases
            if not 35 <= pas <= 120:
                continue
            score = sum(1 for k in range(1, n_cases)
                        if min(abs(p - (debut + k * pas)) for p in positions) <= 4)
            if meilleur is None or score > meilleur[0] or (score == meilleur[0] and fin - debut > meilleur[2] - meilleur[1]):
                meilleur = (score, debut, fin)
    if meilleur is None or meilleur[0] < n_cases * 0.6:
        raise SystemExit("Grille non détectée : relancer avec --cadre X0 Y0 X1 Y1.")
    return meilleur[1], meilleur[2]


def epaisseur(trait, sur_x, pos, debut, fin):
    """Nombre de lignes de pixels pleines (> 60 %) autour d'un bord de case."""
    if sur_x:
        bandes = [trait[debut:fin, int(pos) + d].mean() for d in range(-7, 8)]
    else:
        bandes = [trait[int(pos) + d, debut:fin].mean() for d in range(-7, 8)]
    return sum(1 for v in bandes if v > 0.6)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("pdf")
    p.add_argument("--page", type=int, required=True, help="numéro de page du PDF, à partir de 1")
    p.add_argument("--out", required=True)
    p.add_argument("--nom", help="nom du fichier image du jeu, par exemple quest501")
    p.add_argument("--dpi", type=int, default=200)
    p.add_argument("--cadre", type=float, nargs=4, metavar=("X0", "Y0", "X1", "Y1"))
    a = p.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(a.pdf)
    doc[a.page - 1].get_pixmap(dpi=a.dpi).save(out / "page.png")
    page = Image.open(out / "page.png").convert("RGB")
    trait = masque_traits(page)

    if a.cadre:
        x0, y0, x1, y1 = a.cadre
    else:
        x0, x1 = meilleure_grille(pics(trait.sum(0), trait.shape[0] * 0.2), COLS)
        y0, y1 = meilleure_grille(pics(trait.sum(1), trait.shape[1] * 0.2), ROWS)
    cw, ch = (x1 - x0) / COLS, (y1 - y0) / ROWS
    print(f"grille : x {x0:.1f} -> {x1:.1f}, y {y0:.1f} -> {y1:.1f}, case {cw:.1f} x {ch:.1f} px")

    if a.nom:
        # Case de 28 px, trait de grille en x = 1 et y = 1 (voir FORMAT.md, section 1).
        sx, sy = cw / 28, ch / 28
        jeu = page.resize((731, 534), Image.LANCZOS, box=(x0 - sx, y0 - sy, x0 + 730 * sx, y0 + 533 * sy))
        jeu.save(out / f"{a.nom}.jpg", quality=92)

    z = 60
    grille = page.resize((COLS * z, ROWS * z), Image.LANCZOS, box=(x0, y0, x1, y1))
    d = ImageDraw.Draw(grille)
    for c in range(COLS + 1):
        d.line([(c * z, 0), (c * z, ROWS * z)], fill=(0, 160, 255))
    for r in range(ROWS + 1):
        d.line([(0, r * z), (COLS * z, r * z)], fill=(0, 160, 255))
    for r in range(ROWS):
        for c in range(COLS):
            d.text((c * z + 3, r * z + 2), str(r * COLS + c), fill=(0, 0, 255))
    grille.save(out / "grille.png")
    mx, my = 14 * z, 10 * z
    for nom, boite in {"haut-gauche": (0, 0, mx, my), "haut-droite": (COLS * z - mx, 0, COLS * z, my),
                       "bas-gauche": (0, ROWS * z - my, mx, ROWS * z),
                       "bas-droite": (COLS * z - mx, ROWS * z - my, COLS * z, ROWS * z)}.items():
        grille.crop(boite).save(out / f"zoom-{nom}.png")

    lignes = ["Bord gauche de chaque case (colonnes 1 à 25), une ligne par rangée :"]
    for r in range(ROWS):
        ya, yb = int(y0 + (r + 0.2) * ch), int(y0 + (r + 0.8) * ch)
        lignes.append(f"{r:2d} " + " ".join(f"{epaisseur(trait, True, x0 + c * cw, ya, yb):2d}" for c in range(1, COLS)))
    lignes.append("Bord haut de chaque case (rangées 1 à 18), une ligne par rangée, colonnes 0 à 25 :")
    for r in range(1, ROWS):
        lignes.append(f"{r:2d} " + " ".join(
            f"{epaisseur(trait, False, y0 + r * ch, int(x0 + (c + 0.2) * cw), int(x0 + (c + 0.8) * cw)):2d}"
            for c in range(COLS)))
    (out / "bords.txt").write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"fichiers écrits dans {out}")


if __name__ == "__main__":
    main()
