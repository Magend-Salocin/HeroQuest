#!/usr/bin/env python3
"""Superpose le contenu de questN.js sur questN.jpg pour le relire visuellement.

Vert : murs. Croix bleue : case bloquée. Point rouge : case devant une porte. Carré noir : hors carte.
X violet : piège. Mn : monstre de type n. Chaque case porte la lettre de sa pièce.

Usage :
  python controler_plateau.py questN.js questN.jpg --out controle.png
"""
import argparse
import re

from PIL import Image, ImageDraw


def tableau(src, nom):
    corps = re.search(r"var " + nom + r"\s*=\s*\[(.*?)\];", src, re.S).group(1)
    return [v.strip().strip("'\"") for v in corps.replace("\n", "").split(",")]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("js")
    p.add_argument("jpg")
    p.add_argument("--out", required=True)
    a = p.parse_args()

    src = open(a.js, encoding="utf-8").read()
    murs = [int(v) for v in tableau(src, "MesMurs")]
    pieces, portes, pieges = (tableau(src, n) for n in ("MesPieces", "MesPortes", "MesPieges"))

    z, s = 2, 56  # image agrandie 2 fois, case de 56 px
    im = Image.open(a.jpg).convert("RGB").resize((731 * z, 534 * z))
    d = ImageDraw.Draw(im)
    vert = (0, 200, 0)
    for c in range(494):
        x, y = (1 + 28 * (c % 26)) * z, (1 + 28 * (c // 26)) * z
        if pieces[c] == "0":
            d.rectangle([x + 20, y + 20, x + 36, y + 36], fill=(0, 0, 0))
            continue
        m = murs[c]
        if m & 1: d.line([x, y + 3, x + s, y + 3], fill=vert, width=3)
        if m & 2: d.line([x + s - 3, y, x + s - 3, y + s], fill=vert, width=3)
        if m & 4: d.line([x, y + s - 3, x + s, y + s - 3], fill=vert, width=3)
        if m & 8: d.line([x + 3, y, x + 3, y + s], fill=vert, width=3)
        if m & 16:
            d.line([x + 8, y + 8, x + s - 8, y + s - 8], fill=(0, 0, 255), width=3)
            d.line([x + s - 8, y + 8, x + 8, y + s - 8], fill=(0, 0, 255), width=3)
        if portes[c] != "0":
            d.ellipse([x + 22, y + 22, x + 34, y + 34], fill=(255, 0, 0))
        if pieges[c] == "X":
            d.text((x + 24, y + 20), "X", fill=(255, 0, 255))
        d.text((x + 4, y + 40), pieces[c], fill=(0, 0, 0))
    for type_, case in re.findall(r"TabMonstre\((\d+),\s*(\d+)", src):
        c = int(case)
        d.text(((1 + 28 * (c % 26)) * z + 30, (1 + 28 * (c // 26)) * z + 40), "M" + type_, fill=(255, 0, 0))
    im.save(a.out)
    print(f"{a.out} écrit")


if __name__ == "__main__":
    main()
