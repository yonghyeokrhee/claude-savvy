#!/usr/bin/env python3
"""Download a PDF from a URL to a local path."""
import sys
import requests

def main():
    if len(sys.argv) != 3:
        print("usage: fetch_pdf.py <url> <out.pdf>", file=sys.stderr)
        sys.exit(2)
    url, out = sys.argv[1], sys.argv[2]
    r = requests.get(url, timeout=60, headers={"User-Agent": "pdf-to-deck/1.0"})
    r.raise_for_status()
    with open(out, "wb") as f:
        f.write(r.content)
    print(f"saved {len(r.content):,} bytes -> {out}")

if __name__ == "__main__":
    main()
