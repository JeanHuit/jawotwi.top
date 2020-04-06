---
title: "Running Ghost on Google Compute Engine"
date: 2017-07-01T12:34:35Z
draft: false
---

<section class="post-content">
            <p>So what do you with <strong>$300</strong> you cannot spend.<br>
Well except on the platform that gave you the cash, albeit virtual.</p>
<p>I run a blog or as I like to say, a place where I dump my thoughts and ideas at <a href="http://johnawotwi.me">johnawotwi.me</a> and my favourite platform to run on is Ghost<br>
</p>
<p>So my first expense was to host a ghost blog on Google Compute Engine; this is just an aspect of the whole Google Cloud Platform. Now take note however, Google Cloud Platform  has inbuilt deployments of Ghost Blogging platform through the Cloud Launcher [One click solution/deployment].</p>
<ul>
<li>Sign in with "as usual" your gmail account.<br>
<a href="https://console.cloud.google.com">Google Cloud Console</a></li>
<li>Select Compute Engine and start a new VM instance.</li>
<li>A name of your choice</li>
<li>Ubuntu 16.04 (my choice)</li>
<li>Setup an f1 micro compute engine VM instance
<ul>
<li>This is the smallest instance available. I chose to start with this.</li>
</ul>
</li>
<li>After the instance is started up, you are presented with option to log into your instance. I choose to this this via "ssh in your browser"</li>
<li>Once this is done, update and upgrade your repo and installed packages.</li>
<li>Then install: <code>nginx</code> , <code>zip</code> , <code>wget</code>, <code>node v6</code> &amp; <code>nano</code></li>
<li>Also grab the ghost package while doing that.</li>
<li>Start up your nginx server and ensure its working.<br>
<code>service start nginx</code> and check out the temp IP address provided.</li>
</ul>
<p>This line will update, upgrade, install and get all the necessary packages needed to continue with this step.</p>
<pre><code class="language-bash">sudo apt-get update &amp;&amp; sudo apt-get upgrade -y &amp;&amp; sudo apt-get install -y zip wget nano nginx  &amp;&amp; curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash - &amp;&amp; sudo apt-get install -y nodejs &amp;&amp; wget https://ghost.org/zip/ghost-latest.zip &amp;&amp; unzip ghost-latest.zip -d ghost 
</code></pre>
<ul>
<li>
<p>This will copy and extract your ghost directory in your working directory.</p>
</li>
<li>
<p>Change into your Ghost directory and run<br>
<code>npm install —production &amp;&amp; npm install sqlite3 —save</code></p>
</li>
<li>
<p>Next we need to make sure <code>nginx</code> sees our ghost application and properly redirects traffic to the ghost setup.</p>
</li>
<li>
<p><code>cd</code> into <code>/etc/nginx</code> and create your own <code>conf</code> file aptly named <code>ghost.conf</code></p>
</li>
<li>
<p>Using nano or an editor you prefer type this in :</p>
</li>
</ul>
<pre><code class="language-bash">server {
    listen 80;
    server_name your-domain-name.com;
    location / {
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   Host      $http_host;
        proxy_pass         http://127.0.0.1:2368;
    }
}
</code></pre>
<ul>
<li>
<p>Above are configuration settings that point external requests coming to your <strong>domain name</strong> through <strong>port 80</strong> to the <strong>localhost@2368</strong> which has ghost running. <strong>Note</strong> <code>your-domain-name.com</code> can be the external IP google gives you via the console at setup if you do not have a domain name yet.</p>
</li>
<li>
<p>Next delete the default conf files in the following directories, using <code>rm</code> here.</p>
</li>
</ul>
<pre><code class="language-bash">rm /etc/nginx/sites-available/default
rm /etc/nginx/sites-enabled/default
rm /etc/nginx/conf.d/default
</code></pre>
<ul>
<li>and you are done.</li>
<li>restart <code>ghost</code> | <code>nginx</code> and et voila.</li>
</ul>
<p><strong>Note:</strong> Anytime any of the above services stops, your ghost platform stops. Also note external IP's also change. To make them static, you can reserve an IP through the Google cloud console.</p>
<ul>
<li>
<p>To do this, click on the options button i.e on the cloud console, click on <code>Networks &gt; External IP addresses</code>.</p>
</li>
<li>
<p>Select your running instance and click on reserve static address. Thats it! You now have a static ip to go with your ghost instance.</p>
</li>
<li>
<p>With a static IP you can configure your domain if you have one, to point to your static IP address. Remember to change <code>your-domain-name.com</code> in <strong>ghost.conf</strong>  to reflect your new setup if you used the IP initially.</p>
</li>
<li>
<p>Next is to get ghost running permanently.</p>
</li>
<li>
<p>You can achieve this using <a href="http://pm2.keymetrics.io/">pm2</a>, <a href="https://github.com/foreverjs/forever">forever</a> or <a href="https://github.com/petruisfan/node-supervisor">supervisor</a></p>
</li>
<li>
<p>I found <strong>supervisor</strong> worked for me. <em><strong>There are many tutorials out there that takes care of this</strong></em></p>
</li>
</ul>
<p>Thats it!<br>
You know have a running ghost blog.</p>
<p><strong>ps</strong> I received a prompt, citing performance issues, after two days running ghost on the f1 micro. Technical tip was to go in for more ram and processor capacity, that equal $$ out of your $300.</p>

        </section>