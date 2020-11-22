# INSTALL_TESTIFY 


### Setup

clone repository:
```
git clone https://gitlab.com/UlrichKh/testify.git
```
move to folder "testify":
```
cd testify
```

### install docker:


```
sudo apt update -y
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable" -y
sudo apt update -y
apt-cache policy docker-ce
sudo apt install docker-ce -y
sudo usermod -aG docker ${USER}
su - ${USER}
id -nG
sudo usermod -aG docker ubuntu
```

### install docker-compose:

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### set up environment


create a file ".env" 
```
touch .env
```
and fill in the file as in the example ".env.example", but with your own settings. Where "xxxx" you need to change to your settings (use "nano .env" to edit this file)


### run app

run:

```
docker-compose up
```

you need to collect staticfiles:
```
docker-compose exec backend python manage.py collectstatic
```
and media:
```
docker-compose exec backend cp -r media/ /var/www/testify/media
```
you need to create database:
```
docker-compose exec postgresql bash
```
next step:
```
su - postgres
```
next step:
```
psql
```
next step (you can create your own user, change password and other data):
```
CREATE DATABASE testify; 
CREATE USER testify_admin WITH PASSWORD 'xxxx';
ALTER ROLE testify_admin SET client_encoding TO 'utf8';
ALTER ROLE testify_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE testify_admin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE testify TO testify_admin;
ALTER USER testify_admin CREATEDB;

```
return in to folder "testify" (use combination of keys "ctrl + d" 3 times)

you need to add your changed data in ".env" file (use nano .env) 

you shout make migration:
```
docker-compose exec backend python manage.py migrate
```

### Finish

Congratulation! You can use it 
