---
title: "An Outline of Outline"
date: 2018-10-08T11:44:56Z
draft: false
---
An upcoming travel opportunity had me searching for a VPN service I could use whiles away from 127.0.0.1 . This search lead me to [Outline.](https://www.getoutline.org/en/home)  A free vpn tool tailored for journalist - Touted as granting you access to the "internet you can trust" , as having "strong privacy and security".

What led me to choose Outline over the rest, was the fact that you could run this vpn tool on your own server or a [VPS](https://en.wikipedia.org/wiki/Virtual_private_server) of your choice.

The three things you would need to get started:

1.  A VPS of your choice eg. Vultr, AWS, Google Platform, Digital Ocean etc
2.  [The Outline Manger](https://github.com/Jigsaw-Code/outline-server/releases)
3.  [The Outline Client](https://github.com/Jigsaw-Code/outline-client/releases)

*   Spin up a linux based server on your VPS
*   Login to your server, **ssh** credentials should be available to you.
*   Follow the prompts on the Outline Manager to setup the server.
*   Download the Outline Client and add a server by copying and pasting an access key made available via the Outline Manager

And just like that you have a VPN connection setup. Your conversations, transactions etc etc are all free from prying eyes.

Another thing I like is that, I can just destroy my server and spin up another one and a completely new VPN connection anytime I want.