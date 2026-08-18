---
title: "MarkFlow: A Lightweight Markdown Editor Built With Tauri"
date: 2026-08-16T00:00:00ZT00:00:00Z
draft: false
description: "The world does not need another markdown editor. But it might need a better one — one that starts fast, gets out of your way, and doesn't ship a 200MB Electron binary just to render some text."
author: John Awotwi
category: Blogging
tags: []
keywords: []
excerpt: "The world does not need another markdown editor. But it might need a better one — one that starts fast, gets out of your way, and doesn't ship a 200MB"
---

# MarkFlow: A Lightweight Markdown Editor Built With Tauri

## Why another markdown editor?

The world doesn't need another markdown editor. But it might need a better one — one that starts fast, gets out of your way, and doesn't ship a 200MB Electron binary just to render some text.

That's why I built **MarkFlow**.

## What is MarkFlow?

MarkFlow is a minimal, cross-platform markdown editor built with Tauri. It renders GitHub Flavored Markdown (GFM), supports dark and light themes, and exports to PDF and Word — all from a binary under 5MB.

It runs on Linux, macOS, and Windows. No Electron. No Chromium. Just a native webview and a Rust backend.

### Features at a glance

- **GitHub Flavored Markdown** — tables, task lists, code blocks, strikethrough
- **Dark & light mode** — toggle with one click, respects system preference
- **PDF export** — styled, A4-formatted, ready to print
- **Word export** — proper .docx with headings, lists, and code blocks
- **Autosave** — saves every 5 seconds to localStorage, recovers on restart
- **File associations** — right-click any `.md` file → Open with MarkFlow
- **Keyboard-first** — `E` to edit, `Escape` to preview, `Ctrl+O` to open

## The tech stack

MarkFlow uses a deliberately simple stack:

| Layer | Technology |
|-------|-----------|
| Backend | Rust (Tauri 2) |
| Frontend | Vanilla JS, HTML, CSS |
| Markdown | marked.js (GFM) |
| PDF | html2pdf.js (jsPDF + html2canvas) |
| Word | docx.js |
| Build | Cargo + GitHub Actions |

No React. No Vue. No build toolchain. Just files you can read in five minutes.

## Why Tauri?

I evaluated three options:

1. **Electron** — battle-tested, but ships a full Chromium instance. Your "lightweight" editor ships at 150MB+.
2. **Flutter** — great for mobile, but web rendering adds complexity for a simple desktop app.
3. **Tauri** — uses the system's native webview (WebKit on macOS, WebView2 on Windows, WebKitGTK on Linux). The binary is under 5MB. The Rust backend handles file I/O, window management, and system integration.

Tauri won because it matches the project's philosophy: do the minimum, do it well, and ship small.

## Building the release pipeline

Cross-platform builds aren't free. Here's how I set it up:

**GitHub Actions** triggers on every `v*` tag push. Three parallel jobs build for:
- **Linux** — `.deb` package, portable `.tar.gz`, and an Arch PKGBUILD
- **macOS** — `.dmg` installer (Apple Silicon)
- **Windows** — NSIS `.exe` installer and `.msi` package

Each job runs on a fresh runner, installs Rust, and builds the Tauri release. Artifacts are uploaded automatically to a GitHub release.

The `.deb` package includes a `.desktop` file with MIME type registration, so MarkFlow shows up in your file manager's "Open with" menu.

## The autosave problem

Every editor needs autosave, but most implementations are either too aggressive (saving on every keystroke) or too fragile (writing to disk and failing silently).

MarkFlow's approach:
- **Debounced saves** — waits 5 seconds after the last edit before saving
- **localStorage only** — no disk writes until you explicitly save
- **Session recovery** — on restart, checks if saved content differs from the editor. If so, asks "Restore previous session?"
- **Visual feedback** — status bar shows "Saved 14:32:07" when autosave fires

This means you never lose work, even if the app crashes or you accidentally close the window.

## Design decisions

A few things that might surprise you:

**No markdown preview toggle button in the toolbar** — the keyboard shortcut (`E` / `Escape`) is faster and more reliable than a button click. The toolbar has buttons for file operations, not mode switching.

**No file tree sidebar** — MarkFlow opens one file at a time. If you need a file tree, use VS Code.

**No plugin system** — plugins add complexity. MarkFlow does markdown editing. That's it.

**CSS custom properties for theming** — every color in the app is a CSS variable. Dark mode isn't a separate stylesheet; it's just different values for the same variables.

## The logo

The MarkFlow logo combines a hashtag (`#` — the universal markdown symbol) with a flow arrow. It's simple, recognizable at 16x16, and works in both dark and light themes. The teal/turquoise color palette gives it a distinctive identity without being loud.

## Getting started

**Linux:**
```bash
sudo dpkg -i markflow_0.4.0_amd64.deb
markflow
```

**macOS:**
Download the `.dmg`, drag MarkFlow to Applications.

**Windows:**
Download the `.exe` installer, run it.

**From source:**
```bash
git clone https://github.com/TopHermDev/markdown-editor
cd markdown-editor/src-tauri
cargo tauri build
```

## What's next?

MarkFlow is intentionally minimal. Future considerations:
- Table of contents navigation for long documents
- Find and replace (Ctrl+F)
- Custom CSS themes
- Vim keybindings (maybe)

But for now, it does what it says on the tin: edit markdown, preview it, export it. Fast.

---

**Download MarkFlow v0.4.0:** [GitHub Releases](https://github.com/TopHermDev/markdown-editor/releases/tag/v0.4.0)

**Source code:** [github.com/TopHermDev/markdown-editor](https://github.com/TopHermDev/markdown-editor)

**License:** MIT
