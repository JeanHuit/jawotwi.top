# Project Structure

This document provides a comprehensive overview of the project structure and where to find key files and directories.

## Overview

This is a personal portfolio and blog website built with **[Astro](https://astro.build/)** — a modern static site generator. The site showcases professional services, projects, blog posts (musings), and community programs.

**Site URL:** https://jawotwi.top

---

## Directory Tree

```
jawotwi.top/
├── public/                          # Static assets (served as-is)
│   ├── favicon.svg                  # Site favicon
│   ├── me.jpg                       # Profile image
│   ├── moi.png                      # Profile image (alternate)
│   ├── 5.webp                       # Hero/background image
│   └── robots.txt                   # SEO robots directives
│
├── src/
│   ├── components/                  # Reusable UI components
│   │   ├── Analytics.astro          # Analytics/tracking integration
│   │   ├── Card.astro               # Standard card component
│   │   ├── ExpandableCard.astro     # Collapsible/expandable card
│   │   ├── FlippingCard.astro       # Card with flip animation
│   │   ├── GitHubStats.astro        # GitHub statistics display
│   │   ├── GradientCard.astro       # Card with gradient styling
│   │   ├── Icon.astro               # Icon wrapper component
│   │   ├── MinimalCard.astro        # Minimal-styled card
│   │   ├── Pagination.astro         # Pagination navigation
│   │   ├── Search.astro             # Search functionality
│   │   ├── SectionNav.astro         # Section navigation
│   │   ├── SEO.astro                # SEO meta tags component
│   │   ├── ServicesSection.astro    # Services display section
│   │   ├── Skills.astro             # Skills showcase
│   │   ├── SkipLink.astro           # Accessibility skip link
│   │   └── SocialLinks.astro        # Social media links
│   │
│   ├── content/                     # Content collections (Markdown-based)
│   │   ├── musings/                 # Blog posts (47 articles)
│   │   ├── projects/                # Project showcases (3 projects)
│   │   ├── services/                # Service offerings (4 services)
│   │   ├── programs/                # Community programs/events (3 programs)
│   │   └── config.ts                # Content schema definitions (Zod)
│   │
│   ├── layouts/                     # Page layout templates
│   │   ├── BaseLayout.astro         # Root layout (HTML shell, head, nav)
│   │   └── BlogPostLayout.astro     # Layout for blog/musing posts
│   │
│   ├── pages/                       # File-based routing
│   │   ├── index.astro              # Homepage
│   │   ├── 404.astro                # Custom 404 error page
│   │   ├── rss.xml.js               # RSS feed generator
│   │   ├── categories/
│   │   │   └── [slug].astro         # Dynamic category pages
│   │   ├── tags/
│   │   │   └── [slug].astro         # Dynamic tag pages
│   │   └── musings/
│   │       └── [slug].astro         # Dynamic blog post pages
│   │
│   └── styles/                      # Global stylesheets
│       └── global.css               # Global CSS styles
│
├── .astro/                          # Astro cache (auto-generated)
├── .vscode/                         # VS Code settings
├── .qwen/                           # Qwen Code settings
│
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── .prettierignore                  # Prettier ignore rules
├── astro.config.mjs                 # Astro configuration
├── eslint.config.mjs                # ESLint configuration
├── prettier.config.mjs              # Prettier configuration
├── package.json                     # Dependencies and scripts
├── package-lock.json                # Dependency lock file
├── tsconfig.json                    # TypeScript configuration
└── README.md                        # Project readme
```

---

## Key Locations

### Content Management

| Content Type | Location | Purpose |
|---|---|---|
| **Blog Posts** | `src/content/musings/` | All blog articles in Markdown format |
| **Projects** | `src/content/projects/` | Project portfolio items |
| **Services** | `src/content/services/` | Professional service offerings |
| **Programs** | `src/content/programs/` | Community programs, events, initiatives |

Content schemas are defined in `src/content/config.ts` using Zod validation.

### Pages & Routing

| Route | File | Purpose |
|---|---|---|
| `/` | `src/pages/index.astro` | Homepage |
| `/musings/:slug` | `src/pages/musings/[slug].astro` | Individual blog posts |
| `/categories/:slug` | `src/pages/categories/[slug].astro` | Posts by category |
| `/tags/:slug` | `src/pages/tags/[slug].astro` | Posts by tag |
| `/rss.xml` | `src/pages/rss.xml.js` | RSS feed |
| `404` | `src/pages/404.astro` | Not found page |

### Components

All reusable UI components live in `src/components/`. Key components include:

- **SEO.astro** — Handles meta tags, Open Graph, and structured data
- **Analytics.astro** — Analytics/tracking integration
- **Card variants** — Multiple card styles (Card, MinimalCard, GradientCard, FlippingCard, ExpandableCard)
- **Search.astro** — Site search functionality
- **Pagination.astro** — Pagination for lists
- **Skills.astro** — Skills display section
- **ServicesSection.astro** — Services showcase

### Layouts

- **BaseLayout.astro** — The root layout wrapper; contains the HTML shell, navigation, and footer
- **BlogPostLayout.astro** — Layout specifically for blog/musing posts

### Static Assets

Files in `public/` are served directly at the root URL:

- **Images:** `me.jpg`, `moi.png`, `5.webp`
- **Favicon:** `favicon.svg`
- **SEO:** `robots.txt`

---

## Configuration Files

| File | Purpose |
|---|---|
| `astro.config.mjs` | Astro settings, integrations (sitemap), site URL |
| `tsconfig.json` | TypeScript compiler options |
| `eslint.config.mjs` | ESLint linting rules |
| `prettier.config.mjs` | Prettier formatting rules |
| `.env.example` | Template for environment variables |

---

## Available Scripts

Run these from the project root:

| Command | Description |
|---|---|
| `npm run dev` | Start local dev server at `localhost:4321` |
| `npm run build` | Build production site to `./dist/` |
| `npm run preview` | Preview production build locally |
| `npm run astro` | Run Astro CLI commands |
| `npm run lint` | Run ESLint |
| `npm run lint:fix` | Run ESLint with auto-fix |
| `npm run format` | Format code with Prettier |
| `npm run format:check` | Check formatting with Prettier |
| `npm run typecheck` | Run TypeScript type checking |

---

## Tech Stack

- **Framework:** Astro 5.x
- **UI Components:** Preact (via `@astrojs/preact`)
- **Styling:** Global CSS
- **Content:** Markdown with Astro Content Collections
- **SEO:** Sitemap integration (`@astrojs/sitemap`), RSS feed
- **Linting:** ESLint
- **Formatting:** Prettier
- **Language:** TypeScript
