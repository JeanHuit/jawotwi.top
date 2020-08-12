---
title: "Dspace III"
date: 2020-06-29T06:36:08Z
draft: false
---


Installing Dspace on Digital Ocean. Using Ubuntu 18.04
Install the needed tools with these comnands.

```
   sudo apt-get install openjdk-8-jdk -y
   sudo apt-get install ant ant-optional maven -y
   sudo apt-get install tomcat8 -y
```

Edit the tomcat config files here:

```
sudo nano /etc/default/tomcat8
```

Uncomment **#AUTHBIND=no** and change to **AUTHBIND=yes**

Edit the JAVA_OPTS to match the line below. This will help with Memory mangement issues. ```JAVA_OPTS="${JAVA_OPTS} -Djava.security.egd=file:/dev/./urandom -Djava.awt.headless=true -Xmx512m -XX:MaxPermSize=256m -XX:+UseConcMarkSweepGC"```

Run the follow commands to sort out binding ports from the default 8080 to 80.

```
sudo touch /etc/authbind/byport/80 
sudo touch /etc/authbind/byport/443 
sudo chmod 0755 /etc/authbind/byport/80 
sudo chmod 0755 /etc/authbind/byport/443 
sudo chown tomcat8.tomcat8 /etc/authbind/byport/80 
sudo chown tomcat8.tomcat8 /etc/authbind/byport/443 
```

Run the code below to confirm if the change above has taken place
```
ls -lh /etc/authbind/byport/
```
Your output to the above commant should match these:

```
-rwxr-xr-x 1 otuoma otuoma 0 Nov 23 09:42 443 
-rwxr-xr-x 1 otuoma otuoma 0 Nov 23 09:42 80 
```

Navigate to the server.xml file below

```
  sudo nano /etc/tomcat8/server.xml 
```
and edit the content of the connector tag to match this:

```
  <Connector port="80" protocol="HTTP/1.1"
               connectionTimeout="20000"
               URIEncoding="UTF-8"
               redirectPort="443" />
```

Add the tomcat user to dspace user group and vice versa, keep in mind, you might not have created the same user 'dspace' as this tutorial.

```
  sudo useradd -m dspace
  sudo passwd dspace
  sudo adduser tomcat8 dspace
  sudo adduser dspace tomcat8
```
Restart tomcat :

```  
sudo service tomcat8 restart 
```


Install & setup the databse

```
  sudo apt-get install postgresql postgresql-contrib libpg-java -y 

```

Setup host based access to the database
Navigate to the pg_hba.conf file.
```
  sudo nano /etc/postgresql/10/main/pg_hba.conf 
```  

and paste this at the bottom.

```
  host    dspace       dspace      127.0.0.1/32         md5 
```
Next, execute the following 3 commands in succession to change database user permissions to "trust" only

```
sudo sed -i 's/ident/trust/' /etc/postgresql/10/main/pg_hba.conf 
sudo sed -i 's/md5/trust/' /etc/postgresql/10/main/pg_hba.conf 
sudo sed -i 's/peer/trust/' /etc/postgresql/10/main/pg_hba.conf 
sudo service postgresql restart
```

Create the dspace database user

```
sudo -i -u postgres
createuser --interactive
```

This will ask a series of questions, in our situation,  **user = dspace**  and  answer yes to make user  a **superuser**

Create a DB as well, in our case named **dspace**
```
createdb dspace
```

Grant permissions to dspace user on dspace database and create the pgcyrpto extension.
```
psql
ALTER ROLE dspace WITH PASSWORD 'db-password-here'; (e.g dspace) 
ALTER DATABASE dspace OWNER TO dspace; 
GRANT ALL PRIVILEGES ON DATABASE dspace TO dspace; 
psql \c dspace
CREATE EXTENSION pgcrypto; 
\q
\q
exit
```

Download and extract Dspace 

```
cd 
mkdir downloads 
cd downloads 
wget https://github.com/DSpace/DSpace/releases/download/dspace-6.3/dspace-6.3-src-release.tar.gz 
tar -zxf dspace-6.3-src-release.tar.gz
```

Run maven package in the dspace directory within the src-release

```
  cd dspace-6.3-src-release/dspace
  mvn package
```
if you experience any issuses with javax not being found, check if the default java jdk is what you installed, digital ocean installs and sets a default java jdk.

```
sudo update-alternatives --config java
```

Set up an environment to point $JAVA_HOME to your installation.

```
sudo nano /etc/environment
$JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64/"

```
exit and run ```source /etc/environment``` nd rerun ```mvn package```.

After a succesful build, navigate into the config folder, create a copy of local.cfg.EXAMPLE and edit
Things to take note of, the  databse username and password, port for solr, from 8080 to 80, because of the changes in ports done above.
Dspace name, etc etc

```
cd target/dspace-installer
cp local.cfg.EXAMPLE local.cfg
sudo nano local.cfg
```

After editing the configuration file, build the dspace by running the following command.

```
  cd target/dspace-installer/
  sudo ant fresh_install
```

After the build,  run the following...to grant dspace ownership rights to the tomcat installation

```
sudo chown -R tomcat8:tomcat8 /dspace 
```

Create admin account by running : ```sudo /dspace/bin/dspace create-administrator ```
Answer the questions that follow.


Copy the files from your installation or point them to the webapps folder of tomcat.

```
cd /var/lib/tomcat8/webapps
sudo cp -r /dspace/webapps/oai/ /var/lib/tomcat8/webapps 
sudo cp -r /dspace/webapps/solr/ /var/lib/tomcat8/webapps 
sudo cp -r /dspace/webapps/sword/ /var/lib/tomcat8/webapps 
sudo cp -r /dspace/webapps/rest/ /var/lib/tomcat8/webapps 
sudo cp -r /dspace/webapps/*    /var/lib/tomcat8/webapp
```

restart tomcat ```sudo service tomcat8 restart ```

Visit: ``localhost:80/jspui`` or ``locahost:80/xmlui`` to see the installation.