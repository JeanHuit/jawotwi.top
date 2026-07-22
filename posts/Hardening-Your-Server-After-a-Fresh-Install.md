---
title: Hardening Your Server After a Fresh Install
date: 2026-07-22T00:00:00Z
draft: true
description: "When you spin up a fresh Linux server, the default configuration is built for convenience, not security. The package manager is pointed at trusted repositories, SSH lets you in with a password, and do"
author: John Awotwi
category: Blogging
tags: ["security", "server", "linux", "devops", "hardening", "sysadmin"]
keywords: ["security", "server", "linux", "devops", "hardening", "sysadmin"]
excerpt: "When you spin up a fresh Linux server, the default configuration is built for convenience, not security. The package manager is pointed at trusted rep"
---

When you spin up a fresh Linux server, the default configuration is built for convenience, not security. The package manager is pointed at trusted repositories, SSH lets you in with a password, and dozens of services start automatically whether you need them or not. For the first few minutes of its life, your server is a blank slate -- but every minute it stays in that default state is a minute it is exposed.

I have been through enough setup cycles to know that manually locking down a server is repetitive and easy to get wrong. So I put together a hardening script that walks through the essential steps. This post covers what you are up against when you put a server online and what each piece of the script does to address those risks.

The full script is public on GitHub at the link below. You can read through it, suggest improvements, or submit edits if something is missing.

---

### The Risks of an Unhardened Server

A server connected to the internet is probed within minutes of going live. Automated scanners crawl IP ranges looking for open SSH ports, default credentials, or unpatched services. These scans are not personal -- they are bots running around the clock, and they do not discriminate.

If your server has password-based SSH login enabled, those bots will try thousands of username and password combinations. If a service like CUPS or Avahi is running and you do not need it, it is one more surface area to exploit. If automatic updates are not configured, known vulnerabilities stay open until you manually patch them -- and in practice that can take weeks.

The risks fall into a few categories: unauthorised access, information leakage, denial of service, and privilege escalation. A single weak point -- a root SSH login with a simple password, an unneeded service with a known CVE, a kernel parameter that allows IP spoofing -- can turn a fresh server into a compromised machine before you have even deployed your application.

---

### What the Script Does

The script is called `hardeninig.sh` and it is designed for Debian-based distributions. It is structured as a series of steps that can be run on a freshly installed system. Below is a breakdown of each section and the reasoning behind it.

#### 1. System Update and Upgrade

The first step is running `apt update` and `apt full-upgrade`. This ensures all currently installed packages are at their latest versions. Many fresh install images ship with packages that are already several weeks or months old, and the latest updates contain security patches for known vulnerabilities. There is no point hardening a system that still has unpatched software on it.

#### 2. Installation of Security Tools

The script installs a collection of tools that collectively cover monitoring, access control, and auditing:

- **ufw** -- the Uncomplicated Firewall. It provides a simple interface to iptables for managing which ports are open to the network.
- **fail2ban** -- a log-parsing daemon that bans IP addresses showing malicious behaviour, such as repeated failed SSH login attempts.
- **unattended-upgrades** -- automatically installs security updates as soon as they are released, so you do not have to log in every week to patch.
- **apt-listchanges** -- displays a summary of package changes before they are applied during updates, so you know what is changing.
- **debsums** -- verifies installed package files against their checksums, making it possible to detect files that have been altered after installation.
- **rkhunter** -- the Rootkit Hunter. It scans the system for signs of rootkits, backdoors, and other malware.
- **auditd** -- the Linux Audit daemon. It writes detailed logs of system calls, file access, and authentication events for forensic analysis.
- **logwatch** -- a log summariser that can email you daily reports of what happened on your server.
- **sudo** -- allows authorised users to run commands as root without sharing the root password, and logs every command executed.

#### 3. Automatic Updates

Running `dpkg-reconfigure unattended-upgrades` enables the automatic installation of security updates. Once this is configured, critical patches arrive and are applied without manual intervention. You can still review what was installed by checking the log files.

#### 4. UFW Firewall Configuration

The firewall is set to deny all incoming traffic by default and allow all outgoing traffic. This means that unless you explicitly open a port, nothing can reach your server from the outside. The script then opens port 22 for SSH. If you run your SSH on a non-standard port, you would change this line before running the script.

After the rules are set, the firewall is enabled. Enabling a firewall remotely can lock you out if you have not left SSH access open, which is why the `ufw allow OpenSSH` line comes before `ufw --force enable`.

#### 5. SSH Hardening

SSH is one of the most attacked services on any public server. The script makes several changes to `/etc/ssh/sshd_config`:

- **PermitRootLogin no** -- disallows direct login as root. You log in as a regular user and use `sudo` when you need elevated privileges.
- **PasswordAuthentication no** -- disables password-based logins entirely. Only SSH key authentication is allowed. This single change stops the vast majority of brute force attacks.
- **X11Forwarding no** -- turns off X11 forwarding, which is rarely needed on a server and can be a vector for session hijacking.
- **MaxAuthTries 3** -- limits authentication attempts before the connection is dropped.
- **ClientAliveInterval 300** and **ClientAliveCountMax 2** -- detects dead or orphaned SSH sessions and disconnects them after 10 minutes of inactivity.

A backup of the original configuration is saved before changes are applied.

#### 6. Fail2Ban Configuration

Fail2Ban monitors log files for repeated failed authentication attempts and temporarily bans the offending IP address using the system firewall. The script writes a local configuration that sets a 10-minute ban window for IPs that fail 5 times within 10 minutes. This protects against SSH brute force attacks without permanently blocking legitimate users who mistype a password.

#### 7. File Permissions

The script sets `/root` to mode 700 (only root can read, write, or enter the directory) and `/etc/ssh/sshd_config` to mode 600 (only root can read or write the SSH configuration). Both are sensible defaults that prevent other users or processes from accessing sensitive files.

#### 8. Auditd

The audit daemon is enabled and started. Once running, it logs system calls, login events, and file accesses to a dedicated log file. If your server is ever compromised, these logs are the primary source of evidence for determining how the attacker got in and what they did.

#### 9. Rootkit Detection

Rkhunter is updated and its property database is initialised. This gives you a baseline of file checksums that the tool can compare against in future scans. Running `rkhunter --check` periodically will alert you if any system binaries have been modified by malware.

#### 10. Disabling Unnecessary Services

The script disables and stops `avahi-daemon` (mDNS/Bonjour broadcasting) and `cups` (the print service). Neither service is needed on a typical server, and both have had remote code execution vulnerabilities in the past. If your server does not need to advertise itself on the local network or accept print jobs, these services should not be running.

#### 11. Kernel Hardening

The script applies several kernel parameter changes via `sysctl`:

- **IP forwarding is disabled** -- the server will not route traffic between networks unless explicitly configured to do so.
- **Accept and send redirects are disabled** -- prevents an attacker from altering your server's routing table through ICMP redirect messages.
- **Source route acceptance is disabled** -- blocks IP packets that specify their own route, which can be used for spoofing.
- **Martian packets are logged** -- packets that arrive on an interface they should not have, often a sign of misconfiguration or an attack.
- **ICMP broadcast echo requests are ignored** -- prevents the server from being used in a Smurf amplification attack.
- **Bogus ICMP error responses are ignored** -- drops malformed ICMP packets.
- **ASLR is enabled** -- kernel address space layout randomisation makes it harder for exploit code to predict memory addresses.

These changes are written to `/etc/sysctl.d/99-hardening.conf` and applied immediately.

#### 12. Password Policies

The `libpam-pwquality` module is installed and configured to enforce password complexity: minimum 12 characters, with at least one uppercase letter, one lowercase letter, one digit, and one special character. This applies only if password authentication is used anywhere on the system.

#### 13. Locking Unused Accounts

System accounts like `games` and `news` are locked with `passwd -l`. These accounts exist by default on many Linux installations but are not needed for normal server operation. Locking them removes them as potential entry points.

---

### Using the Script

The script is available as a public gist on GitHub:

https://gist.github.com/JeanHuit/7e551d11ec8b9e15b8a49507e2f0c16e

You can download it, review the code, and run it on a fresh Debian-based system. Because it makes several irreversible changes -- particularly disabling password-based SSH login -- it is worth reading through the whole thing first and adjusting any settings that do not match your environment.

If you spot something I have missed or have a suggestion for improvement, the gist supports comments and edits. The goal is to keep this script practical and up to date as new threats and tools emerge.

---

### One Last Thing

The script disables password-based SSH login in favour of key-based authentication. You need to make sure your SSH public key is in place on the server before running the script, or you will lose access. The script ends with a reminder to verify that key-based login works before closing your current session. That reminder is there because I have locked myself out exactly that way and I suspect I am not the only one.
