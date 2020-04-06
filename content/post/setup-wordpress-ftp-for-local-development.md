---
title: "Setup Wordpress Ftp for Local Development"
date: 2018-08-25T11:42:25Z
draft: false
---
Ever encountered the issue of setting up an **FTP server** to allow you upload, update themes and plugins on your local/development version of wordpress?

Well, there is a simple solution to that.

Simply edit your `wp-config` file by adding this piece of code anywhere in the above mentioned file.

    define('FS_METHOD', 'direct');
    

This should sort you out.