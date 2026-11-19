"""Search the icon set.

Examples:
  python find.py --list                 every icon id, grouped by category (compact)
  python find.py --list --details       every icon with name, colour, aliases, licence
  python find.py --categories           every category with a count
  python find.py --category database    icons in one category
  python find.py k8s postgres "next.js" look up names, aliases or partial names
  python find.py react --json           machine-readable output
"""
import argparse
import json
from collections import Counter

from _common import build_index, load_manifest, normalize, split_names, suggest


def search(term, manifest, index):
    """Exact id/name/alias match first, then partial matches, then fuzzy suggestions."""
    key = normalize(term)
    if key in index:
        return [index[key]], "exact"
    partial = [
        icon for icon in manifest
        if any(key in normalize(k) for k in [icon["id"], icon["name"], *icon["aliases"]])
    ]
    if partial:
        return partial, "partial"
    by_id = {icon["id"]: icon for icon in manifest}
    return [by_id[i] for i in suggest(term, index)], "suggestion"


def print_table(icons):
    for icon in icons:
        aliases = ", ".join(icon["aliases"]) or "-"
        license = f"  licence: {icon['license']}" if icon.get("license") else ""
        guidelines = f"  guidelines: {icon['guidelines']}" if icon.get("guidelines") else ""
        print(f"  {icon['id']:<16} {icon['name']:<16} {icon['category']:<10} {icon['hex']}  aliases: {aliases}{license}{guidelines}")


def print_compact(icons):
    """Ids only, one line per category: about a fifth of the tokens of the full table."""
    by_category = {}
    for icon in icons:
        by_category.setdefault(icon["category"], []).append(icon["id"])
    for cat, ids in sorted(by_category.items()):
        print(f"{cat}: {', '.join(ids)}")
    print("(look up names with find.py <name> for details and licences, or add --details)")


def main():
    p = argparse.ArgumentParser(description="Search the dev-icons set.")
    p.add_argument("query", nargs="*", help="names, aliases or partial names (comma or space separated)")
    p.add_argument("--list", action="store_true", help="list every icon id, grouped by category")
    p.add_argument("--details", action="store_true", help="with --list or --category: show the full table")
    p.add_argument("--category", help="only icons in this category")
    p.add_argument("--categories", action="store_true", help="list categories with counts")
    p.add_argument("--json", action="store_true", help="print JSON instead of a table")
    args = p.parse_args()

    manifest = load_manifest()
    index = build_index(manifest)

    if args.categories:
        counts = Counter(icon["category"] for icon in manifest)
        if args.json:
            print(json.dumps(dict(sorted(counts.items())), indent=2))
        else:
            for cat, n in sorted(counts.items()):
                print(f"  {cat:<12} {n}")
        return

    terms = split_names(args.query)
    if not terms:
        icons = [i for i in manifest if not args.category or i["category"] == args.category]
        if args.json:
            print(json.dumps(icons, indent=2))
        elif args.details:
            print(f"{len(icons)} icons:")
            print_table(icons)
        else:
            print(f"{len(icons)} icons:")
            print_compact(icons)
        return

    results = {}
    for term in terms:
        icons, kind = search(term, manifest, index)
        if args.category:
            icons = [i for i in icons if i["category"] == args.category]
        results[term] = {"match": kind if icons else "none", "icons": icons}

    if args.json:
        print(json.dumps(results, indent=2))
        return
    for term, r in results.items():
        if r["match"] == "none":
            print(f'"{term}": no match')
        elif r["match"] == "suggestion":
            print(f'"{term}": not found, did you mean:')
            print_table(r["icons"])
        else:
            print(f'"{term}":')
            print_table(r["icons"])


if __name__ == "__main__":
    main()
