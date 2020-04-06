---
title: "Wifite"
date: 2015-06-02T13:08:58Z
draft: false
---

I knew the title of my post, I knew the plot my post was going to take, but I did not know how to start. So I am just going to tell it like I hear it in my head.

People who work with computers almost always seem to have time on their hands, and the excuse, “its compiling”,”Its rendering”, “its…”. Todays topic is on a tool that makes wireless security pen-tests a breeze, you also get to say “its capturing”.

**Wifite** is its name of this tool.

When I got to know of this project it was hosted publicly on google code : [https://code.google.com/p/wifite/](https://code.google.com/p/wifite/) however it has since moved to Github : [https://github.com/derv82/wifite](https://github.com/derv82/wifite) All current development is done on Github. To follow, contribute, start, watch, get to the Github repo.

This tool, makes use of our famous aircrack-ng suite, reaver, pyrit, cowpatty, a wireless card and the appropriate drivers that are patched for injection and promiscuous/monitor mode. Unfortunately for my windows users, this tool only works in the linux environment. Most specifically, Kali Linux, gentoo, blackbox or ubuntu based distros. Recent versions of Kali Linux - the pentesters wet dream, ships with Wifite .  
Get the latest/current wifite version from

`wget https://raw.github.com/derv82/wifite/master/wifite.py`

Start up the application,with escalated privileges “command line please” -

`sudo chmod +x wifite.py` && `sudo ./wifite.py`  
and voila .

The application starts and scans for available SSID’s and gives you the option to attempt a pentest on one, two or all discovered SSID’s. Exploiting all known vulnerabilities in your chosen security implemetation (WEP|WPA|WPA2|WPS).  
This is in no way detailed. Just an introduction to the tool wifite. Its interface, albeit commandline based, its truly intuitive.

**NB:** _This post is in no way giving you the permission to cause havoc.  
Yes, this here is a disclaimer, I will not be held responsible for any distraction you cause with said tool. This hear has been introduced for academic purposes. Seek for permission before you use this tool on a WIFI network that is not yours._