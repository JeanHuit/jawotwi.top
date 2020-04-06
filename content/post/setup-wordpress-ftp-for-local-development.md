---
title: "Setup Wordpress Ftp for Local Development"
date: 2018-08-25T11:42:25Z
draft: false
---

<p>Ever encountered the issue of setting up an <strong>FTP server</strong> to allow you upload, update themes and plugins on your local/development version of wordpress?</p>
<p>Well, there is a simple solution to that.</p>
<p>Simply edit your <code>wp-config</code> file by adding this piece of code anywhere in the above mentioned file.</p>
<pre><code>define('FS_METHOD', 'direct');
</code></pre>
<p>This should sort you out.</p>