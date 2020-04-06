---
title: "The Pipe"
date: 2018-04-18T12:58:58Z
draft: false
---

The alternate symbol (vertical bar) on the backslash key, on the standard US keyboard: is known as the pipe. i'm sure more of you didnt know it was called that.

And I can bet most people, have not used it before.

If you are a developer or someone on the unix,linux,macOS side of life,or spend most of your time in the terminal or command-line, you are not most people.

The pipe serves a form of redirection, that channels the output of a command,script or program as input for another set of commands, scripts or program.

Eg.  
`command 1's output | command 2 as input`  
`cat text | wc -l`  
The above example, uses the cat command on a text document and pipes the result of that instruction into the word count wc command with the \-l argument to show number of lines.

Usage is not limited too  
`ps aux | grep 'root'| less`  
One can daisy chain more of these pipes together to your hearts content.

Thats it for now.