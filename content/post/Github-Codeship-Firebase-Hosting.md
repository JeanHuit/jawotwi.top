---
title: "Github : Codeship :Firebase Hosting "
date: 2018-06-05T12:13:20Z
draft: false
---

If `free` is a requirement to hosting your code amidst running a continuous integration and delivery setup. You have come to the right place.

This here, is a short tutorial to making this come true.  
Need to understand git? check this [here](https://github.com/GDGAccra/CrashCourseWeb/wiki/Git-Resources)

The defualt mode of hosting for free on firebase, will be to develop locally and then push directly to firebase - hosting.  
However, this will work if you are the only developer.

In the scenario where, you have a team of developers,as is usually the case, you will need to bring in the middleman, [**codeship**](https://codeship.com/) or another of its like.

Setting up and connecting to your github/bitbucket/gitlab repository is as simple as abc. I will skip all that and bring you to the meat of the equation.

For Codeship to push/deploy your code to firebase-hosting, it will need to login as the owner of the firebase account. To do this, codeship will need a token which you will generate in your terminal.

**ps**: You need to have firebase-cli installed to do this.  
`npm install -g firebase-tools`

Next you login via the terminal `firebase login:ci`  
You will be redirected to your browser to login with the required gmail address and its password. After a succeful login, a token "in this case a string of text" will be generated and display in the terminal.  
Keep this safe.

Running `firebase list` gives you the list of projects you have running on/created on firebase and the names you gave them. Keep the name of this project in mind.

By now, you might have completed the creation of your project on codeship.  
Just to be sure:

*   create account/login to codeship
*   click on **new project**
*   connect to your repository
*   select codeship **pro** or **basic**

If you skipped the configure projects, you can find that under project settings. Select the **ENVIRONMENT** tab.  
Under Environement Variable, type in `FIREBASE_TOKEN` as the KEY and then paste the token you initially generated into the VALUE field. Click Save or Add or +

Click on the **Test** tab,  
Select, the option to run your own commands and in the space for setup commands type in:

    nvm install <verison number>  
    #eg. nvm install v6.9.5
    #to install that particular version of node
    
    
    npm install -g firebase-tools
    #to install the firebase tools
    
    firebase deploy --token "$FIREBASE_TOKEN" --project "<project name>"
    
    #to deploy your project with the token you generated and saved #as an envrionment variable and the project name
    
    

save changes and that should be all. Make a commit to your repo, and you should see codeship kick-in and do the rest.

All **should** be green and good.