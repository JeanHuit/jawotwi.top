---
title: "The Pipe"
date: 2018-04-18T12:58:58Z
draft: false
---

<section class="post-content">
            <p>The alternate symbol (vertical bar) on the backslash key, on the standard US keyboard: is known as the pipe. <mark>i'm sure more of you didnt know it was called that</mark>.</p>
<p>And I can bet most people, have not used it before.</p>
<p>If you are a developer or someone on the unix,linux,macOS side of life,or spend most of your time in the terminal or command-line, you are not most people.</p>
<p>The pipe serves a form of redirection, that channels the output of a command,script or program as input for another set of commands, scripts or program.</p>
<p>Eg.<br>
<code>command 1's output | command 2 as input</code><br>
<code>cat text | wc -l</code><br>
The above example, uses the <mark>cat</mark> command on a text document and pipes the result of that instruction into the word count <mark>wc</mark> command with the <mark>-l</mark> argument to show number of lines.</p>
<p>Usage is not limited too<br>
<code>ps aux | grep 'root'| less</code><br>
One can daisy chain more of these pipes together to your hearts content.</p>
<p>Thats it for now.</p>

        </section>