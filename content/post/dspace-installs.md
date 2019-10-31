---
title: "Dspace Installs"
date: 2019-10-30T15:15:28Z
draft: false
---
I have spent over three weeks in trying to get dspace set up. It has been one helluva ride. Finally got it working somewhat on a windows OS and wanted to document the process for posterity sake.

### What is DSpace?

DSpace is an open source repository software package typically used for creating open access repositories for scholarly and/or published digital content. While DSpace shares some feature overlap with content management systems and document management systems, the DSpace repository software serves a specific need as a digital archives system, focused on the long-term storage, access and preservation of digital content. - [Wikipedia reference](https://en.wikipedia.org/wiki/DSpace)

To get this working, you need:

- Apache Ant
- Apache Maven
- Apache Tomcat
- Postgresql
- Java JDK
- DSpace src-release

Funny enough, only certain specific versions get to work well with each other.

- Apache Ant v1.9.9
- Apache Maven v3.3.9
- Apache Tomcat v9.0.0.m18
- Postgresql v9.6.4-1
- Java JDK v8u121
- DSpace src-release v6.1
- postgresql admin interface (pgadmin v3 or v4)

This magic formula was concocted by [Dr. Santosh Gupta](https://www.youtube.com/watch?v=I-lmBHp6pDE)

Even in the comments peopole give him praise.

### Installation

- Install Java: Get your environment variables working, so ``java -verion`` works in the command line
- Install Apache ant & maven, this is usually simplified by extracting them from their respective zip or tar archives and placing them in the root of your drive, say "C:/"
  - Setup your environmental variables (sytemwide path) that points to the bin directories where ant and maven are stored.
- Create variables JAVA_HOME, ANT_HOME under environmental variables (user) and point these to the main directories.
- Install tomcat, this you can get as an executable.
- Install postrgresql and pgadmin.
  - Start up the postgresql db and add a new login ``name =  dspace``
  - passwords are yours to choose.
  - under role priviledges, simply turn all on for user dspace
  - Add a new database, ``name = dspace``  and ``owner = dspace``
  - set tablespace to the default pg_default.
  - Add pg_crypto under extensions.
  - DB should be connected and active.

- Extract the dspace src- release zip file into the root directory.

- Open up the commandline
  - test your environmental variables
    - ``ant vesion`` &  ``java version``
  - Navigate into the  **dspace** folder in  dspace-6.1-src-release folder
  - run ``mvn package`` , make sure you have a working internet connection
  - after the download and installation of various packages are done.
  - navigate into the config folder  and locate a **local.cfg** file, scroll through said file and change the db password there. default will be dspace. Also change the installation directory  to ``C:/dspace``
  - Now create a dspace folder in your root
  - Navigate into dspace-6.1-src-release > dspace > target >dspace_installer
  - Run ``ant fresh_install``
  - Navigate into the bin folder of the newly created dspace folder at your root directory ``c:\dspace\bin``
  - Run `` dspace create-administrator`` to create an admin, follow the requirements.
  - Copy ``jspui`` , ``xmlui`` & ``solr `` from the webapps folder in the new dspace installation to the webapps folder of your tomcat installation.
  - open your web browser and point it to ``localhost:8080\jspui`` for your dspace installation.

The end (For windows installations)