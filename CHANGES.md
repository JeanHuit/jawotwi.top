# Redesign: "engineering drawing sheet"

Branch: `redesign/engineering-drawing` (from `v5`).

## Build pipeline (unchanged)

- `netlify.toml` still runs `pip install -r requirements.txt && python build.py`. `requirements.txt` is unchanged (pyyaml only). The code does not need pandoc (the old fallback path still works).
- `build.py` remains the only generator of `musings.html` and `musings/*.html`.
- Added to `build.py` (all run at build time, so they never go stale):
  - Revision preview on the homepage: the 5 newest posts, filled between `<!-- revisions:start/end -->` in `index.html`.
  - Sheet stamp `REV YYYY-MM` and copyright `© YYYY` in `index.html`, `resume.html`, `musings.html` and posts, from the build date.
  - `_redirects`, one 301 per post from `/musings/<slug>.html.html` to `/musings/<slug>`.
- Everything else (home, resume, CSS) is hand-written static HTML.

## Files changed (per commit)

1. `css/style.css`: rewritten. Tokens, sheet frame, components, dark-mode inversion, responsive rules.
2. `index.html`, `build.py`: homepage layout; generated revision preview; build-time stamps.
3. `musings.html`, `build.py`: index with year groups, tag filters, search. Filters and rows are generated from the posts.
4. `musings/_template.html`, `build.py`, `musings/*.html`: post template; generated REV, PREVIOUS/NEXT REV, contents, numbered figure captions, wrapped tables.
5. `resume.html`: Experience, Skills and Education as tables.
6. `_redirects` (new), `og.png` (new, 1200x630), `index.html` (og:image tags).
7. `screenshots/` (new): 24 PNGs at 1440, 1024 and 390, light and dark, for home, musings, one post, and resume. Netlify publishes the whole repo root, so these are publicly reachable at `/screenshots/`. Delete the folder before merging if you do not want that.

## Redirects and the `.html.html` issue

- The generator never produced `.html.html`. I checked the current output, the git history (`git log -S`) and `dist/`.
- The live homepage does link to five `musings/<slug>.html.html` URLs. They return 301 to the clean URL. Those five posts are not in any git ref of this repo, so the live site is not built from this branch (see open questions).
- Fix: `build.py` now writes `_redirects` so old `.html.html` URLs 301 to clean URLs for every post in `posts/`.

## Content changes (intentional, from the spec)

- Hero copy "Systems engineer, builder, tinkerer." and the bio paragraph are replaced by the five General Notes items. The "Read the blog" and "View my work" buttons are removed.
- Services section is now PARTS LIST with the shortened descriptions from the spec. Old descriptions were longer (e.g. "Linux server administration, compute environments, Proxmox virtualisation, and secure production deployments.").
- Homepage "Archived" block is now the single SUPERSEDED line. Its three descriptions are dropped from the homepage, but the full text is still on `/resume` under "Projects archived". None of the three had links before, so none are added.
- Musings index intro is the spec sentence. The old "Been writing since 2010." is dropped.
- Post meta no longer shows the author line "Jean Huit" (the spec's meta line is `REV · date · tags`).
- The old "Copy link", Twitter and LinkedIn share links are kept.
- Resume: all existing text is kept word for word. "Download PDF" is not used because no PDF exists; the existing `window.print()` link is kept and labelled "Save as PDF ↓".
- Dimensions numbers are kept as hardcoded in the HTML (8+, 6+, 40+, 24), as before. The site does not compute them.

## Placeholders (visible on purpose)

- `[PLACEHOLDER: project link]` in each Detail cell. The old project cards had no links. Each cell links to its own anchor (`#detail-a/b/c`) until you give me URLs.
- `[PLACEHOLDER: stack not listed in source]` on the IT Officer row of the resume experience table.
- `[PLACEHOLDER: no certifications listed in the current resume]` on the resume.
- `[PLACEHOLDER: photo]` appears only if `moi.png` fails to load.

## Content problems in the source (not changed)

- `posts/AI-in-Early-Childhood-Education.md`: the front-matter `description` is truncated mid-sentence ("...From sm").
- Seven posts have a body `# ` heading, which would give those pages a second H1. Body H1s are demoted to H2. In "AI in Early Childhood Education" the body H2 is a different title from the front matter, so it stays in the contents list.
- `musings/Auditing-your-phone`: an image with no caption. The caption falls back to the alt text ("FIG. 1 — Graph from App Annie").
- Tags from `tags` and `categories` are now de-duplicated (one post had `ai` twice).

## Deviations from the spec

- Mockup: `https://claude.ai/artifact/...` returns only an artifact shell; the design renders in a sandboxed iframe I cannot read. Built from the spec alone.
- Hover hatch: the spec's `--hatch` note says "photo placeholder or loading state only", but the Interaction section asks for a faint hatch on detail-cell hover. I followed the Interaction section.
- Prose links (inside post bodies) are underlined. Without it, body links are indistinguishable from text (WCAG 1.4.1). Everywhere else links follow the no-underline rule.
- Page titles use `<h1>` on index, resume and musings (`REVISION HISTORY`, `JOHN AWOTWI` on resume) at 64px, because each page needs exactly one H1.
- Parts list uses a horizontally scrolling table (within its own container) on phones, not stacked blocks. It is the simpler option that keeps table semantics.
- Post H1 is not clamped to 3 lines. Long titles wrap naturally, so a very long title can exceed three lines.
- Post contents list: the spec says H2s. Most posts only use H3 for sections, so the list includes H2 and H3 (H3 indented), and skips any heading equal to the post title.
- Photo uses `src="moi.png"` (relative). The old `https://jawotwi.top/moi.png` resolves to the same file.
- Certification/education/skills tables: no content added.
- Theme colour: light is `#F1F2EE` (as requested). Dark is `#14161A`, the dark paper token, rather than `#F1F2EE` in dark mode.

## Contrast (computed)

| Pair | Ratio | Result |
|---|---|---|
| `--red-text` #C7311D on `--paper` #F1F2EE | 4.81:1 | AA pass (body and small text) |
| `--red-text` on `--desk` #DADCD6 | 3.91:1 | Fails AA for text under 24px. Not used on the desk. |
| `--red` #E4402B on `--paper` | 3.69:1 | Only for lines, dots and large fills. Not used for body text. |
| `--ink` on `--paper` | 16.1:1 | Pass |
| Dark `--red-text` #FF8A78 on `--paper` #14161A | 7.9:1 | Pass |

## Verification

- Build: `python3 build.py` is idempotent (second run produces no diff).
- Internal links: every relative `href` in `index.html`, `resume.html`, `musings.html` and `musings/*.html` resolves to an existing file.
- External URLs: unchanged. Only the Google Fonts links are added. Mailto, social and resume links are identical to the old pages.
- Overflow: at 390, 1024 and 1440 every page has `scrollWidth == clientWidth` (no horizontal page scroll).
- Name fit at 1440: one line, 1196px wide inside the 1280px column.
- Screenshots: 24 PNGs in `screenshots/`. Scheme was checked with `matchMedia` for each render.
- Not verified: real-device testing, Safari/Firefox rendering, Lighthouse.

## Open questions

1. **Live site vs this branch.** The live homepage lists five posts (2026) with `.html.html` links: `building-my-first-omarchy-plugin`, `i-built-two-android-apps-from-my-phone-today-no-laptop-no-coding-desk`, `my-fire-tablet-wouldnt-stop-restarting-so-hermes-fixed-it-over-usb`, `gh-link-vs-visamastercard-what-happened-to-ghanas-homegrown-payment-card`, `from-welfare-contributions-to-sustainability-…`. None of them are in `posts/` or any git ref here, and the live `/musings/welcome.html` has a different title. Deploying this branch would remove them. Where do their sources live?
2. Project links for Detail A/B/C (or should the cells stay non-links?).
3. Stack for the IT Officer role, and any certifications.
4. Favicon: the repo has none. Do you want one added?
5. Should "Entries written" and "Repositories" be computed (post count from `posts/`, repo count from GitHub), or stay hardcoded?
6. `moi.png` is 620 KB and is displayed at 240x300. A 480x600 export would save most of the page weight.
7. Keep `screenshots/` in the repo, or move them out before merging?
8. Hover hatch: confirm the Interaction-section hatch is intended, since the token note restricts `--hatch`.
