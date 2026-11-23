#!/usr/bin/env python3
"""Add the Cloudflare Web Analytics beacon to generated HTML before deployment."""
import argparse
import os
from pathlib import Path
import re
import sys

BEACON = "https://static.cloudflareinsights.com/beacon.min.js"
BEACON_TAG = re.compile(r'<script\b[^>]*src=["\']https://static\.cloudflareinsights\.com/beacon\.min\.js["\'][^>]*>\s*</script>', re.I)
BODY_END = re.compile(r"</body\s*>", re.I)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, default=Path("build"))
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    pages = sorted(args.site.rglob("*.html"))
    if not pages:
        parser.error("No built HTML files found")
    token = os.environ.get("CLOUDFLARE_WEB_ANALYTICS_TOKEN", "").strip()
    if not args.verify and not re.fullmatch(r"[a-fA-F0-9]{32}", token):
        parser.error("Set CLOUDFLARE_WEB_ANALYTICS_TOKEN to your 32-character public Cloudflare site token")
    errors = []
    updated_count = 0
    for path in pages:
        html = path.read_text(encoding="utf-8")
        count = html.count(BEACON)
        if args.verify:
            if count != 1:
                errors.append(f"{path}: expected one beacon, found {count}")
            continue
        tag = '<script defer src="' + BEACON + '" data-cf-beacon=' + "'{\"token\":\"" + token + "\"}'" + '></script>'
        if count:
            updated, replacements = BEACON_TAG.subn(lambda _: tag, html)
            if replacements != count:
                errors.append(f"{path}: existing beacon could not be safely updated")
                continue
        else:
            updated, replacements = BODY_END.subn(lambda _: "  " + tag + "\n</body>", html, count=1)
            if replacements != 1:
                errors.append(f"{path}: missing closing body tag")
                continue
        if updated != html:
            path.write_text(updated, encoding="utf-8")
            updated_count += 1
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Cloudflare Web Analytics: {len(pages)} HTML files checked; {updated_count} modified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
