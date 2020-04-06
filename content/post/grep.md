---
title: "Grep"
date: 2017-09-02T12:20:27Z
draft: false
---
Another linux command, I find very useful, this is a command that helps you search for strings/text within documents. There are a whole lot of uses for it, but I will leave you to explore that yourself.

Its simplest form is:

    grep <word> <in file>
    => grep "dog" animals.txt
    

The above looks for dog in a text file called animal.txt

There are flags/options you can set with the command to make things easier.

     -x = exclusive, exact match
     -v = everything but
     -i = I do not care about case
    

and many more.

You can also use \[\] and ^ to help make your search more refined.

    grep ^a* fruits.txt
    

Finds fruits that have a in them

     grep ^a.p fruits.txt
    

Finds fruits that begin with an a and followed a random letter and then by a p.

    grep ^[a-p] fruits.txt
    

Find all text that begin with an a through to P in fruits.txt  
Go ahead and play with grep!

Lastly, grep can search through huge files very quickly, and outputs can be overwhelming, eg. log files. To make it easier, and this can be used for most linux commands,you can pipe commands through each other.

    ps aux | grep 'root'| less
    

This simply means, I am looking for root in the output of `ps aux` but due to the volume outputted, I want to see them in pages, thus the use of `less`.

Go ahead and play with grep. Fun times ahead.