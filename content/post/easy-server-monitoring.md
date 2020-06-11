---
title: "Easy Server Monitoring"
date: 2020-06-11T07:31:49Z
draft: false
---

Discovered a simple script that allows you to monitor your server in a quick glance.

Found here: https://www.ezservermonitor.com/esm-sh/documentation

Comes with a web version as well if you are so inclined. 

I opted for the bash script for its simplicity especially with dependencies; None.

One issue I came across was an error in the script due to the fact that it was written on a windows platform.
```
Bad interpreter: No Such File ^M
```

Solution: ```sed -i -e 's/\r$//' <scriptname.sh>```

Others sugest rewriting the whole script in your unix environment.
Others still, suggest you use [dos2unix](http://dos2unix.sourceforge.net/)