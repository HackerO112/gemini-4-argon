#!/usr/bin/env python3
"""Lightweight static checks for the single-file HTML app."""
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import tempfile

class DocumentCheck(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = False
        self.in_title = False
        self.inline_script = False
        self.script_type = ""
        self.script_parts = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag.lower() == "title":
            self.in_title = True
        if tag.lower() == "script":
            self.script_type = (attrs.get("type") or "").lower()
            self.inline_script = not bool(attrs.get("src"))

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False
        if tag.lower() == "script":
            if self.inline_script and self.script_type in ("", "text/javascript", "module", "application/javascript"):
                self.scripts.append("".join(self.script_parts))
            self.script_parts = []
            self.inline_script = False
            self.script_type = ""

    def handle_data(self, data):
        if self.in_title and data.strip():
            self.title = True
        if self.inline_script:
            self.script_parts.append(data)

def main():
    path = Path("index.html")
    if not path.is_file():
        raise SystemExit("Missing index.html")
    parser = DocumentCheck()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    if not parser.title:
        raise SystemExit("Missing non-empty document title")
    with tempfile.TemporaryDirectory() as tmp:
        for i, script in enumerate(parser.scripts):
            js = Path(tmp) / f"inline-{i}.js"
            js.write_text(script, encoding="utf-8")
            subprocess.run(["node", "--check", str(js)], check=True)
    print(f"HTML parsed; title present; {len(parser.scripts)} inline JavaScript block(s) passed node --check.")

if __name__ == "__main__":
    main()
