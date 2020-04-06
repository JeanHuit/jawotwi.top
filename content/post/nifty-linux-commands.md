---
title: "Nifty Linux Commands"
date: 2017-07-04T12:23:37Z
draft: false
---

<section class="post-content">
            <blockquote>
<p>This post is the beginning of a series I'd tag <mark>nlc</mark> to talk about linux commands that I come across.A <strong>simpler man</strong> page for myself of my own words, minus the bells and whistles of the many options you come across in the man pages without almost ever using.</p>
</blockquote>
<hr>
<h2 id="netstat">Netstat</h2>
<p>Short for network status, this command when run without options <code>netstat</code> , can get carried away. Displaying all incoming and outgoing network requests at a go.  This can be daunting and one may easily get lost trying to sift through all that data.<br>
Piping <code>|</code> the data through <code>less</code> will make it easier for you to peruse and understand where your data  is going, from what application and from what point data is being returned.<br>
eg.</p>
<pre><code class="language-bash">netstat -nr | less
</code></pre>
<p>Using the <code>- nr</code> option, gives you access to your routing table in number format, i.e shows you the network address.</p>

        </section>