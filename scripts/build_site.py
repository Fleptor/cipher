#!/usr/bin/env python3
"""Package only CIPHER's public showcase files; Python standard library only."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
import shutil
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                raise ValueError(f"Duplicate HTML id: {attrs['id']}")
            self.ids.add(attrs["id"])
        for name in ("href", "src", "poster"):
            if name in attrs:
                self.links.append(attrs[name])


def build(output):
    output.mkdir(parents=True, exist_ok=True)
    # An explicit allowlist keeps runtime data, credentials and the dashboard out.
    for name in ("index.html", "style.css", "favicon.svg"):
        shutil.copy2(ROOT / "website" / name, output / name)
    assets = output / "assets"
    assets.mkdir(exist_ok=True)
    for name in ("CIPHER_Startup_Alley_Pitch.pdf", "CIPHER_Startup_Alley_Pitch.pptx", "CIPHER_Presenter_Notes.txt"):
        shutil.copy2(ROOT / "docs/presentation" / name, assets / name)
    shutil.copy2(ROOT / "docs/showcase/plain-english-incidents.png", assets / "incident.png")
    shutil.copy2(ROOT / "docs/demo/CIPHER_demo.mp4", assets / "CIPHER_demo.mp4")
    (output / ".nojekyll").touch()

    parser = Links()
    parser.feed((output / "index.html").read_text(encoding="utf-8"))
    for link in parser.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        if url.path:
            target = (output / unquote(url.path)).resolve()
            if not target.is_relative_to(output.resolve()) or not target.is_file():
                raise ValueError(f"Missing or nonlocal asset: {link}")
        elif url.fragment and url.fragment not in parser.ids:
            raise ValueError(f"Missing section: {link}")
    with ZipFile(assets / "CIPHER_Startup_Alley_Pitch.pptx") as deck:
        slides = [n for n in deck.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")]
        if len(slides) != 10:
            raise ValueError(f"Expected 10 slides, found {len(slides)}")
    print(f"Packaged {output}: all local links resolve, 10-slide deck included.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / ".local/site")
    build(parser.parse_args().output)
