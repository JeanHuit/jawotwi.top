---
title: "Github : Codeship :Firebase Hosting "
date: 2018-06-05T12:13:20Z
draft: false
---

<section class="post-content">
            <p>If  <code>free</code>  is a requirement to hosting your code amidst running a continuous integration and delivery setup. You have come to the right place.</p>
<p>This here, is a short tutorial to making this come true.<br>
Need to understand git? check this <a href="https://github.com/GDGAccra/CrashCourseWeb/wiki/Git-Resources">here</a></p>
<p>The defualt mode of hosting for free on firebase, will be to develop locally and then push directly to firebase - hosting.<br>
However, this will work if you are the only developer.</p>
<p>In the scenario where, you have a team of developers,as is usually the case, you will need to bring in the middleman, <a href="https://codeship.com/"><strong>codeship</strong></a> or another of its like.</p>
<p>Setting up and connecting to your github/bitbucket/gitlab repository is as simple as abc. I will skip all that and bring you to the meat of the equation.</p>
<p>For Codeship to push/deploy your code to firebase-hosting, it will need to login as the owner of the firebase account. To do this, codeship will need a token which you will generate in your terminal.</p>
<p><strong>ps</strong>: You need to have firebase-cli installed to do this.<br>
<code>npm install -g firebase-tools</code></p>
<p>Next you login via the terminal <code>firebase login:ci</code><br>
You will be redirected to your browser to login with the required gmail address and its password. After a succeful login, a token  "in this case a string of text" will be generated and display in the terminal.<br>
Keep this safe.</p>
<p>Running  <code>firebase list</code> gives you the list of projects you have running on/created on firebase and the names you gave them. Keep the name of this project in mind.</p>
<p>By now, you might have completed the creation of your project on codeship.<br>
Just to be sure:</p>
<ul>
<li>create account/login to codeship</li>
<li>click on  <strong>new project</strong></li>
<li>connect to your repository</li>
<li>select codeship <strong>pro</strong> or <strong>basic</strong></li>
</ul>
<p>If you skipped the configure projects, you can find that under project settings. Select the <strong>ENVIRONMENT</strong> tab.<br>
Under Environement Variable, type in <code>FIREBASE_TOKEN</code> as the KEY and then paste the token you initially generated into the VALUE field. Click Save or Add or +</p>
<p>Click on the <strong>Test</strong> tab,<br>
Select, the option to run your own commands and in the space for setup commands type in:</p>
<pre><code>nvm install &lt;verison number&gt;  
#eg. nvm install v6.9.5
#to install that particular version of node


npm install -g firebase-tools
#to install the firebase tools

firebase deploy --token "$FIREBASE_TOKEN" --project "&lt;project name&gt;"

#to deploy your project with the token you generated and saved #as an envrionment variable and the project name

</code></pre>
<p>save changes and that should be all. Make a commit to your repo, and you should see codeship kick-in and do the rest.</p>
<p>All <strong>should</strong> be green and good.</p>

        </section>