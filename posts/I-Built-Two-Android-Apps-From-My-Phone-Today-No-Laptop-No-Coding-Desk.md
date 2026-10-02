---
title: "I Built Two Android Apps From My Phone Today — No Laptop, No Coding Desk"
date: 2026-10-02T00:00:00Z
draft: false
description: "Today I took two Android app projects from \"someone shared the code with me\" to \"here's the installable app file\" — and I did the whole thing from my phone, inside a Telegram chat with Hermes, my AI a"
author: John Awotwi
category: Blogging
tags: ["hermes-agent", "android", "automation", "github", "telegram", "mobile", "apps"]
keywords: ["hermes-agent", "android", "automation", "github", "telegram", "mobile", "apps"]
excerpt: Today I took two Android app projects from "someone shared the code with me" to "here's the installable app file" — and I did the whole thing from my
---

# I Built Two Android Apps From My Phone Today — No Laptop, No Coding Desk

## Nothing but a chat window

Today I took two Android app projects from "someone shared the code with me" to "here's the installable app file" — and I did the whole thing from my phone, inside a Telegram chat with [Hermes](https://hermes-agent.nousresearch.com/), my AI assistant.

No laptop. No Android Studio. No programming tools installed anywhere. I sent messages, and the finished app files came back to the same conversation.

Here's how the day went, including the two things that went wrong.

## App 1: the one that had never built successfully

First up was a finance tracker app. Someone had sent me an invitation to the project on GitHub — a place where developers store and share code. The project had two versions: a web version, and an Android version.

I looked at both and picked the Android one. It was already a real phone app, so there was no reason to rebuild anything from scratch.

There was already an automatic build system set up for it. It had also **never worked**. Two attempts, two failures.

The error message was small but telling: one of the settings the app needed was coming through *empty*, when it had to have a value in it — like submitting a form with the name field left blank. The fix was simple once I understood the cause: put a stand-in value in place when the real one isn't there.

Build passed after that.

## Then my phone refused to install the app

This is where Android stepped in. Google's built-in security, Play Protect, blocks apps that aren't properly signed — a bit like a wax seal on a letter, proving who it's from.

Development versions of apps share one generic seal that every developer on earth uses, so Play Protect doesn't trust them. The fix is to create a proper, personal seal for the app — called a signing key — and use that instead.

I created one, stored it safely in the project's settings, and set things up so every future build is automatically sealed and checked before it gets shared. If the seal is missing or broken, the build stops rather than handing you a file you can't install.

## App 2: the one that couldn't build at all

The second project, a stock tracker, arrived the same way — but in worse shape. It was missing the basic startup script its build system needed, it had never had an automatic build set up, and it was carrying some files that were only meant to stay on the original developer's machine.

I supplied what was missing, tidied up before building, and set up the same automatic system.

Both parts of that build worked first time.

## Then I made a real change: Ghanaian cedi

Between the two projects, I updated the finance app to use Ghanaian cedi instead of US dollars.

Before changing anything, I ran a quick test to see what the app would actually show. It came back `GH₵1,234.56` — exactly right.

While I was in there, I taught the app to recognise cedi in text messages too. In Ghana, mobile money notifications say things like "GHS 50.00" — the app now understands those, not just dollar amounts.

I also swapped the app's icon for a new one: a folder with an arrow rising out of it, sized to fit every kind of phone screen.

## How I knew it actually worked

Here's the part I'd tell anyone doing this: **don't just trust that the build finished.**

Files inside an Android app are deliberately renamed and shuffled around, so it's easy to check the wrong thing and think you're done. Instead, I confirmed it three ways:

- Every icon file I generated matched, exactly, what ended up inside the app
- The finished app reported the correct currency
- The app's own signature checked out — the personal seal was really there

A green tick from the build system only means the process finished. It doesn't mean the right things are inside the file. Checking properly is what turns "it built" into "it works."

## Two honest caveats

The signing key I created has the finance app's name on it, and it now signs both apps. Harmless, but if I ever want a cleaner name on it, anyone who already installed the apps would have to uninstall first.

And because these apps aren't distributed through the Google Play Store, your phone may still show an "unrecognized app" warning when installing. That one has an **Install anyway** option — a different thing from the hard block that stopped the first version.

There's also some digital clutter waiting in both projects — the usual bits and pieces. Next time I'm at a proper keyboard, I'll clear it.

## What I keep coming back to

The loop was simple: *message from my phone → changes saved online → automatic build runs → finished app file arrives back in the same chat → install.*

Twice, with a real feature change squeezed in between.

And the best part isn't today. It's that this setup is permanent. From now on, whenever those projects get updated, a properly sealed, properly checked app builds itself automatically — no laptop required.

Today was just the day it all got switched on. From a phone.
