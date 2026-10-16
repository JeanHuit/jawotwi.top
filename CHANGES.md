# Redesign: "engineering drawing sheet"

Branch: `redesign/engineering-drawing` (from `v5`).

## Build pipeline (unchanged)

- `netlify.toml` still runs `pip install -r requirements.txt && python build.py`. `requirements.txt` is unchanged (pyyaml only). No pandoc needed (fallback path still works).
- `build.py` is still the only generator of `musings.html` and `musings/*.html`. Posts come from `posts/*.md`, which your agent syncs from the vault.
- Added to `build.py`, all run at build time:
  - Homepage revision preview: the 5 newest posts (between `<!-- revisions:start/end -->`).
  - Homepage dimensions, computed (between `<!-- dims:start/end -->`):
    - Entries written = number of posts.
    - Repositories = `public_repos` from the GitHub profile API (`/users/JeanHuit`), the number GitHub shows on the profile. Falls back to 43 if the API is unreachable at build time.
    - Years in the field = current year minus 2015 (start of the earliest role on the resume).
    - Platforms deployed = `6+`, a constant (no data source).
  - Sheet stamp `REV YYYY-MM` and copyright `© YYYY` from the build date.
  - `_redirects`: one 301 per post from `/musings/<slug>.html.html` to `/musings/<slug>`.
  - Date parsing now accepts YAML `date` objects (unquoted `2026-10-02`), which previously were silently dropped.

## Files

- `css/style.css`: tokens, sheet frame, components, dark-mode inversion, responsive rules.
- `index.html`: homepage. `resume.html`: resume. `musings.html`: index. `musings/_template.html`: post template.
- `build.py`: listing, revision preview, stats, post generation, stamps, redirects.
- `posts/`: five posts restored from the vault (see below).
- `favicon.png` (64px, transparent) and `apple-touch-icon.png` (180px, paper background), monochrome, generated from the logo's alpha channel.
- `logo.png`: the original logo, committed unchanged.
- `moi.png`: resized to 480x600 (cover crop). Displayed at 240x300.
- `og.png` (1200x630) and the `og:image` tags on the homepage.
- `_redirects` (generated).

## Content

- **Restored from the vault.** Five posts were live on jawotwi.top but not in this repo. Copied from `~/Documents/HermesVault/Blog/` into `posts/` under slug-based filenames, so the live URLs are unchanged:
  - `building-my-first-omarchy-plugin`
  - `i-built-two-android-apps-from-my-phone-today-no-laptop-no-coding-desk`
  - `my-fire-tablet-wouldnt-stop-restarting-so-hermes-fixed-it-over-usb`
  - `gh-link-vs-visamastercard-what-happened-to-ghanas-homegrown-payment-card`
  - `from-welfare-contributions-to-sustainability-a-simple-model-for-predicting-the-future-of-sectorial-welfare-funds`
  - Three had `created:` instead of `date:`. A `date:` line was added with the same value. Nothing else changed.
- **Resume: experience from the CV (source of truth).** All five CV roles are listed, in CV order and wording: Senior Technical Officer (2025–present), Technical Officer (2019–2024), Web Developer | Systems Administrator | Technical Support (2015–2019), Developer / Researcher — GSTDP (2013–2014), Teaching Assistant (Sep 2013 – Jul 2014). Employer names and education dates/degrees match the CV. The homepage Resume strip also shows 2025 – present.
- **Stack column.** The CV lists no per-role stack, so all five rows use the Senior Technical Officer stack (PHP · Python · Linux · Proxmox · Docker · Git/CI-CD · MariaDB). It is accurate for the two CSIR-INSTI roles; for the MESTI/COTVET and National Service rows it is inherited, not verified.
- **AWS removed** from the experience stack, the homepage strip and the Cloud & Data skills row. The Profile paragraph, the Technical skills table and the Projects archived list are unchanged from the old resume.
- **Certifications.** The resume's Certifications table now lists the ten entries from your ATS CV (2004–2023). Nothing else on the resume was changed from the CV.
- **Resume download.** The CV is not linked or copied. The "Save as PDF ↓" link (print) is unchanged.
- **Email.** `mail@jawotwi.top` everywhere (mailto links and visible text).
- **Nav and headings.** "Revisions" is now "Musings" (nav on every page, homepage section, index heading, "All musings →"). "Parts list" is now "Services" (nav on every page, homepage heading). Anchor ids (`#parts`) and CSS class names are unchanged. The per-post `REV n` labels are unchanged.
- **Detail views.** The cells are no longer links, and the `[PLACEHOLDER: project link]` lines are gone. Hover hatch and title underline removed. The `--hatch` token is still defined.
- Earlier cuts still apply: hero copy and bio replaced by the General Notes; services use the shortened descriptions; the "Archived" block is now the SUPERSEDED line (full descriptions still on the resume under "Projects archived"); the post author line is removed from post meta.

## Placeholders still visible

- None. (The photo placeholder remains, shown only if `moi.png` fails to load.)
- Photo: `[PLACEHOLDER: photo]`, only if `moi.png` fails to load.

## Source issues (not changed)

- `posts/AI-in-Early-Childhood-Education.md`: front-matter `description` truncated ("…From sm").
- Seven posts use a body `#` heading; demoted to H2 so each page has one H1.
- One post's body H2 has a different title from its front matter, so it stays in the post's contents list.

## Deviations from the spec

- Mockup: the Claude artifact link returns only a shell; built from the spec.
- Prose links in post bodies are underlined (WCAG 1.4.1). Other links follow the no-underline rule.
- H1 on index, resume and musings is the page title at 64px, because each page needs one H1.
- Parts list table scrolls inside its container on phones instead of stacking.
- Post titles are not clamped to three lines; very long titles can wrap further.
- Post contents include H2 and H3 (H3 indented), skipping any heading equal to the post title.
- Photo uses `src="moi.png"` (relative). Same file as the old absolute URL.
- Theme colour: light `#F1F2EE`; dark `#14161A` (the dark paper token).
- Favicon and touch icon are monochrome (ink mark from the logo's alpha channel). `logo.png` is committed as-is in the repo root.

## Contrast

| Pair | Ratio | Result |
|---|---|---|
| `--red-text` #C7311D on `--paper` #F1F2EE | 4.81:1 | AA pass |
| `--red-text` on `--desk` #DADCD6 | 3.91:1 | Fails AA for text under 24px. Not used on the desk. |
| `--red` #E4402B on `--paper` | 3.69:1 | Lines, dots and large fills only |
| `--ink` on `--paper` | 16.1:1 | Pass |
| Dark `--red-text` #FF8A78 on `#14161A` | 7.9:1 | Pass |

## Verification

- `python3 build.py` is idempotent.
- Every internal `href`/`src` in the HTML resolves.
- Overflow: at 390, 1024 and 1440, `scrollWidth == clientWidth` on the pages checked (home re-checked after the latest changes).
- Name: one line at 1440 (1196px in the 1280px column).
- Photo centred in the stacked (≤1024px) layout.
- Not verified: real devices, Safari/Firefox, Lighthouse.

## Open questions

1. **Stack column.** All five rows share the Senior Technical Officer stack at your instruction. Correct for the two CSIR-INSTI roles; please confirm the MESTI/COTVET and National Service rows.
2. **Platforms deployed (6+).** Still a constant. No source to compute it from.
