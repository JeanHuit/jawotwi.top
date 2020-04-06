---
title: "The Move to Firebase"
date: 2017-12-14T12:57:25Z
draft: false
---

For some reason, I just do not remmeber why, I decided to find out if my one off blog could find another home.

For two years, this blog has been squatting living for free on github and before that blogger.

Today, I'm proud to say, what begun as:  
_[http://bustlive.blogspot.com](http://bustlive.blogspot.com)_ --> _[http://jeanhuit.github.io](http://jeanhuit.github.io)_ and then to _[http://johnawotwi.me](http://johnawotwi.me)_ is now _[https://johnawotwi.me](https://johnawotwi.me)_ .  
New digs and all, notice the extra (s) in there..yuh, that is all for free.

See [Ghost Adventures](https://johnawotwi.me/ghost-adventures-i/) for the initial steps, especially the update.

All you will need to replace is the part about github. Instead of hosting and setting up a git repo, get a free account and setup a free project 'static sites' only at `console.firebase.google.com`  
Install the firebase CLI (command line interface), login,initialize the project folder, select your static output folder and then deploy.

Obviously, [you should know your node](https://johnawotwi.me/know-your-node/) first.

*   install the firebase tools

    npm install -g firebase-tools 
    

*   provide your credentials, popup opens a browser

    firebase login 
    

    cd <project folder>
    

*   initialize the project, select the kind of project, hosting

    firebase init
    

*   select path to folder for static pages

    firebase deploy
    

et voila!!!
===========