---
title: "Running Ghost on Google Compute Engine"
date: 2017-07-01T12:34:35Z
draft: false
---
So what do you with **$300** you cannot spend.  
Well except on the platform that gave you the cash, albeit virtual.

I run a blog or as I like to say, a place where I dump my thoughts and ideas at [johnawotwi.me](http://johnawotwi.me) and my favourite platform to run on is Ghost  

So my first expense was to host a ghost blog on Google Compute Engine; this is just an aspect of the whole Google Cloud Platform. Now take note however, Google Cloud Platform has inbuilt deployments of Ghost Blogging platform through the Cloud Launcher \[One click solution/deployment\].

*   Sign in with "as usual" your gmail account.  
    [Google Cloud Console](https://console.cloud.google.com)
*   Select Compute Engine and start a new VM instance.
*   A name of your choice
*   Ubuntu 16.04 (my choice)
*   Setup an f1 micro compute engine VM instance
    *   This is the smallest instance available. I chose to start with this.
*   After the instance is started up, you are presented with option to log into your instance. I choose to this this via "ssh in your browser"
*   Once this is done, update and upgrade your repo and installed packages.
*   Then install: `nginx` , `zip` , `wget`, `node v6` & `nano`
*   Also grab the ghost package while doing that.
*   Start up your nginx server and ensure its working.  
    `service start nginx` and check out the temp IP address provided.

This line will update, upgrade, install and get all the necessary packages needed to continue with this step.

    sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get install -y zip wget nano nginx  && curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash - && sudo apt-get install -y nodejs && wget https://ghost.org/zip/ghost-latest.zip && unzip ghost-latest.zip -d ghost 
    

*   This will copy and extract your ghost directory in your working directory.
    
*   Change into your Ghost directory and run  
    `npm install —production && npm install sqlite3 —save`
    
*   Next we need to make sure `nginx` sees our ghost application and properly redirects traffic to the ghost setup.
    
*   `cd` into `/etc/nginx` and create your own `conf` file aptly named `ghost.conf`
    
*   Using nano or an editor you prefer type this in :
    

    server {
        listen 80;
        server_name your-domain-name.com;
        location / {
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   Host      $http_host;
            proxy_pass         http://127.0.0.1:2368;
        }
    }
    

*   Above are configuration settings that point external requests coming to your **domain name** through **port 80** to the **localhost@2368** which has ghost running. **Note** `your-domain-name.com` can be the external IP google gives you via the console at setup if you do not have a domain name yet.
    
*   Next delete the default conf files in the following directories, using `rm` here.
    

    rm /etc/nginx/sites-available/default
    rm /etc/nginx/sites-enabled/default
    rm /etc/nginx/conf.d/default
    

*   and you are done.
*   restart `ghost` | `nginx` and et voila.

**Note:** Anytime any of the above services stops, your ghost platform stops. Also note external IP's also change. To make them static, you can reserve an IP through the Google cloud console.

*   To do this, click on the options button i.e on the cloud console, click on `Networks > External IP addresses`.
    
*   Select your running instance and click on reserve static address. Thats it! You now have a static ip to go with your ghost instance.
    
*   With a static IP you can configure your domain if you have one, to point to your static IP address. Remember to change `your-domain-name.com` in **ghost.conf** to reflect your new setup if you used the IP initially.
    
*   Next is to get ghost running permanently.
    
*   You can achieve this using [pm2](http://pm2.keymetrics.io/), [forever](https://github.com/foreverjs/forever) or [supervisor](https://github.com/petruisfan/node-supervisor)
    
*   I found **supervisor** worked for me. _**There are many tutorials out there that takes care of this**_
    

Thats it!  
You know have a running ghost blog.

**ps** I received a prompt, citing performance issues, after two days running ghost on the f1 micro. Technical tip was to go in for more ram and processor capacity, that equal $$ out of your $300.