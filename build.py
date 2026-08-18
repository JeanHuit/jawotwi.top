#!/usr/bin/env python3
"""Build script: converts markdown posts → HTML blog pages + updates musings listing."""

import os, re, yaml, subprocess
from datetime import datetime
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


def fmt_date(date_val):
    if not date_val:
        return ""
    if isinstance(date_val, datetime):
        dt = date_val
    elif isinstance(date_val, str):
        for fmt in [
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d",
        ]:
            try:
                dt = datetime.strptime(date_val, fmt)
                break
            except ValueError:
                continue
        else:
            return date_val
    elif isinstance(date_val, (int, float)):
        return datetime.fromtimestamp(date_val).strftime("%b %-d, %Y")
    else:
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

def generate_post(md_file, out_dir):
    text = md_file.read_text()
    fm, body_text = parse_front_matter(text)

    title = fm.get("title", md_file.stem)
    description = fm.get("description", fm.get("excerpt", ""))
    date_val = fm.get("date", "")
    tags = extract_tags(fm)
    slug = slug_from_filename(md_file.name)
    out_name = html_filename(md_file.name)

    display_date = fmt_date(date_val)
    url_title = title.replace(" ", "%20").replace("—", "%E2%80%94")

    tag_display = " · ".join(tags[:5]) if tags else ""
    tag_links = ""
    for tag in tags:
        tag_links += f'        <a href="../musings.html?tag={tag}" class="post-tag">{tag}</a>\n'

    desc_html = ""
    if description:
        desc_html = f'      <p class="post-header__desc" style="color:var(--ink-2);font-size:0.95rem;margin-bottom:var(--space-3);">{description}</p>'

    body_html = md_to_html(body_text)

    tmpl = TEMPLATE_FILE.read_text()
    html = tmpl
    for old, new in [
        ("__TITLE__", title),
        ("__DESCRIPTION__", description.replace('"', "&quot;")),
        ("__SLUG__", slug),
        ("__TAG_DISPLAY__", tag_display),
        ("__DATE__", display_date),
        ("__TAG_LINKS__", tag_links.rstrip()),
        ("__BODY__", body_html),
        ("__URL_TITLE__", url_title),
        ("__DESC_HTML__", desc_html),
    ]:
        html = html.replace(old, new)

    out_path = out_dir / out_name
    out_path.write_text(html)
    return out_name, title, display_date, tags, date_val


# ── Regenerate musings listing ────────────────────────────────────────────

def build_listing_html(posts):
    """Build the posts list HTML section (year groups + rows)."""
    years = {}
    for p in posts:
        y = p["year"]
        years.setdefault(y, []).append(p)

    year_order = sorted(years.keys(), reverse=True)
    if "older" in year_order:
        year_order.remove("older")
        year_order.append("older")

    lines = []
    for year in year_order:
        label = year if year != "older" else "Older"
        lines.append(f'      <!-- {year} -->')
        lines.append(f'      <div class="musings-year-group" data-year="{year}">')
        lines.append(f'        <div class="musings-year-label">{label}</div>')
        lines.append(f'        <ul class="musings-list">')

        for p in years[year]:
            tag_classes = " ".join(p["tags"])
            tag_buttons = ""
            for t in p["tags"]:
                tag_buttons += f'                    <span class="musing-tag">{t}</span>\n'

            lines.append(f'''          <li data-tags="{tag_classes}">
            <a href="musings/{p["file"]}" class="musing-row">
              <div>
                <div class="musing-row__title">{p["title"]}</div>
                <div class="musing-row__meta">
                  <span class="musing-row__date">{p["short_date"]}</span>
                  <span class="musing-row__tags">
                    {tag_buttons}                  </span>
                </div>
              </div>
              <span class="musing-row__date">→</span>
            </a>
          </li>''')

        lines.append('        </ul>')
        lines.append('      </div>')

    return '\n'.join(lines)


def build_filters_html(all_tags):
    """Build filter button HTML from tag frequency."""
    # Always include 'all' first
    lines = ['        <button class="filter-btn active" data-tag="all">all</button>']
    for tag, _ in all_tags.most_common(15):
        lines.append(f'        <button class="filter-btn" data-tag="{tag}">{tag}</button>')
    return '\n'.join(lines)


def update_musings_listing(posts, all_tags):
    musings_path = BASE / "musings.html"
    html = musings_path.read_text()

    # Replace the posts list section
    start_marker = '<div class="musings-index-list" id="posts-list">'
    end_marker = "</div><!-- /posts-list -->"

    start_idx = html.find(start_marker)
    end_idx = html.find(end_marker, start_idx)

    if start_idx < 0 or end_idx < 0:
        print("ERROR: Could not find posts-list markers in musings.html")
        return

    listing_html = build_listing_html(posts)
    empty_state = """      <!-- Empty state -->
      <div id="empty-state" style="display:none; text-align:center; padding: var(--space-12) 0;">
        <p style="font-family: var(--font-mono); font-size: 0.85rem; color: var(--ink-3);">
          no posts match that search.
        </p>
      </div>"""

    new_section = f"""    <div class="musings-index-list" id="posts-list">

{listing_html}

{empty_state}
    </div><!-- /posts-list -->"""

    html = html[:start_idx] + new_section + html[end_idx + len(end_marker):]

    # Replace filter buttons
    filter_start = '<div class="musings-filters" id="tag-filters" role="group" aria-label="Filter by tag">'
    filter_end = "</div>"

    fs = html.find(filter_start)
    fe = html.find(filter_end, fs)

    if fs >= 0 and fe >= 0:
        filters_html = build_filters_html(all_tags)
        new_filters = f"""      <div class="musings-filters" id="tag-filters" role="group" aria-label="Filter by tag">
{filters_html}
      </div>"""
        html = html[:fs] + new_filters + html[fe + len("</div>"):]

    musings_path.write_text(html)


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
        sort_date = datetime.min
        if isinstance(date_val, datetime):
            sort_date = date_val
        elif isinstance(date_val, str):
            for fmt in [
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d",
            ]:
                try:
                    sort_date = datetime.strptime(date_val, fmt)
                    break
                except ValueError:
                    continue

        year = str(sort_date.year) if sort_date and sort_date != datetime.min else "older"
        display_date = fmt_date(date_val)
        short_date = fmt_date_short(date_val)

        posts.append({
            "file": fname,
            "title": title,
            "date": display_date,
            "short_date": short_date,
            "year": year,
            "sort_date": sort_date,
            "tags": tags[:3],
        })

    # Sort newest first
    posts.sort(key=lambda p: p["sort_date"].replace(tzinfo=None), reverse=True)

    # Generate blog post HTML files
    for md_file in md_files:
        generate_post(md_file, MUSINGS_DIR)
        print(f"  ✓ musings/{html_filename(md_file.name)}")

    # Update musings.html listing
    update_musings_listing(posts, all_tags)
    print(f"  ✓ musings.html listing updated ({len(posts)} posts)")

    print(f"\nDone. Generated {len(posts)} posts.")


if __name__ == "__main__":
    main()
