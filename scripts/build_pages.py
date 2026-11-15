#!/usr/bin/env python3
"""Build the homepage in every language.

Strings live in i18n/<lang>.json (en.json is the source; every language has the
same keys) and the markup in i18n/template.html. Writes index.html for English,
<lang>/index.html for the rest, and sitemap.xml with hreflang alternates.

    python3 scripts/build_pages.py
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://alexriakhin.com"

# code: (native name, og:locale, text direction)
LANGUAGES = {
    "en": ("English", "en_US", "ltr"),
    "ar": ("العربية", "ar_AR", "rtl"),
    "de": ("Deutsch", "de_DE", "ltr"),
    "es": ("Español", "es_ES", "ltr"),
    "fr": ("Français", "fr_FR", "ltr"),
    "hr": ("Hrvatski", "hr_HR", "ltr"),
    "ja": ("日本語", "ja_JP", "ltr"),
    "ko": ("한국어", "ko_KR", "ltr"),
    "pt-BR": ("Português (Brasil)", "pt_BR", "ltr"),
    "ru": ("Русский", "ru_RU", "ltr"),
    "uk": ("Українська", "uk_UA", "ltr"),
}

GLOBE = (
    '<svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">'
    '<circle cx="12" cy="12" r="9.5" fill="none" stroke="currentColor" stroke-width="1.8"/>'
    '<path d="M2.5 12h19M12 2.5c2.6 2.8 3.9 6 3.9 9.5s-1.3 6.7-3.9 9.5c-2.6-2.8-3.9-6-3.9-9.5s1.3-6.7 3.9-9.5z" '
    'fill="none" stroke="currentColor" stroke-width="1.8"/></svg>'
)


def path_for(lang):
    return "/" if lang == "en" else f"/{lang.lower()}/"


def lang_menu(current, label):
    items = []
    for code, (name, _, _) in LANGUAGES.items():
        current_attr = ' aria-current="page"' if code == current else ""
        items.append(
            f'                    <li><a href="{path_for(code)}" hreflang="{code}" lang="{code}"{current_attr}>{name}</a></li>'
        )
    name = LANGUAGES[current][0]
    return (
        '            <details class="lang">\n'
        f'                <summary aria-label="{html.escape(label)}">{GLOBE}'
        f'<span class="lang-name">{name}</span><span class="lang-code">{current.split("-")[0].upper()}</span></summary>\n'
        '                <ul>\n' + "\n".join(items) + "\n                </ul>\n"
        "            </details>"
    )


def hreflang_links():
    links = [f'    <link rel="alternate" hreflang="{c}" href="{SITE}{path_for(c)}">' for c in LANGUAGES]
    links.append(f'    <link rel="alternate" hreflang="x-default" href="{SITE}/">')
    return "\n".join(links)


def main():
    template = (ROOT / "i18n/template.html").read_text()
    source = json.loads((ROOT / "i18n/en.json").read_text())
    problems = []

    for code, (_, og_locale, direction) in LANGUAGES.items():
        strings = json.loads((ROOT / f"i18n/{code}.json").read_text())
        missing = source.keys() - strings.keys()
        extra = strings.keys() - source.keys()
        if missing or extra:
            problems.append(f"{code}: missing {sorted(missing)} extra {sorted(extra)}")
            continue
        values = dict(strings)
        values.update(
            lang=code,
            dir=direction,
            og_locale=og_locale,
            page_url=SITE + path_for(code),
            hreflang_links=hreflang_links(),
            lang_menu=lang_menu(code, strings["lang_label"]),
            meta_title_json=json.dumps(strings["meta_title"], ensure_ascii=False)[1:-1],
        )
        page = re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], template)
        out = ROOT / ("index.html" if code == "en" else f"{code.lower()}/index.html")
        out.parent.mkdir(exist_ok=True)
        out.write_text(page)

    if problems:
        sys.exit("\n".join(problems))

    urls = []
    for code in LANGUAGES:
        alternates = "\n".join(
            f'    <xhtml:link rel="alternate" hreflang="{c}" href="{SITE}{path_for(c)}"/>' for c in LANGUAGES
        )
        urls.append(f"  <url>\n    <loc>{SITE}{path_for(code)}</loc>\n{alternates}\n  </url>")
    urls.append(f"  <url>\n    <loc>{SITE}/resume.html</loc>\n  </url>")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    print(f"Built {len(LANGUAGES)} languages")


if __name__ == "__main__":
    main()
