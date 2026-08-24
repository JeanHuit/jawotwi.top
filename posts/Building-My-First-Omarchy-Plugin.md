---
title: Building My First Omarchy Plugin
date: 2026-08-23T00:00:00ZT00:00:00Z
draft: false
description: "I work across several machines, and I use Syncthing to keep a folder of stuff identical on all of them. Inside that folder lives my Obsidian vault — a pile of markdown files that I already think of as"
author: John Awotwi
category: Blogging
tags: []
keywords: []
excerpt: "I work across several machines, and I use Syncthing to keep a folder of stuff identical on all of them. Inside that folder lives my Obsidian vault — a"
---

# Building My First Omarchy Plugin

## The problem: todos, everywhere, always

I work across several machines, and I use [Syncthing](https://syncthing.net/) to keep a folder of stuff identical on all of them. Inside that folder lives my Obsidian vault — a pile of markdown files that I already think of as my second brain.

What I didn't have was a way to *see* my todos at a glance. They lived in markdown, which is great for writing but terrible for noticing. I wanted the open count sitting in my top bar, a click away from the full list, and the ability to check things off without opening Obsidian.

That's how I ended up building my first Omarchy plugin.

## The idea: no server, no API, no account

Most todo apps solve the "sync across machines" problem by running a server and asking you to log in. I already had Syncthing doing the sync. So the plugin didn't need to be an app — it just needed to be a *view* over a folder.

The whole architecture is:

```
Obsidian vault (synced by Syncthing)
  └── Todos/
        ├── inbox.md     # - [ ] Buy milk
        └── project.md

Omarchy shell ──watches──> reads .md ──> bar shows open count
                  toggle checkbox ──> writes back ──> syncs everywhere
```

Each machine reads its own local copy. Check a task off on the laptop, Syncthing pushes it to the desktop, and the desktop's bar updates within seconds. No server to maintain, no sync protocol to debug.

## Learning how an Omarchy plugin is put together

Omarchy's shell is a long-running [Quickshell](https://quickshell.org/) process, and a plugin is just a folder with a `manifest.json` and some QML. The manifest declares what the plugin *is* and how to load it:

```json
{
  "schemaVersion": 1,
  "id": "jeanhuit.todos",
  "name": "Synced Todos",
  "version": "1.0.0",
  "kinds": ["bar-widget"],
  "entryPoints": { "barWidget": "Panel.qml" }
}
```

The `bar-widget` kind is what puts it in the status bar. The manifest also carries a `schema`, which is what drives the built-in settings panel — so `vaultPath`, `todosDir`, and a couple of other options become editable fields with no extra UI work on my part.

The rest of the plugin is two files:

- **`Model.js`** — pure-JS parsing of [Obsidian Tasks](https://publish.obsidian.md/tasks/) syntax (`- [ ]`, `- [x]`, `📅 due dates`). I kept it Qt-free so it's unit-testable under plain `node`.
- **`Panel.qml`** — the bar button and the popup, built entirely from Omarchy's own `qs.Ui` component kit.

## Watching files with FileView

The interesting part was reacting to changes. Quickshell's `FileView` type reads a file *and* can watch it, firing a signal when it changes. That single type did most of the heavy lifting:

- one `FileView` watches the `Todos/` directory and re-scans when anything appears or disappears
- one `FileView` per markdown file parses its tasks on load and reload

When Syncthing writes a new version of `inbox.md`, the watcher fires, the file is re-read, and the count updates. I didn't write any polling — the shell just tells me when things change.

## Writing back is where it got tricky

Checking a task off means rewriting a line in a markdown file — flipping `- [ ]` to `- [x]`. That part is easy. The tricky part was making the popup reflect the change immediately rather than waiting for the file-watcher round-trip.

I landed on an optimistic update: write the file, then update the in-memory model straight away. The watcher re-syncs a moment later as a safety net.

The other gotcha took a while to pin down: after hot-reloading a bar widget during development, its IPC handler sometimes doesn't re-register cleanly. The symptom was confusing — methods worked, then didn't, or returned stale counts. The fix is embarrassingly simple: `omarchy restart shell`. Development reloads are fine for the UI, but a clean restart is what makes the command-line interface line up again.

## Quick-add from anywhere

Because the plugin is file-backed, "adding a task" is just appending a line. That means my agents — and a keyboard shortcut — can drop tasks in without touching the popup:

```bash
omarchy-shell jeanhuit.todos add "Buy milk 📅 2026-08-30"
```

And because agents can write plain markdown straight into the vault, anything that can write a file becomes a todo source for free.

## Theming came for free

I was worried about matching Omarchy's look — the rounded corners, the accent colors, the pill shapes. It turned out to be a non-issue. Every color, font, and border in the plugin resolves through Omarchy's theme singletons, so the widget restyles itself the moment I switch themes. I never hardcoded a single color.

## What you need to run it

- **Omarchy** (it runs inside `omarchy-shell`)
- **An Obsidian vault** (or any folder of markdown)
- **Syncthing** (or Dropbox, rsync — anything that syncs a folder)

No other runtime dependencies — just `find`, `bash`, and a couple of coreutils.

## Try it

```bash
omarchy plugin add https://github.com/TopHermDev/omarchy-todos.git --enable
```

The code is public at [github.com/TopHermDev/omarchy-todos](https://github.com/TopHermDev/omarchy-todos), with a README covering configuration and the full IPC reference. I've also submitted it to the community plugin marketplace at omarchyplugins.com.

---

Building it taught me the nice thing about Omarchy's model: a plugin doesn't have to be an application. Sometimes it's just a window onto files you already have — and Syncthing does the hard part for you.
