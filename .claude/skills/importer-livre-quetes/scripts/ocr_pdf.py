#!/usr/bin/env python3
"""OCR d'un PDF scanné (livre de quêtes) page par page, avec détection de l'orientation.

Sortie dans DOSSIER/ocr/page-NNN.txt (NNN = numéro de page du PDF, à partir de 1) et
DOSSIER/pages/page-NNN.png (page rendue, utile pour relire visuellement).
Le script reprend où il s'est arrêté : relancer la même commande tant qu'il reste des pages.
--max-seconds limite la durée d'un lancement (les outils ont une limite de temps par commande).

Usage :
  python ocr_pdf.py LIVRE.pdf --out /tmp/livre [--lang fra] [--dpi 200] [--workers 4]
                    [--pages 1-40] [--max-seconds 240] [--contact]

Prérequis : poppler (pdftoppm), tesseract, pytesseract, Pillow. Les données de langue sont
téléchargées dans DOSSIER/tessdata si elles manquent (github.com doit être joignable).
"""
import argparse
import os
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

CFG = {}


def ensure_tessdata(out: Path, lang: str) -> Path:
    td = out / "tessdata"
    td.mkdir(parents=True, exist_ok=True)
    for src in ("/usr/share/tesseract-ocr/5/tessdata", "/usr/share/tesseract-ocr/4.00/tessdata", "/usr/share/tessdata"):
        for name in ("osd", "eng"):
            f = Path(src) / f"{name}.traineddata"
            if f.exists() and not (td / f.name).exists():
                (td / f.name).write_bytes(f.read_bytes())
    target = td / f"{lang}.traineddata"
    if not target.exists():
        # peut déjà être installée au niveau système
        for src in ("/usr/share/tesseract-ocr/5/tessdata", "/usr/share/tesseract-ocr/4.00/tessdata", "/usr/share/tessdata"):
            f = Path(src) / f"{lang}.traineddata"
            if f.exists():
                target.write_bytes(f.read_bytes())
                break
    if not target.exists():
        url = f"https://raw.githubusercontent.com/tesseract-ocr/tessdata_fast/main/{lang}.traineddata"
        print(f"Téléchargement de {url}", flush=True)
        urllib.request.urlretrieve(url, target)
    return td


def n_pages(pdf: str) -> int:
    info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True, check=True).stdout
    return int(next(l.split()[1] for l in info.splitlines() if l.startswith("Pages:")))


def parse_range(s, total):
    if not s:
        return list(range(1, total + 1))
    a, _, b = s.partition("-")
    return list(range(int(a), int(b or a) + 1))


def score(im, lang):
    import pytesseract
    d = pytesseract.image_to_data(im, lang=lang, config="--psm 3", output_type=pytesseract.Output.DICT)
    return sum(1 for t, c in zip(d["text"], d["conf"]) if len(t) >= 3 and t.isalpha() and float(c) > 70)


def work(args):
    pdf, out, page, lang, dpi, tessdata = args
    os.environ["TESSDATA_PREFIX"] = tessdata
    from PIL import Image, ImageOps
    import pytesseract
    png = Path(out) / "pages" / f"page-{page:03d}.png"
    if not png.exists():
        prefix = str(png)[:-4]
        subprocess.run(["pdftoppm", "-png", "-r", str(dpi), "-f", str(page), "-l", str(page), "-singlefile", pdf, prefix], check=True)
    im = Image.open(png).convert("L")
    im = ImageOps.autocontrast(im, cutoff=1)
    small = im.resize((im.width // 2, im.height // 2))
    sc = {r: score(small.rotate(r, expand=True), lang) for r in (0, 180)}
    if max(sc.values()) < 15:  # page peu textuelle : tester aussi les quarts de tour
        sc.update({r: score(small.rotate(r, expand=True), lang) for r in (90, 270)})
    rot = max(sc, key=sc.get)
    text = pytesseract.image_to_string(im.rotate(rot, expand=True), lang=lang, config="--psm 3")
    (Path(out) / "ocr" / f"page-{page:03d}.txt").write_text(text, encoding="utf-8")
    return page, rot, sc[rot]


def contact_sheet(pdf, out, pages):
    from PIL import Image
    tmp = Path(out) / "contact"
    tmp.mkdir(exist_ok=True)
    subprocess.run(["pdftoppm", "-jpeg", "-r", "30", pdf, str(tmp / "c")], check=True)
    files = sorted(tmp.glob("c-*.jpg"))
    if not files:
        return
    w, h = Image.open(files[0]).size
    cols = 8
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * h), "white")
    for i, f in enumerate(files):
        sheet.paste(Image.open(f).convert("RGB"), ((i % cols) * w, (i // cols) * h))
    sheet.save(Path(out) / "contact.jpg", quality=80)
    print(f"Planche-contact : {Path(out) / 'contact.jpg'}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--out", required=True)
    ap.add_argument("--lang", default="fra")
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--pages")
    ap.add_argument("--max-seconds", type=int, default=240)
    ap.add_argument("--contact", action="store_true", help="crée aussi une planche-contact des pages")
    a = ap.parse_args()

    out = Path(a.out)
    (out / "ocr").mkdir(parents=True, exist_ok=True)
    (out / "pages").mkdir(parents=True, exist_ok=True)
    tessdata = str(ensure_tessdata(out, a.lang))
    total = n_pages(a.pdf)
    wanted = parse_range(a.pages, total)
    todo = [p for p in wanted if not (out / "ocr" / f"page-{p:03d}.txt").exists()]
    print(f"{total} pages dans le PDF ; {len(todo)} à traiter sur {len(wanted)} demandées.", flush=True)

    if a.contact:
        contact_sheet(a.pdf, out, wanted)

    start = time.time()
    done = []
    with ProcessPoolExecutor(a.workers) as ex:
        it = iter(todo)
        pending = {}
        for _ in range(a.workers):
            p = next(it, None)
            if p:
                pending[ex.submit(work, (a.pdf, str(out), p, a.lang, a.dpi, tessdata))] = p
        while pending:
            for fut in as_completed(list(pending)):
                p = pending.pop(fut)
                page, rot, words = fut.result()
                done.append(page)
                print(f"page {page:03d}  rotation {rot:>3}  mots fiables {words}", flush=True)
                if time.time() - start < a.max_seconds:
                    nxt = next(it, None)
                    if nxt:
                        pending[ex.submit(work, (a.pdf, str(out), nxt, a.lang, a.dpi, tessdata))] = nxt
                break
    left = [p for p in wanted if not (out / "ocr" / f"page-{p:03d}.txt").exists()]
    if left:
        print(f"\nIl reste {len(left)} page(s) : relancer la même commande.")
    else:
        print("\nOCR terminé. Pages sans texte (cartes, illustrations) : taille de fichier < 50 octets.")


if __name__ == "__main__":
    main()
