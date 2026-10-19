#!/usr/bin/env python3
"""Vérifie la structure Markdown d'une campagne HeroQuest.

Contrôles :
  - présence de README.md et des dossiers 01-regles, 02-quetes, 03-suivi ;
  - chaque lien Markdown relatif [texte](chemin) pointe vers un fichier existant ;
  - chaque fichier NN-*.md de 02-quetes est listé dans 02-quetes/index.md ;
  - chaque fichier de quête commence par un titre « # ».

Usage : python verifier_campagne.py Campagne02
"""
import re
import sys
from pathlib import Path

LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    root = Path(sys.argv[1])
    problems = []
    if not root.is_dir():
        sys.exit(f"Dossier introuvable : {root}")

    if not (root / "README.md").exists():
        problems.append("README.md absent")
    for d in ("01-regles", "02-quetes", "03-suivi"):
        if not (root / d).is_dir():
            problems.append(f"dossier {d}/ absent")

    md_files = sorted(root.rglob("*.md"))
    for f in md_files:
        text = f.read_text(encoding="utf-8")
        for target in LINK.findall(text):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            path = target.split("#", 1)[0]
            if path and not (f.parent / path).exists():
                problems.append(f"{f.relative_to(root)} : lien cassé -> {target}")

    quetes = root / "02-quetes"
    if quetes.is_dir():
        index = quetes / "index.md"
        index_text = index.read_text(encoding="utf-8") if index.exists() else ""
        if not index.exists():
            problems.append("02-quetes/index.md absent")
        for q in sorted(quetes.glob("[0-9][0-9]-*.md")):
            if q.name not in index_text:
                problems.append(f"{q.name} absent de index.md")
            if not q.read_text(encoding="utf-8").startswith("# "):
                problems.append(f"{q.name} ne commence pas par un titre « # »")

    print(f"{len(md_files)} fichiers Markdown contrôlés dans {root}")
    if problems:
        print(f"\n{len(problems)} problème(s) :")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print("OK : structure et liens valides.")


if __name__ == "__main__":
    main()
