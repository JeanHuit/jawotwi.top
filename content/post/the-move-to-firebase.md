---
title: "The Move to Firebase"
date: 2017-12-14T12:57:25Z
draft: false
---

<section class="post-content">
            <p>For some reason, I just do not remmeber why, I decided to find out if my one off blog could find another home.</p>
<p>For two years, this blog has been <s>squatting</s> living for free on github and before that blogger.</p>
<p>Today, I'm proud to say, what begun as:<br>
<em><a href="http://bustlive.blogspot.com">http://bustlive.blogspot.com</a></em> --&gt; <em><a href="http://jeanhuit.github.io">http://jeanhuit.github.io</a></em> and then to <em><a href="http://johnawotwi.me">http://johnawotwi.me</a></em> is now <em><a href="https://johnawotwi.me">https://johnawotwi.me</a></em> .<br>
New digs and all, notice the extra (s) in there..yuh, that is all for free.</p>
<p>See <a href="https://johnawotwi.me/ghost-adventures-i/">Ghost Adventures</a> for the initial steps, especially the update.</p>
<p>All you will need to replace is the part about github. Instead of hosting and setting up a git repo, get a free account and setup a free project 'static sites' only at <code>console.firebase.google.com</code><br>
Install the firebase CLI (command line interface), login,initialize the project folder, select your static output folder and then deploy.</p>
<p>Obviously, <a href="https://johnawotwi.me/know-your-node/">you should know your node</a> first.</p>
<ul>
<li>install the firebase tools</li>
</ul>
<pre><code>npm install -g firebase-tools 
</code></pre>
<ul>
<li>provide your credentials, popup opens a browser</li>
</ul>
<pre><code>firebase login 
</code></pre>
<pre><code>cd &lt;project folder&gt;
</code></pre>
<ul>
<li>initialize the project, select the kind of project, hosting</li>
</ul>
<pre><code>firebase init
</code></pre>
<ul>
<li>select path to folder for static pages</li>
</ul>
<pre><code>firebase deploy
</code></pre>
<h1 id="etvoila">et voila!!!</h1>

        </section>