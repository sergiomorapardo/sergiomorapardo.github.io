#!/usr/bin/env python3
"""Validate the generated portfolio using only the Python standard library."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


SITE_HOST = "sergiomorapardo.github.io"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[str] = []
        self.images_without_alt = 0
        self.h1_count = 0
        self.lang = ""
        self.is_redirect = False
        self.noindex = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if values.get("id"):
            self.ids.append(values["id"])
        if tag in {"a", "link"} and values.get("href"):
            self.links.append(values["href"])
        if tag in {"img", "script", "source"} and values.get("src"):
            self.links.append(values["src"])
        if tag == "img" and "alt" not in values:
            self.images_without_alt += 1
        if tag == "h1":
            self.h1_count += 1
        if tag == "html":
            self.lang = values.get("lang", "")
        if tag == "meta":
            if values.get("http-equiv", "").lower() == "refresh":
                self.is_redirect = True
            if values.get("name", "").lower() == "robots" and "noindex" in values.get("content", "").lower():
                self.noindex = True


def target_file(root: Path, source: Path, raw_url: str) -> tuple[Path | None, str]:
    parsed = urlparse(raw_url)
    if parsed.scheme in {"mailto", "tel", "javascript", "data"}:
        return None, ""
    if parsed.scheme in {"http", "https"} and parsed.netloc != SITE_HOST:
        return None, ""
    if parsed.scheme and parsed.scheme not in {"http", "https"}:
        return None, ""

    path = unquote(parsed.path)
    if not path:
        return source, parsed.fragment
    candidate = root / path.lstrip("/") if path.startswith("/") else source.parent / path
    if path.endswith("/") or candidate.is_dir():
        candidate /= "index.html"
    return candidate.resolve(), parsed.fragment


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    pages: dict[Path, PageParser] = {}

    for page in sorted(root.rglob("*.html")):
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        pages[page.resolve()] = parser
        label = page.relative_to(root)

        if parser.noindex:
            errors.append(f"{label}: contains a noindex directive")
        if len(parser.ids) != len(set(parser.ids)):
            errors.append(f"{label}: contains duplicate element IDs")
        if not parser.is_redirect:
            if not parser.lang:
                errors.append(f"{label}: missing html[lang]")
            if parser.h1_count != 1:
                errors.append(f"{label}: expected one h1, found {parser.h1_count}")
            if parser.images_without_alt:
                errors.append(f"{label}: {parser.images_without_alt} image(s) missing alt")

    for page, parser in pages.items():
        for raw_url in parser.links:
            destination, fragment = target_file(root, page, raw_url)
            if destination is None:
                continue
            if not destination.exists():
                errors.append(f"{page.relative_to(root)}: missing target {raw_url}")
                continue
            if fragment and destination.suffix == ".html":
                target_parser = pages.get(destination)
                if target_parser and fragment not in target_parser.ids:
                    errors.append(f"{page.relative_to(root)}: missing fragment #{fragment} in {raw_url}")

    pdf = root / "cv" / "sergio-mora-cv.pdf"
    if not pdf.exists() or pdf.read_bytes()[:4] != b"%PDF":
        errors.append("cv/sergio-mora-cv.pdf: missing or invalid PDF")
    return errors


def main() -> int:
    cli = argparse.ArgumentParser()
    cli.add_argument("site", type=Path, help="Generated Hugo directory")
    args = cli.parse_args()
    root = args.site.resolve()
    if not root.is_dir():
        cli.error(f"not a directory: {root}")

    errors = validate(root)
    if errors:
        print("Site validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Site validation passed: {len(list(root.rglob('*.html')))} HTML pages checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

