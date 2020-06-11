---
title: "Making MySQL Accessible remotely"
date: 2020-06-10T22:37:25Z
draft: false
---

#### Os: Ubuntu Server 20.04

If you ever find yourself unable to log-in or connect to your newly created MySQL server, with errors such as these being thrown around,

```
- Host ''xxx.xx.xxx.xxx'' is not allowed to connect to this MySQL server
- Unknown authentication method
- Port closed
```
You have come to the right place

**Assumption: mysql server is already installed.

1. Log into your server and connect to the DB using the root account.
```sudo mysql -u <user> -p <enter password at prompt>```
2. check for available account on the DB
```SELECT user,authentication_string,plugin,host FROM mysql.user;```
3. Create a new user if not present or alter existing user with the following commands
```mysql
(creates user to connect via the internet & localhost)
- CREATE USER 'user'@'%' IDENTIFIED WITH mysql_native_password IDENTIFIED BY 'password';
- CREATE USER 'user'@'localhost' IDENTIFIED WITH mysql_native_password IDENTIFIED BY 'password';
- GRANT ALL PRIVILEGES ON *.* TO 'user'@'%' WITH GRANT OPTION;
- GRANT ALL PRIVILEGES ON *.* TO 'user'@'localhost' WITH GRANT OPTION;
- FLUSH PRIVILEGES;
```
or

```mysql
(Alters existing users)
- ALTER USER 'user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
- ALTER USER 'ruser'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
- GRANT ALL PRIVILEGES ON *.* TO 'user'@'%' WITH GRANT OPTION;
- GRANT ALL PRIVILEGES ON *.* TO 'user'@'localhost' WITH GRANT OPTION;
- FLUSH PRIVILEGES;
```
4. Exit mysql ```exit```
5. Enable firewall (ufw) and allow port 3306 through
```bash
ufw enable
ufw allow 3306
```
If you have a specific IP you will be connecting from (safest),
```bash
ufw enable
ufw allow from remote_IP_address to any port 3306
```
6. Mysql must listen for an external IP address or all addresses(not safe). To enable this, open up your ```mysqld.cnf file```:
```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

7. Scroll down till you reach ```bind-address            = 127.0.0.1```
Edit ```127.0.0.1``` to specific IP mysql should listen for or to ```0.0.0.0``` for everyone(not safe)
8. Uncomment ```#port = 3306``` if it is commented.
9. Save the document and restart mysql ```sudo systemctl restart mysql```

Now you can connect to your DB, using your new user and the password via the internet.