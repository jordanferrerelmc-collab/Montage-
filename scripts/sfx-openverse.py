#!/usr/bin/env python3
"""Effets sonores depuis Openverse (https://openverse.org, API https://api.openverse.org) : sons sous licence libre.

Usage :
  npm run sfx:openverse -- cherche "crowd cheer stadium" [--max 8] [--duree 15] [--licences cc0,pdm,by]
  npm run sfx:openverse -- prends <id Openverse> <nom> [--debut 1.2 --fin 4.0] [--fichier son-envoye.mp3]
  npm run sfx:openverse -- sync            (retélécharge tous les sons du manifeste dans une nouvelle session)
  npm run sfx:openverse -- credits [nom…]  (lignes de crédit à coller dans la description de la vidéo)

Les sons vont dans effets/sfx/openverse/<nom>.wav (mono 48 kHz, volume homogène) ; ils ne sont pas versionnés.
Le manifeste effets/sfx/openverse/manifest.json (versionné) garde l'identifiant, l'auteur, la licence et les liens.

Licences acceptées par défaut : cc0 et pdm (domaine public, aucun crédit) et by (crédit de l'auteur OBLIGATOIRE dans la
description). Refusées : nc (pas d'usage commercial), nd (pas de modification : un mixage en est une), sa (partage à
l'identique). Réseau : api.openverse.org est autorisé (recherche). Le téléchargement depuis cdn.freesound.org est REFUSÉ par
le filtrage de la plateforme (403, constaté le 13/11/2026) : l'utilisateur télécharge le son sur la page indiquée par
« cherche » et l'envoie ; on l'importe avec --fichier (licence et crédit repris d'Openverse).
"""
import argparse, json, os, re, subprocess, sys, tempfile, urllib.error, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/effets/sfx/openverse"
MANIFEST = f"{OUT}/manifest.json"
API = "https://api.openverse.org/v1/audio/"
UA = {"User-Agent": "montage-sfx/1.0 (atelier video)"}
OK = {"cc0", "pdm", "by"}

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()

def manifest():
    return json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}

def save(m):
    os.makedirs(OUT, exist_ok=True)
    json.dump(m, open(MANIFEST, "w"), indent=2, ensure_ascii=False, sort_keys=True)

def norm(src, name, e):
    trim = (["-ss", str(e["debut"])] if e.get("debut") is not None else []) + (["-to", str(e["fin"])] if e.get("fin") is not None else [])
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *trim, "-i", src, "-ac", "1", "-ar", "48000",
                    "-af", "loudnorm=I=-16:TP=-1.5", f"{OUT}/{name}.wav"], check=True)

def fetch(name, e, fichier=None):
    """Télécharge (ou importe un fichier envoyé) et normalise un son du manifeste."""
    os.makedirs(OUT, exist_ok=True)
    if fichier:
        return norm(fichier, name, e)
    with tempfile.NamedTemporaryFile(suffix=os.path.splitext(urllib.parse.urlparse(e["url"]).path)[1] or ".mp3") as tmp:
        try:
            tmp.write(get(e["url"])); tmp.flush()
        except urllib.error.HTTPError as err:
            sys.exit(f"téléchargement refusé ({err.code}) pour {e['url']}\n→ demander à l'utilisateur de télécharger le son sur {e['page']} et de l'envoyer, puis relancer avec --fichier")
        norm(tmp.name, name, e)

def credit(name, e):
    lic = e["licence"].upper() + (f" {e['version']}" if e.get("version") else "")
    if e["licence"] in ("cc0", "pdm"):
        return f"{name} : « {e['titre']} » ({lic}, domaine public, crédit facultatif) — {e['page']}"
    return f"« {e['titre']} » par {e['auteur']} — licence CC {lic} — {e['page']}"

p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sub = p.add_subparsers(dest="cmd", required=True)
s = sub.add_parser("cherche"); s.add_argument("q"); s.add_argument("--max", type=int, default=8)
s.add_argument("--duree", type=float, default=20, help="durée maximale en secondes"); s.add_argument("--licences", default="cc0,pdm,by")
s = sub.add_parser("prends"); s.add_argument("id"); s.add_argument("nom"); s.add_argument("--debut", type=float); s.add_argument("--fin", type=float); s.add_argument("--fichier")
sub.add_parser("sync")
s = sub.add_parser("credits"); s.add_argument("noms", nargs="*")
a = p.parse_args()

if a.cmd == "cherche":
    lic = ",".join(l for l in a.licences.split(",") if l in OK) or "cc0,pdm,by"
    out, page = [], 1
    while len(out) < a.max and page <= 4:
        d = json.loads(get(API + "?" + urllib.parse.urlencode({"q": a.q, "license": lic, "page_size": 20, "page": page})))
        for r in d.get("results", []):
            if (r.get("duration") or 0) / 1000 <= a.duree and r["license"] in OK:
                out.append(r)
        if page >= d.get("page_count", 1): break
        page += 1
    for r in out[:a.max]:
        print(f"{r['id']}  {(r.get('duration') or 0) / 1000:5.1f} s  {r['license']:4} {r['title'][:50]}  — {r.get('creator') or '?'}\n      {r.get('foreign_landing_url')}")
    print(f"{len(out[:a.max])} résultat(s) pour « {a.q} » (licences {lic}, ≤ {a.duree:g} s)")

elif a.cmd == "prends":
    r = json.loads(get(API + a.id + "/"))
    if r["license"] not in OK:
        sys.exit(f"licence refusée : {r['license']} (acceptées : {', '.join(sorted(OK))})")
    name = re.sub(r"[^a-z0-9-]+", "-", a.nom.lower()).strip("-")
    e = {"id": r["id"], "titre": r["title"], "auteur": r.get("creator") or "inconnu", "licence": r["license"], "version": r.get("license_version"),
         "licence_url": r.get("license_url"), "page": r.get("foreign_landing_url"), "source": r["provider"], "url": r["url"],
         "debut": a.debut, "fin": a.fin}
    fetch(name, e, a.fichier)
    m = manifest(); m[name] = e; save(m)
    print(f"✓ {OUT}/{name}.wav\n  crédit : {credit(name, e)}")

elif a.cmd == "sync":
    m = manifest()
    for name, e in m.items():
        if not os.path.exists(f"{OUT}/{name}.wav"):
            fetch(name, e); print(f"✓ {name}")
    print(f"{len(m)} son(s) Openverse dans {OUT}")

elif a.cmd == "credits":
    m = manifest()
    for name in (a.noms or sorted(m)):
        if name in m: print(credit(name, m[name]))
