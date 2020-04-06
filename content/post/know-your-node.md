---
title: "Know Your Node"
date: 2016-11-10T12:22:07Z
draft: false
---
Hi there,

Yes, you. The period of silence on this blog has been loud.

Anyways, I am back with some sort of motivation to continue to update this blog.

This post is a quick one.

How do you know which node you are using? To the developer, that'd be a simple question. just do `node -v` right?

Well yes!  
But then have you ever encountered a particular project with its own set of node version different from yours? Most especially when the difference in version raises a whole lot of issues and yet, you still want to keep your version....

In walks the Node Version Manager or **"NVM"**.  
With the Manager, you get to have multiple versions of node on your local development machine. Now, I'd just like to speak on the **n** manager. Obviously, like node it self there are many managers our there. I have no special reason for installing **n**, just like that its not as mouthful as **NVM**.

We will be using [homebrew](http://brew.sh/) to install "n"

    -> brew install n
    -> n <latest | stable | 6.9>
    -> n #can be used to select version you will want to use
    
    

et voila!