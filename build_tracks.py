#!/usr/bin/env python3
"""Build tracks.json for the Euclidean Ear Test.

Folder layout (next to this script):
  audio/   e{k}-{n}_{Track title}.mp3     e.g. e4-15_Duh_Poteca.mp3
  cards/   e{k}-{n}.webp                  (.png, .jpg also work)
  rhythms.json                            names, descriptions, mnemonics (edit by hand)

Run:  python3 build_tracks.py

Only the start of an audio name (e{k}-{n}_) and the .mp3 ending matter.
The title part can use any letters: capitals, Greek, Cyrillic, diacritics.
Several clips can share one rhythm: add more files with the same e{k}-{n} start.
New rhythms get an empty entry in rhythms.json for you to fill in.
"""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AUDIO = ROOT / "audio"
CARDS = ROOT / "cards"
META = ROOT / "rhythms.json"
OUT = ROOT / "tracks.json"

N_MIN, N_MAX = 2, 16          # allowed steps
CARD_EXTS = (".webp", ".png", ".jpg", ".jpeg")   # first match wins
FILE_RE = re.compile(r"^e(\d+)-(\d+)_(.+)\.mp3$", re.IGNORECASE)


def nfc(text):
    """Write accented and non-Latin letters in one standard form, so the web address
    matches what GitHub stores whether the files came from a Mac, Windows or Linux."""
    return unicodedata.normalize("NFC", text)


def find_card(rid):
    if not CARDS.is_dir():
        return None
    names = {}
    for path in CARDS.iterdir():
        if path.suffix.lower() in CARD_EXTS:
            names.setdefault((nfc(path.stem).lower(), path.suffix.lower()), nfc(path.name))
    for ext in CARD_EXTS:
        if (rid, ext) in names:
            return f"cards/{names[(rid, ext)]}"      # the real file name, so it also matches online
    return None


def check_mnemonic(rid, text):
    """Mnemonics hold one syllable per step: n syllables, k of them in CAPITALS. _ is a rest."""
    m = re.match(r"e(\d+)-(\d+)$", rid)
    if not (m and text):
        return
    k, n = int(m.group(1)), int(m.group(2))
    tokens = re.findall(r"_|[^-_]+", text)
    pulses = [t for t in tokens if t != "_" and t == t.upper() and t != t.lower()]
    if len(tokens) != n or len(pulses) != k:
        print(f"check  {rid}: mnemonic has {len(tokens)} syllables and {len(pulses)} capitalised; E({k},{n}) needs {n} and {k}")


def main():
    meta = json.loads(META.read_text(encoding="utf-8")) if META.exists() else {}
    rhythms = {}

    for path in sorted(AUDIO.iterdir()) if AUDIO.is_dir() else []:
        if path.suffix.lower() != ".mp3":
            if not path.name.startswith("."):
                print(f"skip   {path.name}: not an .mp3 file")
            continue
        name = nfc(path.name)
        m = FILE_RE.match(name)
        if not m:
            print(f"skip   {path.name}: does not match e{{k}}-{{n}}_{{title}}.mp3")
            continue
        k, n, title = int(m.group(1)), int(m.group(2)), m.group(3).replace("_", " ")
        if not (N_MIN <= n <= N_MAX and 1 <= k <= n - 1):
            print(f"skip   {path.name}: E({k},{n}) is outside n {N_MIN}-{N_MAX}, k 1..n-1")
            continue
        bad = [c for c in name if c in '#%?\\:*"<>|']
        if bad:
            print(f"warn   {path.name}: the character {bad[0]!r} can cause trouble online; consider removing it")
        rid = f"e{k}-{n}"
        entry = rhythms.setdefault(rid, {"id": rid, "k": k, "n": n, "versions": []})
        entry["versions"].append({"file": f"audio/{name}", "title": title})

    ordered = sorted(rhythms.values(), key=lambda r: (r["n"], r["k"]))
    new_meta = dict(meta)

    for r in ordered:
        rid = r["id"]
        if rid not in new_meta:
            new_meta[rid] = {"name": "", "description": "", "mnemonic": ""}
            print(f"new    {rid}: added an empty entry to rhythms.json")
        info = new_meta[rid]
        r["name"] = info.get("name", "")
        r["description"] = info.get("description", "")
        r["mnemonic"] = info.get("mnemonic", "")
        r["card"] = find_card(rid)
        if not r["card"]:
            print(f"warn   {rid}: no card image found in cards/")

    # keep rhythms.json tidy: sorted by n, then k
    def sort_key(item):
        m = re.match(r"e(\d+)-(\d+)$", item[0])
        return (int(m.group(2)), int(m.group(1))) if m else (999, 999)

    META.write_text(
        json.dumps(dict(sorted(new_meta.items(), key=sort_key)), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    OUT.write_text(json.dumps({"rhythms": ordered}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for rid, info in new_meta.items():
        check_mnemonic(rid, info.get("mnemonic", ""))

    clips = sum(len(r["versions"]) for r in ordered)
    print(f"done   {len(ordered)} rhythms, {clips} clips -> {OUT.name}")


if __name__ == "__main__":
    main()
