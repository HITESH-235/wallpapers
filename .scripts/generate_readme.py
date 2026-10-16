#!/usr/bin/env python3
import os
import re
import urllib.parse
from pathlib import Path
from collections import Counter

REPO_DIR = Path(__file__).resolve().parent.parent if Path(__file__).parent.name == ".scripts" else Path(__file__).resolve().parent

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
    ".avif",
    ".bmp",
    ".svg",
}

def slugify(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = slug.replace(" ", "-")
    return "#" + slug

def generate_readme():
    files = [
        f for f in os.listdir(REPO_DIR)
        if os.path.isfile(REPO_DIR / f)
        and not f.startswith(".")
        and os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS
    ]
    files.sort()

    stems = [os.path.splitext(f)[0] for f in files]
    stem_counts = Counter(stems)

    entries = []
    for filename in files:
        stem, ext = os.path.splitext(filename)
        if stem_counts[stem] > 1:
            display_name = f"{stem} ({ext.lstrip('.').upper()})"
        else:
            display_name = stem
        anchor = slugify(display_name)
        encoded_file = urllib.parse.quote(filename)
        entries.append({
            "filename": filename,
            "display_name": display_name,
            "anchor": anchor,
            "encoded_file": encoded_file,
        })

    lines = [
        "# 🖼️ Wallpapers Collection",
        "",
        "A curated collection of high-quality wallpapers.",
        "",
        "---",
        "",
        "## 📑 Table of Contents / Shortcuts",
        "",
        "Quick navigation to any wallpaper:",
        "",
        "| # | Preview Link / Name | File |",
        "|---|----------------------|------|",
    ]

    for idx, item in enumerate(entries, start=1):
        lines.append(
            f"| {idx} | [{item['display_name']}]({item['anchor']}) | [`{item['filename']}`](./{item['encoded_file']}) |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 🖼️ Gallery & Wallpapers",
        "",
    ])

    gallery_blocks = []
    for item in entries:
        block = (
            f"### {item['display_name']}\n"
            f"[Back to top ↑](#-table-of-contents--shortcuts) • [Direct Link](./{item['encoded_file']})\n"
            f"<br/>\n"
            f'<a href="./{item['encoded_file']}"><img src="./{item['encoded_file']}" alt="{item['display_name']}" width="800"/></a>'
        )
        gallery_blocks.append(block)

    lines.append("\n\n---\n\n".join(gallery_blocks))
    lines.append("")

    readme_path = REPO_DIR / "README.md"
    readme_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Updated README.md with {len(entries)} wallpapers.")

if __name__ == "__main__":
    generate_readme()
