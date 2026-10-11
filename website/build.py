#!/usr/bin/env python3
# Modified for the Odoo Workbench derivative, 2026.
"""Build the Odoo Workbench website and render repository Markdown docs.

    python3 website/build.py OUT [--version 0.1.0]

Set GITHUB_REPOSITORY=OWNER/REPOSITORY in CI so links and social metadata point
at the new repository. The APT signing key from upstream is deliberately not used.
"""

import argparse
import html
import os
import re
import shutil
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "").strip().strip("/")
if REPOSITORY.startswith("https://github.com/"):
    REPOSITORY = REPOSITORY.removeprefix("https://github.com/")
GITHUB = f"https://github.com/{REPOSITORY}" if REPOSITORY else ""
if REPOSITORY and "/" in REPOSITORY:
    OWNER, REPO_NAME = REPOSITORY.split("/", 1)
    PAGES_URL = f"https://{OWNER}.github.io/" + ("" if REPO_NAME == f"{OWNER}.github.io" else f"{REPO_NAME}/")
else:
    PAGES_URL = ""

# (source, output name, title in the docs navigation)
DOCS = [
    ("docs/install.md", "install", "Install and first run"),
    ("docs/troubleshooting.md", "troubleshooting", "Troubleshooting"),
    ("SECURITY.md", "security", "Security model"),
    ("CONTRIBUTING.md", "contributing", "Contributing"),
]
LINKS = {src.rsplit("/", 1)[-1]: f"{name}.html" for src, name, _ in DOCS}
LINKS["README.md"] = "../index.html"
CURRENT = ' aria-current="page"'


def rewrite_link(match: re.Match, src_dir: Path) -> str:
    target = match.group(2)
    if re.match(r"^[a-z]+:|^#", target):
        return match.group(0)
    path, _, anchor = target.partition("#")
    page = LINKS.get(path.rsplit("/", 1)[-1])
    if page:
        url = page + (f"#{anchor}" if anchor else "")
    elif GITHUB:
        rel = (src_dir / path).resolve().relative_to(REPO)
        url = f"{GITHUB}/blob/main/{rel.as_posix()}" + (f"#{anchor}" if anchor else "")
    else:
        # Local build: use the file's path if it was copied; otherwise avoid a dead external URL.
        name = path.rsplit("/", 1)[-1]
        url = (f"../{name}" if name in {"LICENSE", "NOTICE"} else "#") + (f"#{anchor}" if anchor else "")
    return f"{match.group(1)}({url})"


def render(src: Path) -> tuple[str, str]:
    md_text = re.sub(r"(\]\s?)\(([^)\s]+)\)", lambda m: rewrite_link(m, src.parent), src.read_text(encoding="utf-8"))
    first = md_text.splitlines()[0]
    title = first.lstrip("# ").strip() if first.startswith("# ") else ""
    body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "toc", "sane_lists"],
        extension_configs={"toc": {"permalink": "#", "permalink_class": "anchor"}},
        output_format="html",
    )
    return title, body


def page(template: str, **values: str) -> str:
    def fill(match: re.Match) -> str:
        if match.group(1) not in values:
            raise SystemExit(f"unfilled placeholder: {match.group(0)}")
        return values[match.group(1)]

    return re.sub(r"\{\{(\w+)\}\}", fill, template)


def build(out: Path, version: str) -> None:
    if out.exists():
        shutil.rmtree(out)
    (out / "docs").mkdir(parents=True)
    shutil.copytree(HERE / "assets", out / "assets")
    shutil.copy(HERE / "style.css", out / "style.css")
    shutil.copy(REPO / "LICENSE", out / "LICENSE")
    shutil.copy(REPO / "NOTICE", out / "NOTICE")
    (out / ".nojekyll").write_text("")

    site_url = PAGES_URL
    social_image = f"{PAGES_URL}assets/workbench-social-card.png" if PAGES_URL else "assets/workbench-social-card.png"
    repo_value = html.escape(REPOSITORY, quote=True)
    index = (HERE / "index.html").read_text(encoding="utf-8")
    (out / "index.html").write_text(
        page(index, version=html.escape(version), repository=repo_value,
             site_url=html.escape(site_url, quote=True), social_image=html.escape(social_image, quote=True)),
        encoding="utf-8",
    )

    layout = (HERE / "doc.html").read_text(encoding="utf-8")
    for src, name, nav_title in DOCS:
        title, body = render(REPO / src)
        nav = "\n".join(
            f'<a href="{n}.html"{CURRENT if n == name else ""}>{html.escape(t)}</a>'
            for _, n, t in DOCS
        )
        source = f"{GITHUB}/blob/main/{src}" if GITHUB else "#"
        (out / "docs" / f"{name}.html").write_text(
            page(layout, title=html.escape(title or nav_title), nav=nav, body=body,
                 source=html.escape(source, quote=True), version=html.escape(version), repository=repo_value),
            encoding="utf-8",
        )
    print(f"site in {out}: index.html, {len(DOCS)} docs, version {version}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("out", type=Path)
    parser.add_argument("--version", default="")
    args = parser.parse_args()
    version = args.version.lstrip("v") or re.search(
        r'"version": "([^"]+)"', (REPO / "app/src-tauri/tauri.conf.json").read_text(encoding="utf-8")
    ).group(1)
    build(args.out, version)


if __name__ == "__main__":
    main()
