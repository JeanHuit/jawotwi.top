---
title: My Fire Tablet Wouldn't Stop Restarting — So Hermes Fixed It Over USB
date: 2026-09-07T22:09:43Z
draft: false
description: "My Amazon Fire HD 8 (2020) started doing something deeply annoying: restarting \"on the regular,\" and almost on cue whenever I launched an app. Full restarts, too — Amazon logo, boot animation, the wor"
author: John Awotwi
category: Blogging
tags: ["fire-tablet", "amazon", "android", "adb", "fire-os", "troubleshooting", "debugging", "ai-assistant", "hermes-agent"]
keywords: ["fire-tablet", "amazon", "android", "adb", "fire-os", "troubleshooting", "debugging", "ai-assistant", "hermes-agent"]
excerpt: "My Amazon Fire HD 8 (2020) started doing something deeply annoying: restarting \"on the regular,\" and almost on cue whenever I launched an app. Full re"
---

# My Fire Tablet Wouldn't Stop Restarting — So Hermes Fixed It Over USB

## The setup

My Amazon Fire HD 8 (2020) started doing something deeply annoying: restarting "on the regular," and almost on cue whenever I launched an app. Full restarts, too — Amazon logo, boot animation, the works. My first instinct, like anyone's, was hardware. An old tablet with an old battery, randomly power-cycling under load? Classic.

I plugged it into my PC, fired up [Hermes](https://hermes-agent.nousresearch.com/) — my AI agent — and asked it to take a look over USB. What followed was one of the most satisfying debugging sessions I've had in a while, and the fix wasn't a new battery. It wasn't even a factory reset.

## Plot twist: it was never really rebooting

The first clue was a contradiction. Hermes pulled the kernel uptime: **7 days**. The tablet had supposedly been "restarting" all week — yet the kernel had not once gone down. What I was seeing was a *soft reboot*: Android's core process (`system_server`) was crashing, and the framework was auto-restarting itself. On a Fire tablet, a framework restart replays the full boot animation from scratch. To the user — me — that *is* a restart. To the kernel, nothing happened. The USB connection never even blinked.

So the question changed from "why is the battery dying?" to "what keeps killing system_server?"

## Finding the culprits in the crash logs

This is where having an agent that can actually read the device paid off. Fire tablets keep a hidden dropbox of crash reports, and Hermes pulled three days of them:

1. **Amazon's dcpms service was crash-looping.** `com.amazon.dcpms.fos.service` — Amazon's "Device Control & Policy Management" — had hard-crashed 8 times in 3 days, roughly every 6 hours. Its signature error was a lifecycle bug: it kept getting torn down mid user-switch, firing "receiver not registered" crashes.

2. **The kids profile was wedging the system.** The tablet had a kids profile , which Fire OS runs as a separate Android user (`user 10`). The log right before one restart said it all: `User switch timeout: from 10 to 0` — a profile switch that got stuck and took `system_server` down with it. Throw in a 2 GB tablet running on fumes (70 MB of free RAM, load average 16), and launching an app was all it took to tip the whole house of cards.

3. The old battery got a cameo — the boot log from a week earlier showed a genuine battery-forced shutdown. But it was a red herring for the *current* problem. The restarts were software, not silicon.

## The fix, three commands deep

All of it was doable over USB, no root required:

```
adb shell pm clear com.amazon.dcpms.fos.service   # wipe dcpms's corrupted state
adb shell pm remove-user 10                        # remove the kids profile
adb reboot                                         # clean start
```

Clearing dcpms's data let Amazon's own service rebuild itself from scratch. Removing the kids profile deleted the entire second-user machinery that kept jamming the system — and, as a bonus, freed about **9 GB** of space it had been hoarding. The tablet booted in 25 seconds and the crash log went silent.

## Going full de-Amazon

While we were in there, we went further. I don't use the Amazon ecosystem — I sideload APKs — so we killed the noise at the source:

- Deregistered the Amazon account (the one step that needs a thumb instead of a terminal — it's a server-side operation). No account means the launcher's endless "account needs recovery" retry loop has nothing left to reach for, and Amazon stops pushing OS updates to the device entirely.
- Disabled the background bloat that was spamming errors: Alexa (both components), Prime Video, and the wallpaper service. All reversible with `pm enable`.

Result: a Fire tablet with 21 GB free, no Amazon account nagging, no crash-looping services, and no kids profile waiting to wedge the next profile switch.

## What I learned

- **"Restarting" on a Fire tablet is often a soft reboot.** Boot animation ≠ kernel reboot. Check `uptime` before you blame the battery.
- **The crash logs are there — you just need someone to read them.** Amazon's dropbox, boot reasons, and process forensics told us more in ten minutes than weeks of "just factory reset it" advice ever would.
- **You can do a lot to a Fire tablet over adb without root** — clear system-app data, manage users, disable Amazon's bloat. Root wasn't needed and, on this model, isn't even available.
- **The old battery is still worth respecting.** It's a 2019-era tablet with a tired cell — it now lives on a proper wall charger instead of a PC's anemic USB port.

The tablet has been stable since the fix. If it ever restarts again, the crash log will tell us exactly why — and Hermes will be one USB cable away.

*This debugging session was a collaboration between me and Hermes, my AI agent. I drove the questions; it read the logs, found the patterns, and walked me through every fix over adb. If your device is doing something weird, let an agent read its logs before you buy a replacement.*
