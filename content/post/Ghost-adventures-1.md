---
title: "Ghost Adventures 1"
date: 2015-03-20T12:10:06Z
draft: false
---
These adventures follow Jean in his quest to get a blog up and running the open source way. The first in the series,tell of how Jean battled to get Ghost working on the OS X platform locally and on Github as static pages.

Battle Duration: 30 mins

**Update-25/08/2017**  
As at writing, Ghost has gained 1.0 status and has an even simpler method of installation.  
instead of hopping through the afore mentioned hoops to do a simple local install.

    1. npm install -g ghost-cli
    2. mkdir <a new directory>
    3. ghost install local
    

The above assumes you have `npm` already installed to work. After this, you need to install `buster` and continue as before. See installation steps below.  
To start and stop ghost is as simple as `ghost start` and `ghost stop`.

#### Installing necessary tools.

Brew (package manager):

    `ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)” && brew update && brew doctor`
    

Wget (software for retrieving files over http(s),ftp):

`brew install wget`

Node (platform for building fast,scalable network applications):

`brew install node`

Python (Programming language):

`brew install python`

This also installs _pip_ - a tool for installing and managing python packages.

Buster (To generate static pages):

`pip install buster`

Git (versioning control sytem):

`brew install git`

Git might already be installed on your system.

#### Download & Install Ghost

Time to download Ghost - the simple publishing platform this fuss is all about. [https://ghost.org/download/](https://ghost.org/download/)

I found it much better to follow this directory structure.

1.  Blog{your main folder}
    *   Files{subfolder to Blog}  
        
    *   Ghost{subfolder to Blog}

`mkdir Blog cd Blog mkdir Files mkdir Ghost`

Unzip ghost.\*\*.zip into Blog/Ghost.

Change directory to Ghost and run `npm install` or `npm install -—production` to install

Then run `npm start` to get your local server up and running.

Navigated to `localhost:2368/ghost` This allows you to setup Ghost.  
Once logged in , the interface is simply intuitive..

Ghost is up and running.

NB: Posts are written using [markdown](https://help.github.com/articles/markdown-basics/); a simple markup language.

#### Setup Git Pages

You need to set up a free Github account and once that is done, you create a new repository with a specific naming convention to allow you have a Github page. Named as such: “**username.github.io**”

Once you are done writing, you need to create static pages,since Github will only serve static pages.  
Hello "Buster"

#### Publishing

Switch directory to "Files", the sub-folder under Blog.  
Your new repo address must be handy,

In the new folder run `buster setup` this command prompts for the repo address, below is a sample.Replace "username" with yours and hit enter.

`https://github.com/username/username.github.io.git`

Once this is done, all you need to run to generate the statics pages is

`buster generate —domain=http://127.0.0.1:2368 && buster deploy`

This pushes latest changes to Github, and voila you now have a website.

Bear in mind, you need to run `buster generate —domain=http://127.0.0.1:2368 && buster deploy` after every edit, to push to Github (public). You can view your changes locally,at `localhost:2368` before pushing to Github.

**Workflow**

1.  Change your directory to Ghost directory
    *   Run `npm start` in your terminal
2.  Open `localhost:2368` in browser
3.  Edit and/or write post, tweak settings
4.  Save
5.  Change directory to Files

*   run `buster generate —domain=http://127.0.0.1:2368`  
    and `buster deploy`

6.  Done

**Repeat 5 - 6 after each post, to generate and publish to Github**