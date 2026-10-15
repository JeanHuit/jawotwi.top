#!/usr/bin/env python3
"""Build script: converts markdown posts → HTML blog pages + updates musings listing."""

import os, re, yaml, subprocess
import html as html_lib
from urllib.parse import quote
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter

BASE = Path(__file__).parent
POSTS_DIR = BASE / "posts"
MUSINGS_DIR = BASE / "musings"

# ── Blog post HTML template ───────────────────────────────────────────────

TEMPLATE_FILE = BASE / "musings" / "_template.html"


# ── Front matter helpers ──────────────────────────────────────────────────

def parse_front_matter(text):
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1))
    except Exception:
        fm = {}
    body = text[m.end():]
    body = re.sub(r'<!--more-->', '', body)
    return fm or {}, body


_DATE_FORMATS = [
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d",
]


def parse_date(date_val):
    """Parse a front-matter date into a timezone-naive datetime, or None."""
    if not date_val:
        return None
    if isinstance(date_val, datetime):
        dt = date_val
    elif isinstance(date_val, (int, float)):
        dt = datetime.fromtimestamp(date_val)
    elif isinstance(date_val, str):
        s = date_val.strip()
        dt = None
        for fmt in _DATE_FORMATS:
            try:
                dt = datetime.strptime(s, fmt)
                break
            except ValueError:
                continue
        if dt is None:
            m = re.match(r"(\d{4}-\d{2}-\d{2})(?:[T ](\d{2}:\d{2}:\d{2}))?", s)
            if m:
                try:
                    dt = datetime.strptime(
                        m.group(0),
                        "%Y-%m-%dT%H:%M:%S" if m.group(2) else "%Y-%m-%d",
                    )
                except ValueError:
                    dt = None
        if dt is None:
            return None
    else:
        return None
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def fmt_date(date_val):
    if not date_val:
        return ""
    dt = parse_date(date_val)
    if dt is None:
        return str(date_val)
    return dt.strftime("%b %-d, %Y")


def fmt_date_short(date_val):
    d = fmt_date(date_val)
    if d and "," in d:
        parts = d.split(", ")
        return parts[0] + " " + parts[1] if len(parts) >= 2 else d
    return d


def extract_tags(fm):
    tags = []
    for key in ("tags", "tag", "categories", "category"):
        val = fm.get(key)
        if not val:
            continue
        if isinstance(val, list):
            tags.extend(val)
        elif isinstance(val, str):
            tags.append(val)
    cleaned = []
    for t in tags:
        t = t.strip().lower()
        if t:
            cleaned.append(t)
    return cleaned


def html_filename(fname):
    base = fname.replace(".md", "")
    mapping = {
        "dspace-III": "dspace-iii", "dspace-II": "dspace-ii",
        "After-a-format": "after-a-format",
        "An-outline-of-outline": "an-outline-of-outline",
        "Apps-Unbecoming": "apps-unbecoming",
        "Auditing-your-phone": "auditing-your-phone",
        "Building-for-the-World": "building-for-the-world",
        "Ghost-adventures-1": "ghost-adventures-1",
        "Ghost-adventures-2": "ghost-adventures-2",
        "Github-Codeship-Firebase-Hosting": "github-codeship-firebase-hosting",
        "I-just-want-to-say-linux-is": "i-just-want-to-say-linux-is",
        "Oh-I-cannot-believe-i-just-sent-that-mail": "oh-i-cannot-believe-i-just-sent-that-mail",
        "Open-Source-alts": "open-source-alts",
        "Open-Source-in-SSA-schools": "open-source-in-ssa-schools",
    }
    if base in mapping:
        return mapping[base] + ".html"
    return base.lower() + ".html"


def slug_from_filename(fname):
    return html_filename(fname).replace(".html", "")


# ── Convert markdown to HTML with pandoc ──────────────────────────────────

def md_to_html(text):
    try:
        result = subprocess.run(
            ["pandoc", "-f", "markdown+smart", "-t", "html", "--no-highlight"],
            input=text, capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    # Fallback: basic markdown conversion
    html = text.strip()
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.M)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.M)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.M)
    html = re.sub(r'```(\w*)\n(.*?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.M)
    paragraphs = []
    for block in html.split('\n\n'):
        block = block.strip()
        if not block:
            continue
        if not block.startswith('<'):
            block = f'<p>{block}</p>'
        paragraphs.append(block)
    return '\n'.join(paragraphs)


# ── Generate individual blog post ─────────────────────────────────────────

def _strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def _slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", html_lib.unescape(s).lower()).strip("-") or "section"


def decorate_body(body, title=""):
    """Demote body H1s, add heading ids, number figures, wrap tables.
    Returns (html, [(id, label, level)]) for the contents list. Headings that
    repeat the post title are kept in the body but left out of contents."""
    body = re.sub(r"<h1([^>]*)>(.*?)</h1>", r"<h2\1>\2</h2>", body, flags=re.S)
    used = set(re.findall(r'<h[23][^>]*\sid="([^"]+)"', body))
    headings = []
    norm_title = _slugify(title)

    def heading(m):
        level, attrs, inner = m.group(1), m.group(2), m.group(3)
        idm = re.search(r'\sid="([^"]+)"', attrs)
        if idm:
            hid = idm.group(1)
        else:
            base = _slugify(_strip_tags(inner))
            hid, n = base, 2
            while hid in used:
                hid, n = f"{base}-{n}", n + 1
            used.add(hid)
            attrs = f' id="{hid}"' + attrs
        label = html_lib.unescape(_strip_tags(inner)).strip()
        if _slugify(label) != norm_title:
            headings.append((hid, label, int(level)))
        return f"<h{level}{attrs}>{inner}</h{level}>"

    body = re.sub(r"<h([23])([^>]*)>(.*?)</h\1>", heading, body, flags=re.S)

    counter = [0]

    def fig(m):
        inner = m.group(1)
        counter[0] += 1
        cap = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", inner, re.S)
        alt = re.search(r'alt="([^"]*)"', inner)
        text = html_lib.unescape(_strip_tags(cap.group(1))).strip() if cap else (
            html_lib.unescape(alt.group(1)).strip() if alt else "")
        inner = re.sub(r"<figcaption.*?</figcaption>", "", inner, flags=re.S).strip()
        capt = (f"<figcaption>FIG. {counter[0]} — {html_lib.escape(text, quote=False)}</figcaption>"
                if text else "")
        return f"<figure>{inner}{capt}</figure>"

    body = re.sub(r"<figure[^>]*>(.*?)</figure>", fig, body, flags=re.S)
    body = re.sub(r"<table(.*?)</table>",
                  lambda m: f'<div class="table-wrap"><table{m.group(1)}</table></div>',
                  body, flags=re.S)
    return body, headings


def _pn_link(entry, label):
    if not entry:
        return "<span></span>"
    return (f'<a href="{entry["file"]}"><span class="pn__label">{label}</span>'
            f'<span class="pn__title">{html_lib.escape(entry["title"], quote=False)}</span></a>')


def generate_post(md_file, out_dir, entry, prev_entry, next_entry):
    """entry: this post's listing record (rev, iso, slug, file, tags, title).
    prev_entry is the older post, next_entry the newer one (or None)."""
    text = md_file.read_text()
    fm, body_text = parse_front_matter(text)

    title = fm.get("title", md_file.stem)
    description = fm.get("description", fm.get("excerpt", "")) or ""
    tags = entry["tags"]
    slug = entry["slug"]
    out_name = entry["file"]

    body_html, headings = decorate_body(md_to_html(body_text), title)

    tag_links = " · ".join(
        f'<a href="../musings.html?tag={quote(t)}">{html_lib.escape(t, quote=False)}</a>' for t in tags
    )
    desc_html = f'<p class="post-desc">{description}</p>' if description else ""

    if headings:
        items = "\n".join(
            f'            <li class="contents__item--{level}"><a href="#{hid}">'
            f'{html_lib.escape(label, quote=False)}</a></li>'
            for hid, label, level in headings
        )
        contents_block = (
            '      <nav class="contents" aria-labelledby="contents-label">\n'
            '        <p class="label" id="contents-label">Contents</p>\n'
            f'        <ol class="contents__list">\n{items}\n        </ol>\n'
            '      </nav>'
        )
    else:
        contents_block = ""

    url_title = title.replace(" ", "%20").replace("—", "%E2%80%94")

    tmpl = TEMPLATE_FILE.read_text()
    html = tmpl
    for old, new in [
        ("__TITLE__", title),
        ("__DESCRIPTION__", description.replace('"', "&quot;")),
        ("__SLUG__", slug),
        ("__REV__", str(entry["rev"])),
        ("__DATE__", entry["iso"]),
        ("__TAG_LINKS__", tag_links),
        ("__DESC_HTML__", desc_html),
        ("__CONTENTS_BLOCK__", contents_block),
        ("__PREV__", _pn_link(prev_entry, "PREVIOUS REV ←")),
        ("__NEXT__", _pn_link(next_entry, "NEXT REV →")),
        ("__URL_TITLE__", url_title),
        ("__BODY__", body_html),
    ]:
        html = html.replace(old, new)

    (out_dir / out_name).write_text(html)
    return out_name


# ── Regenerate musings listing ────────────────────────────────────────────

def build_listing_html(posts):
    """Year-grouped revision rows (posts are newest-first)."""
    years = {}
    for p in posts:
        years.setdefault(p["year"], []).append(p)

    year_order = sorted(years.keys(), reverse=True)
    if "older" in year_order:
        year_order.remove("older")
        year_order.append("older")

    lines = []
    for year in year_order:
        label = f"Year {year}" if year != "older" else "Older"
        lines.append(f'        <section class="yr-group" data-year="{year}" aria-labelledby="yr-{year}">')
        lines.append(f'          <h2 class="yr" id="yr-{year}">{label}</h2>')
        lines.append('          <ul class="revs">')
        for p in years[year]:
            lines.append(rev_row_html(p, indent="            ", with_tags_attr=True))
        lines.append('          </ul>')
        lines.append('        </section>')
    return "\n".join(lines)


def build_filters_html(all_tags):
    """Tag filter buttons: ALL first, then the 15 most used tags."""
    lines = ['        <li><button type="button" data-tag="all" aria-pressed="true">all</button></li>']
    for tag, _ in all_tags.most_common(15):
        lines.append(
            f'        <li><button type="button" data-tag="{html_lib.escape(tag, quote=True)}" '
            f'aria-pressed="false">{html_lib.escape(tag, quote=False)}</button></li>'
        )
    return "\n".join(lines)


def update_musings_listing(posts, all_tags):
    path = BASE / "musings.html"
    html = path.read_text()
    html = replace_between(html, "<!-- filters:start -->", "<!-- filters:end -->", build_filters_html(all_tags))
    html = replace_between(html, "<!-- posts:start -->", "<!-- posts:end -->", build_listing_html(posts))
    path.write_text(html)


# ── Shared helpers for the redesign ───────────────────────────────────────

ROOT_PAGES = ["index.html", "resume.html", "musings.html"]


def iso_date(sort_date):
    if sort_date == datetime.min:
        return "undated"
    return sort_date.strftime("%Y-%m-%d")


def assign_revs(posts):
    """posts are newest-first. REV counts down from the newest as REV <total>."""
    total = len(posts)
    for i, p in enumerate(posts):
        p["rev"] = total - i
        p["iso"] = iso_date(p["sort_date"])
    return posts


def rev_row_html(p, indent="  ", with_tags_attr=False):
    """One revision row: a single link with rev / date / title / tags columns."""
    tags_attr = f' data-tags="|{"|".join(p["tags"])}|"' if with_tags_attr else ""
    tags_text = " · ".join(p["tags"])
    pad = indent
    return (
        f'{pad}<li{tags_attr}>\n'
        f'{pad}  <a class="rev-row" href="musings/{p["file"]}">\n'
        f'{pad}    <span class="rev-row__rev">REV {p["rev"]}</span>\n'
        f'{pad}    <span class="rev-row__date">{p["iso"]}</span>\n'
        f'{pad}    <span class="rev-row__title">{html_lib.escape(p["title"], quote=False)}</span>\n'
        f'{pad}    <span class="rev-row__tags">{html_lib.escape(tags_text, quote=False)}</span>\n'
        f'{pad}  </a>\n'
        f'{pad}</li>'
    )


def replace_between(text, start, end, body):
    """Replace everything between two marker comments (markers are kept)."""
    i = text.find(start)
    j = text.find(end, i + len(start)) if i >= 0 else -1
    if i < 0 or j < 0:
        raise SystemExit(f"ERROR: markers {start!r} / {end!r} not found")
    return text[: i + len(start)] + "\n" + body + "\n" + text[j:]


def update_home(posts):
    """Fill the homepage revision preview with the 5 most recent posts."""
    path = BASE / "index.html"
    html = path.read_text()
    rows = "\n".join(rev_row_html(p) for p in posts[:5])
    html = replace_between(html, "<!-- revisions:start -->", "<!-- revisions:end -->", rows)
    path.write_text(html)
    print(f"  ✓ index.html revision preview (5 of {len(posts)})")


def stamp_pages():
    """Build-time values: sheet REV month and copyright year."""
    now = datetime.now()
    rev_stamp = f"REV {now:%Y-%m}"
    year_stamp = f"© {now:%Y}"
    targets = [BASE / name for name in ROOT_PAGES] + sorted(MUSINGS_DIR.glob("*.html"))
    for path in targets:
        if path.name.startswith("_"):
            continue
        html = path.read_text()
        new = re.sub(r"REV \d{4}-\d{2}", rev_stamp, html)
        new = re.sub(r"©\s*\d{4}", year_stamp, new)
        if new != html:
            path.write_text(new)


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    print("Building site...")

    os.makedirs(MUSINGS_DIR, exist_ok=True)

    # Parse all posts
    posts = []
    all_tags = Counter()

    md_files = sorted(POSTS_DIR.glob("*.md"))
    for md_file in md_files:
        text = md_file.read_text()
        fm, _ = parse_front_matter(text)
        fname = html_filename(md_file.name)
        title = fm.get("title", md_file.stem)
        date_val = fm.get("date", "")
        tags = extract_tags(fm)
        for t in tags:
            all_tags[t] += 1

        # Sort key
        sort_date = parse_date(date_val) or datetime.min
        if sort_date == datetime.min:
            print(f"  ⚠ warning: unparseable date '{date_val}' in {md_file.name}")

        year = str(sort_date.year) if sort_date != datetime.min else "older"
        display_date = fmt_date(date_val)
        short_date = fmt_date_short(date_val)

        posts.append({
            "file": fname,
            "title": title,
            "date": display_date,
            "short_date": short_date,
            "year": year,
            "sort_date": sort_date,
            "tags": tags,
            "slug": slug_from_filename(md_file.name),
            "md": md_file,
        })

    # Sort newest first
    posts.sort(key=lambda p: p["sort_date"], reverse=True)

    assign_revs(posts)
    update_home(posts)

    # Generate blog post HTML files (posts are newest-first: index+1 is older)
    for i, entry in enumerate(posts):
        prev_entry = posts[i + 1] if i + 1 < len(posts) else None
        next_entry = posts[i - 1] if i > 0 else None
        generate_post(entry["md"], MUSINGS_DIR, entry, prev_entry, next_entry)
        print(f"  ✓ musings/{entry['file']}")

    # Update musings.html listing
    update_musings_listing(posts, all_tags)
    stamp_pages()
    print(f"  ✓ musings.html listing updated ({len(posts)} posts)")

    print(f"\nDone. Generated {len(posts)} posts.")


if __name__ == "__main__":
    main()
