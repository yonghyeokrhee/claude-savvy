#!/usr/bin/env python3
"""Extract plain text from a PDF using pypdf."""
import sys
from pypdf import PdfReader

def main():
    if len(sys.argv) != 2:
        print("usage: extract_text.py <pdf>", file=sys.stderr)
        sys.exit(2)
    reader = PdfReader(sys.argv[1])
    for i, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ""
        print(f"\n===== Page {i} =====\n{text.strip()}")

if __name__ == "__main__":
    main()
