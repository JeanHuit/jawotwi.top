---
title: "Hash Arrays"
date: 2020-04-06T01:16:26Z
draft: false
---
```

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

```
  matrix[:rows][0][:elements][0][:distance][:text]

```

Think on it !!