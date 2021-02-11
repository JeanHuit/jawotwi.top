---
title: "Heroku Ruby App"
date: 2021-02-11T12:27:33Z
draft: false
---

In my bid to host my ruby based telegram bot on heroku, I had to jump through hoops due to the fact that my bot was not using webhooks but the polling alternative. 

This required that I run a script to initiate the bot. This also meant that my bot had no web interface. 

Most important 
`REMEMBER TO SET ENV VARIABLES IN HEROKU'S CONFIG VAR`

Add a `Procfile` to the root of your app.

Sample Procfile:

```
  bot: bundle exec ruby app.rb
```

Make sure you have installed Heroku's CLI. Run the following command:
`heroku ps:scale bot=1 -a <appname>`

Note here that 'bot' here is same and similar to  'bot' in the procfile

and 

` heroku run bundle exec ruby <app.rb> -a <appname>`

Thats it. This should get you going?