---
title: "Grep"
date: 2017-09-02T12:20:27Z
draft: false
---

<section class="post-content">
            <p>Another linux command, I find very useful, this is a command that helps you search for strings/text within documents. There are a whole lot of uses for it, but I will leave you to explore that yourself.</p>
<p>Its simplest form is:</p>
<pre><code>grep &lt;word&gt; &lt;in file&gt;
=&gt; grep "dog" animals.txt
</code></pre>
<p>The above looks for <mark>dog</mark> in a text file called <mark>animal.txt</mark></p>
<p>There are flags/options you can set with the command to make things easier.</p>
<pre><code> -x = exclusive, exact match
 -v = everything but
 -i = I do not care about case
</code></pre>
<p>and many more.</p>
<p>You can also use <mark>[]</mark> and <mark>^</mark> to help make your search more refined.</p>
<pre><code>grep ^a* fruits.txt
</code></pre>
<p>Finds fruits that have <mark>a</mark> in them</p>
<pre><code> grep ^a.p fruits.txt
</code></pre>
<p>Finds fruits that begin with an <mark>a</mark> and followed a random letter and then by a <mark>p</mark>.</p>
<pre><code>grep ^[a-p] fruits.txt
</code></pre>
<p>Find all text that begin with an <mark>a</mark> through to <mark>P</mark> in fruits.txt<br>
Go ahead and play with grep!</p>
<p>Lastly, grep can search through huge files very quickly, and outputs can be overwhelming, eg. log files. To make it easier, and this can be used for most linux commands,you can pipe commands through each other.</p>
<pre><code>ps aux | grep 'root'| less
</code></pre>
<p>This simply means, I am looking for <mark>root</mark> in the output of <code>ps aux</code> but due to the volume outputted, I want to see them in pages, thus the use of <code>less</code>.</p>
<p>Go ahead and play with grep. Fun times ahead.</p>

        </section>
