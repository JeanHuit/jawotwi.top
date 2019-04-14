---
title: "Uploading Wordpress to a Live Server"
date: 2019-04-14T21:33:59Z
draft: false
---

There are a thousand and one tutorials on the internet that teach how to go about this (title of post).
There are as well a plethora of plugins that claim to help you do this. I have tried most and what I have found is that, these plugins are not reliable and the tutorials are not always complete.

-------

1. Make a backup of your  database from your development server, i.e export the database you created when you started working on your wordpress based site.  ````somethings.sql````
2. Cleanup your website, i.e get rid of all unused plugins and media files, this causes unneccessary bloat.
3. Create a database on your production (live) server and upload the backup of your datebase (done in step 1), ```something.dql```
4. On your production server database, replace all instances of  ```http:\\localhost``` with  ```http:\\newdomain.com``` in database uploaded in step 3.
5. Edit your ```config.php``` file with the credentials  of your production server, i.e  ["DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST"]
6. Upload your websites directory/src/folder to the root of your production server. ```http:\\newdomain.com```
7. Your website should be up and running, no messy plugins needed.

###### NB:
Do not forget to change the password you used in development.
