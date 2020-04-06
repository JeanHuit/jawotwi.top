---
title: "Hosting a Simple Sinatra App on Heroku"
date: 2019-02-12T13:56:16Z
draft: false
---

## [https://passg.herokuapp.com](https://passg.herokuapp.com) is the sinatra app on heroku.

### This is how it got there.
-----

- First Create an account, or sign-in to an already existing account.

- Create an app.

  - In my scenario, I connected to github from where I deploy my app, whenever there is a push to the master branch of my repo.

- You will need a `Gemfile` , `Gemfile.lock`, `Config.ru`

- Using `touch Gemfile` in your terminal should create a Gemfile for you.
  - In this Gemfile, list  out the gems that you will want installed with your app. eg.

  ```ruby
  # Gemfile

  source "https://rubygems.org"
  gem "sinatra"
  gem "sinatra-contrib"
  ```
- Run `bundle install` in the same directory with the Gemfile and this will create for you, `Gemfile.lock`. **Note:** The bundler gem would have to be installed to do this. `gem install bundler`
**Note:** Heroku requires bundler version 2.

- In your `Config.ru` file,

```ruby
# Config.ru

require './main'
# ./main refers to  "main.rb"

run Sinatra::Application
```

- With this, your app is ready to deploy.

- You might encounter an issue,after you deploy to heroku, especially with Heroku's bunder version.
- The defualt buildpack does not come with bundler version 2. To solve this, visit your heroku dashboard, under settings, add this buildpack to your apps settings.
`https://github.com/bundler/heroku-buildpack-bundler2`
Remove the default ruby buildpack, you should be ready to go then