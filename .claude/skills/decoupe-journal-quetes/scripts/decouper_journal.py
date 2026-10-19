#!/usr/bin/env python3
"""Découpe un journal de quêtes HeroQuest (TXT) en un fichier Markdown par quête.

Règle de découpe (identique à Campagne01/02-quetes) :
  - une quête commence à une ligne qui débute par « ⚔️ Quête N : Titre »
    (casse indifférente : « QUÊTE » accepté) ;
  - le fichier contient la tranche du journal jusqu'à la quête suivante,
    recopiée telle quelle (aucune reformulation) ;
  - seule la première ligne change : on lui ajoute « # » pour en faire un titre ;
  - les lignes vides de fin de tranche sont retirées ;
  - le TXT d'origine n'est jamais modifié.

Usage :
  python decouper_journal.py JOURNAL.txt [--out DOSSIER] [--slug N=mon-slug ...]
                             [--dry-run] [--force] [--no-index]
"""
import argparse
import re
import sys
import unicodedata
from pathlib import Path

# ⚔ (U+2694) suivi ou non de U+FE0F, puis « Quête N : Titre » en début de ligne.
MARKER = re.compile(
    r"^\s*\u2694\ufe0f?\s*qu[êe]te\s+(\d+)\s*:\s*(.+?)\s*$", re.IGNORECASE
)
LINK = re.compile(r"Qu[êe]te\s+(\d+)\s*\(([^)]+)\)", re.IGNORECASE)
STOP = {"le", "la", "les", "l", "un", "une", "des", "de", "du", "d", "et", "a", "au", "aux", "en"}
ARTICLES = {"le", "la", "les", "l", "un", "une"}


def unaccent(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def tokens(s: str) -> list:
    s = unaccent(s).lower().replace("’", " ").replace("'", " ")
    return re.findall(r"[a-z0-9]+", s)


def slugify(title: str) -> str:
    """Titre -> slug : sous-titre après ' – ' coupé, article initial retiré, sans accents."""
    title = re.split(r"\s[–—-]\s", title, maxsplit=1)[0]
    s = unaccent(title).lower().replace("’", "").replace("'", "")
    words = re.findall(r"[a-z0-9]+", s)
    # « L'Épreuve » -> l + epreuve : l'élision a été supprimée plus haut, on retire donc
    # l'article seulement s'il est un mot isolé.
    raw = re.findall(r"[a-z0-9’']+", unaccent(title).lower())
    if raw and re.sub(r"[’'].*", "", raw[0]) in ARTICLES and (
        raw[0] in ARTICLES or "’" in raw[0] or "'" in raw[0]
    ):
        first = raw[0]
        if first in ARTICLES:
            words = re.findall(r"[a-z0-9]+", re.sub(r"[’']", "", " ".join(raw[1:])))
        else:  # forme élidée : l'epreuve -> epreuve
            rest = re.split(r"[’']", first, maxsplit=1)[1]
            words = re.findall(r"[a-z0-9]+", " ".join([rest] + raw[1:]))
    return "-".join(words)


def parse(lines):
    marks = []
    for i, line in enumerate(lines):
        m = MARKER.match(line)
        if m:
            marks.append((i, int(m.group(1)), m.group(2)))
    return marks


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("journal", type=Path)
    ap.add_argument("--out", type=Path, help="dossier de sortie (défaut : <dossier du journal>/02-quetes)")
    ap.add_argument("--slug", action="append", default=[], metavar="N=slug", help="impose le slug de la quête N")
    ap.add_argument("--dry-run", action="store_true", help="n'écrit rien, affiche le plan")
    ap.add_argument("--force", action="store_true", help="autorise l'écrasement de fichiers existants")
    ap.add_argument("--no-index", action="store_true", help="ne génère pas index.md")
    a = ap.parse_args()

    text = a.journal.read_text(encoding="utf-8-sig")
    lines = text.split("\n")
    marks = parse(lines)
    if not marks:
        sys.exit("Aucun marqueur « ⚔️ Quête N : Titre » trouvé : vérifier le format du journal.")

    nums = [n for _, n, _ in marks]
    warnings = []
    dup = sorted({n for n in nums if nums.count(n) > 1})
    if dup:
        sys.exit(f"Numéros de quête en double : {dup}. Corriger ou arbitrer avant de découper.")
    if nums != sorted(nums):
        warnings.append(f"Ordre des quêtes non croissant dans le journal : {nums}")
    missing = [n for n in range(min(nums), max(nums) + 1) if n not in nums]
    if missing:
        warnings.append(f"Numéros manquants entre {min(nums)} et {max(nums)} : {missing}")
    pre = [l for l in lines[: marks[0][0]] if l.strip()]
    if pre:
        warnings.append(f"{len(pre)} ligne(s) non vides avant la première quête : non reprises dans les fichiers.")

    overrides = {}
    for s in a.slug:
        k, _, v = s.partition("=")
        overrides[int(k)] = v

    out = a.out or a.journal.parent / "02-quetes"
    bounds = [i for i, _, _ in marks] + [len(lines)]
    plan = []
    for k, (i, n, title) in enumerate(marks):
        chunk = lines[bounds[k] : bounds[k + 1]]
        while chunk and not chunk[-1].strip():
            chunk.pop()
        chunk[0] = "# " + chunk[0].strip()
        slug = overrides.get(n) or slugify(title)
        plan.append({"n": n, "title": title, "name": f"{n:02d}-{slug}.md", "chunk": chunk, "start": i + 1})

    names = [p["name"] for p in plan]
    if len(set(names)) != len(names):
        sys.exit("Deux quêtes donnent le même nom de fichier : utiliser --slug N=...")

    # Contrôle croisé des « Lien avec la Quête N (Titre) ».
    by_num = {p["n"]: p for p in plan}
    title_tokens = {p["n"]: {t for t in tokens(p["title"]) if t not in STOP} for p in plan}
    issues = []
    for p in plan:
        for off, line in enumerate(p["chunk"]):
            for m in LINK.finditer(line):
                ref, label = int(m.group(1)), m.group(2).strip()
                lt = {t for t in tokens(label) if t not in STOP}
                if not lt:
                    continue
                where = f"Quête {p['n']}, ligne {p['start'] + off} du journal"
                if ref not in by_num:
                    issues.append(f"{where} : renvoie à la Quête {ref} ({label}), absente du journal.")
                    continue
                tt = title_tokens[ref]
                if lt <= tt or tt <= lt:
                    continue
                other = [q for q in title_tokens if q != ref and (lt <= title_tokens[q] or title_tokens[q] <= lt)]
                if other:
                    issues.append(
                        f"{where} : « Quête {ref} ({label}) » mais « {label} » correspond à la Quête {other[0]} "
                        f"({by_num[other[0]]['title']}) ; la Quête {ref} est « {by_num[ref]['title']} »."
                    )
                else:
                    issues.append(
                        f"{where} : « Quête {ref} ({label}) » ne correspond pas au titre de la Quête {ref} "
                        f"(« {by_num[ref]['title']} »)."
                    )
    issues = list(dict.fromkeys(issues))

    # Rapport.
    print(f"Journal : {a.journal}  ({len(lines)} lignes)")
    print(f"Sortie  : {out}{'  [dry-run]' if a.dry_run else ''}\n")
    for p in plan:
        print(f"  {p['name']:<48} {len(p['chunk']):>4} lignes   « {p['title']} »")
    for w in warnings:
        print(f"\nAVERTISSEMENT : {w}")
    if issues:
        print(f"\nRenvois à vérifier ({len(issues)}) :")
        for x in issues:
            print(f"  - {x}")

    if a.dry_run:
        return

    # Écriture sans écraser, sauf --force.
    targets = [out / p["name"] for p in plan] + ([] if a.no_index else [out / "index.md"])
    clash = [t for t in targets if t.exists()]
    if clash and not a.force:
        sys.exit("\nFichiers déjà présents (aucune écriture faite) : "
                 + ", ".join(t.name for t in clash) + "\nRelancer avec --force pour les remplacer.")
    out.mkdir(parents=True, exist_ok=True)
    for p in plan:
        (out / p["name"]).write_text("\n".join(p["chunk"]) + "\n", encoding="utf-8")

    if not a.no_index:
        idx = [
            "# Index des quêtes",
            "",
            f"Ordre et titres tels qu'ils apparaissent dans `../{a.journal.name}`. "
            "Chaque quête est la tranche correspondante du journal, recopiée sans modification.",
            "",
            "| N° | Quête | Fichier |",
            "| ---: | --- | --- |",
        ]
        for p in plan:
            idx.append(f"| {p['n']} | {p['title']} | [{p['name']}]({p['name']}) |")
        if warnings or issues:
            idx += ["", "## Points à arbitrer", "",
                    "> Détectés automatiquement lors du découpage. Les sources sont conservées telles quelles ; "
                    "aucune correction n'est faite sans validation.", ""]
            idx += [f"- {w}" for w in warnings] + [f"- {x}" for x in issues]
        (out / "index.md").write_text("\n".join(idx) + "\n", encoding="utf-8")

    # Vérification : chaque fichier relu == tranche du journal (hors « # » et lignes vides finales).
    bad = []
    for p in plan:
        got = (out / p["name"]).read_text(encoding="utf-8").rstrip("\n").split("\n")
        exp = lines[bounds[plan.index(p)] : bounds[plan.index(p) + 1]]
        while exp and not exp[-1].strip():
            exp.pop()
        if got[0] != "# " + exp[0].strip() or got[1:] != exp[1:]:
            bad.append(p["name"])
    if bad:
        sys.exit(f"\nÉCHEC de la vérification : {bad}")
    print(f"\nOK : {len(plan)} fichiers écrits et vérifiés contre le journal. Source non modifiée.")


if __name__ == "__main__":
    main()
