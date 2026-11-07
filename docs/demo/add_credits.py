#!/usr/bin/env python3
"""Append an eight-second team credit card to the original, uncredited demo.

Requires the brochure Python dependencies, pdftoppm and ffmpeg. The input must
be the 1440 x 900, 25 fps recording without an existing credit card.
"""
import argparse
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
BRAND = ROOT / "website/brand"
CREDITS = json.loads((ROOT / "docs/project-credits.json").read_text())
THEME = json.loads((BRAND / "theme.json").read_text())


def credit_card(path):
    for name in ("Montserrat-Bold", "OpenSans-Regular"):
        pdfmetrics.registerFont(TTFont(name, str(BRAND / "fonts" / f"{name}.ttf")))
    c = canvas.Canvas(str(path), pagesize=(1440, 900), lang="en-US", invariant=1)
    c.setTitle("CIPHER project credits")
    c.setAuthor("; ".join(CREDITS["members"]))

    def rect(x, y, w, h, color):
        c.setFillColor(colors.HexColor(f"#{color}"))
        c.rect(x, y, w, h, fill=1, stroke=0)

    def text(value, x, y, size, color="FFFFFF", font="OpenSans-Regular"):
        c.setFillColor(colors.HexColor(f"#{color}"))
        c.setFont(font, size)
        c.drawString(x, y, value)

    def logo(name, x, y, width):
        image = ImageReader(str(BRAND / THEME[name]))
        w, h = image.getSize()
        c.drawImage(image, x, y, width=width, height=width*h/w, mask="auto")

    rect(0, 0, 1440, 900, THEME["dark"])
    rect(0, 893, 1440, 7, THEME["orange"])
    text("CIPHER", 100, 785, 64, font="Montserrat-Bold")
    text(CREDITS["team"].upper(), 104, 700, 20, THEME["orange"], "Montserrat-Bold")
    for name, x, y in zip(CREDITS["members"], [104, 760, 104, 760], [610, 610, 530, 530]):
        text(name, x, y, 34, font="Montserrat-Bold")
    text("CONTRIBUTOR", 104, 422, 17, "C6C6C6", "Montserrat-Bold")
    text(CREDITS["contributor"], 104, 370, 32)
    rect(0, 0, 1440, 235, "FFFFFF")
    logo("society_logo", 104, 85, 270)
    text("IEEE BAU Computer Society", 495, 133, 24, THEME["ink"])
    text("belalhamdan.com/cipher/", 495, 87, 21, THEME["blue"])
    logo("branch_logo", 1140, 70, 196)
    c.showPage()
    c.save()


def build(recording, output):
    recording, output = recording.resolve(), output.resolve()
    if recording == output:
        raise ValueError("Use a separate output path to preserve the original recording")
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix="cipher-credits-") as directory:
        tmp = Path(directory)
        credit_card(tmp / "credits.pdf")
        subprocess.run(["pdftoppm", "-singlefile", "-r", "72", "-png",
                        str(tmp / "credits.pdf"), str(tmp / "credits")], check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-loop", "1", "-framerate", "25",
                        "-i", str(tmp / "credits.png"), "-t", "8", "-c:v", "libx264",
                        "-profile:v", "high", "-level:v", "4.0", "-pix_fmt", "yuv420p",
                        "-video_track_timescale", "12800", str(tmp / "credits.mp4")], check=True)
        (tmp / "recording.mp4").symlink_to(recording)
        (tmp / "concat.txt").write_text("file 'recording.mp4'\nfile 'credits.mp4'\n")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                        "-i", str(tmp / "concat.txt"), "-c", "copy", "-movflags", "+faststart",
                        "-metadata", "title=CIPHER software demonstration",
                        "-metadata", f"artist={'; '.join(CREDITS['members'])} ({CREDITS['team']})",
                        "-metadata", f"comment=Contributor: {CREDITS['contributor']}",
                        str(output)], check=True)
    print(f"Created {output}; original recording followed by eight seconds of credits")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Original recording without credits")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    build(args.input, args.output)
