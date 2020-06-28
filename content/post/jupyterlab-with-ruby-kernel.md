---
title: " Setting Up Jupyterlab With Ruby Kernel (MacOS)"
date: 2020-06-28T02:52:22Z
draft: false
---

Many are the reasons I choose to setup JupyterLabs with a Ruby Kernel, I will however not disclose those reasons :)

- Setup python, pip, jupyter / jupyterlabs , ruby (soo many tutorials out there)
- Setup the ruby kernel, especially on MacOS, not that many.

```gem install cztop ffi-_rzmq iruby```
- Consider installing the optional dependencies to get additional functionality (gem install):
  * pry
  * pry-doc
  * awesome_print
  * gnuplot
  * rubyvis
  * nyaplot
  * cztop
  * rbczmq***

- 'rbczmq' might fail if your build tools are not setup. To do that, run:
``` brew insall libtool autoconf automake ```
and rerun ```gem install rbczmq```
- Run ``` iruby register --force ```
- Restart your jupyterlab notebook to find your ruby kernel included.