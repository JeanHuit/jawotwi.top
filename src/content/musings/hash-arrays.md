---
title: "Hash Arrays"
date: 2020-04-06T01:16:26Z
cover: /images/hash.png
draft: false
description: "Working with hash arrays in Ruby, specifically traversing nested structures from Google Maps API."
author: "Jean Huit"
category: "Development"
tags: ["ruby", "hash", "arrays", "api", "google maps"]
keywords: ["ruby", "hash", "arrays", "api", "google maps"]
excerpt: "Man got stuck working with Google matric Api to determine distance, duration of travel etc from two points on the map."
---
Man got stuck working with Google matric Api to determine distance, duration of travel etc from two points on the map.
<!--more-->
values the api spat out was a jumble of hash values that took me a while to understand how to traverse it.

```ruby

matrix = 
{
  "destination_addresses":["Egypt Rd, Accra, Ghana"],
  "origin_addresses":["8 Third Dade Walk, Accra, Ghana"],
  "rows":
  [
    {"elements":
      [
        {
          "distance":
          {
            "text":"5.0 km",
            "value":5047
            },
          "duration":
          {
            "text":"12 mins",
            "value":734
            },
            "status": "OK"
            }
              ]
               }
              ],
              "status":"OK"
              }
```

Ever wondered how to traverse an array/hash like this?
code snippet below will output :  ``` "5.0km" ```

``` matrix[:rows][0][:elements][0][:distance][:text]```

Think on it !!