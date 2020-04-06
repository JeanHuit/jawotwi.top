---
title: "Nifty Linux Commands"
date: 2017-07-04T12:23:37Z
draft: false
---

> This post is the beginning of a series I'd tag nlc to talk about linux commands that I come across.A **simpler man** page for myself of my own words, minus the bells and whistles of the many options you come across in the man pages without almost ever using.

* * *

Netstat
-------

Short for network status, this command when run without options `netstat` , can get carried away. Displaying all incoming and outgoing network requests at a go. This can be daunting and one may easily get lost trying to sift through all that data.  
Piping `|` the data through `less` will make it easier for you to peruse and understand where your data is going, from what application and from what point data is being returned.  
eg.

    netstat -nr | less
    

Using the `- nr` option, gives you access to your routing table in number format, i.e shows you the network address.