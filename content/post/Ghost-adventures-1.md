---
title: "Ghost Adventures 1"
date: 2015-03-20T12:10:06Z
draft: false
---

<section class="post-content">
            <p>These adventures follow Jean in his quest to get a blog up and running the open source way. The first in the series,tell of how Jean battled to get Ghost working on the OS X platform locally and on Github as static pages.</p>
<p>Battle Duration: 30 mins</p>
<p><strong>Update-25/08/2017</strong><br>
As at writing, Ghost has gained 1.0 status and has an even simpler method of installation.<br>
instead of hopping through the afore mentioned hoops to do a simple local install.</p>
<pre><code>1. npm install -g ghost-cli
2. mkdir &lt;a new directory&gt;
3. ghost install local
</code></pre>
<p>The above assumes you have <code>npm</code> already installed to work. After this, you need to install <code>buster</code> and continue as before. See installation steps below.<br>
To start and stop ghost is as simple as <code>ghost start</code> and <code>ghost stop</code>.</p>
<h4 id="installingnecessarytools">Installing necessary tools.</h4>
<p>Brew (package manager):</p>
<pre><code>`ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)” &amp;&amp; brew update &amp;&amp; brew doctor`
</code></pre>
<p>Wget (software for retrieving files over http(s),ftp):</p>
<p><code>brew install wget</code></p>
<p>Node (platform for building fast,scalable network applications):</p>
<p><code>brew install node</code></p>
<p>Python (Programming language):</p>
<p><code>brew install python</code></p>
<p>This also installs <em>pip</em> - a tool for installing and managing python packages.</p>
<p>Buster (To generate static pages):</p>
<p><code>pip install buster</code></p>
<p>Git (versioning control sytem):</p>
<p><code>brew install git</code></p>
<p>Git might already be installed on your system.</p>
<h4 id="downloadinstallghost">Download &amp; Install Ghost</h4>
<p>Time to  download Ghost - the simple publishing platform this fuss is all about. <a href="https://ghost.org/download/">https://ghost.org/download/</a></p>
<p>I found it much better to follow this directory structure.</p>
<ol>
<li>Blog{your main folder}
<ul>
<li>Files{subfolder to Blog}<br></li>
<li>Ghost{subfolder to Blog}</li>
</ul>
</li>
</ol>
<p><code>mkdir Blog 	cd Blog 		mkdir Files 		mkdir Ghost</code></p>
<p>Unzip ghost.**.zip  into Blog/Ghost.</p>
<p>Change directory to Ghost and run <code>npm install</code>  or <code>npm install -—production</code> to install</p>
<p>Then run <code>npm start</code> to get your local server up and running.</p>
<p>Navigated to <code>localhost:2368/ghost</code> This allows you to setup Ghost.<br>
Once logged in , the interface is simply intuitive..</p>
<p>Ghost is up and running.</p>
<p>NB: Posts are written using <a href="https://help.github.com/articles/markdown-basics/"> markdown</a>; a simple markup language.</p>
<h4 id="setupgitpages">Setup Git Pages</h4>
<p>You need to set up a free Github account and once that is done, you create a new repository with a specific naming convention to allow you have a Github page. Named as such:  “<strong>username.github.io</strong>”</p>
<p>Once you are done writing, you need to create static pages,since Github will only serve static pages.<br>
Hello "Buster"</p>
<h4 id="publishing">Publishing</h4>
<p>Switch directory to "Files", the sub-folder under Blog.<br>
Your new repo address must be handy,</p>
<p>In the new folder  run <code>buster setup</code> this command prompts for the repo address, below is a sample.Replace "username" with yours and hit enter.</p>
<p><code>https://github.com/username/username.github.io.git</code></p>
<p>Once this is done, all you need to run to generate the statics pages is</p>
<p><code>buster generate —domain=http://127.0.0.1:2368 &amp;&amp; buster deploy</code></p>
<p>This pushes latest changes to Github, and voila  you now have a website.</p>
<p>Bear in mind, you need to run <code>buster generate —domain=http://127.0.0.1:2368 &amp;&amp; buster deploy</code>  after every edit, to push to Github (public). You can view your changes locally,at <code>localhost:2368</code> before pushing to Github.</p>
<p><strong>Workflow</strong></p>
<ol>
<li>Change your directory to Ghost directory
<ul>
<li>Run <code>npm start</code> in your terminal</li>
</ul>
</li>
<li>Open <code>localhost:2368</code> in browser</li>
<li>Edit and/or write post, tweak settings</li>
<li>Save</li>
<li>Change directory to Files</li>
</ol>
<ul>
<li>run <code>buster generate —domain=http://127.0.0.1:2368</code><br>
and <code>buster deploy</code></li>
</ul>
<ol start="6">
<li>Done</li>
</ol>
<p><strong>Repeat 5 - 6 after each post, to generate and publish to Github</strong></p>

        </section>