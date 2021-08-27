![workflow](https://github.com/learling/boxbusiness/actions/workflows/django.yml/badge.svg)
---
**DISCLAIMER**: This is just an experimental project for learning purposes only.
---
# BoxBusiness
### Django SetUp
- Make sure Python 3 is installed: ```which python3```
- Read and adapt the Ubuntu [commands](setup/commands.txt)
### MySQL-Database
Edit ```.env``` and ```settings.py``` as described in the [comments](src/boxbusiness/__init__.py)

**AWS RDS SSL**
```console
sudo apt install mysql-client-core-8.0
wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
cp global-bundle.pem ~/projects/web/django/src/boxbusiness
mysql -h dbname.ffffffffffff.eu-west-1.rds.amazonaws.com \
 --ssl-ca=global-bundle.pem -P 3306 -u masterusername -p
```
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'PASSWORD': env('DB_PASSWORD'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_ALL_TABLES'",
            'ssl': {
                'key': 'global-bundle.pem'
            }
        }
    }
}
```
Add the bunch of Django-tables (e.g. *auth_user*):
```console
~/projects/web/django
source bin/activate
cd src
python3 manage.py migrate
```
Open a second shell to assert encryption:
```console
sudo tcpdump -X port 3306
```
In the first shell, create a superuser and you should not be able to capture any SQL in the second shell:
```console
python3 manage.py createsuperuser
```
### VCS with GitHub
```console
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin git@github.com:learling/boxbusiness.git
git push -u origin main
```
### Test coverage
Edit ```.coveragerc``` and run:
```console
coverage run manage.py test -v 2 && coverage report && coverage html
```
Inspect: ```~/projects/web/django/src/htmlcov/index.html```
## Deployment
First try with [YT-tutorial](https://www.youtube.com/watch?v=nh1ynJGJuT8) from 
*London App Developer*:

See commits [Prepare deployment with docker](https://github.com/learling/boxbusiness/commit/1da4daf036c6dd41abaf2e9e7e878cf490c3aad9)
### Installation
On the VPS, install Docker, Docker Compose, Certbot and Git:
```console
sudo apt update
sudo apt install docker docker-compose
sudo apt install certbot
sudo apt install git
```
```console
mkdir -p ~/projects/web/django
cd ~/projects/web/django
git init
git remote add origin git@github.com:learling/boxbusiness.git
```
Create key-pair in the default path:
```console
ssh-keygen -t rsa
```
Show the **public** key to copy and paste it into https://github.com/settings/key:
```console
cat ~/.ssh/id_rsa.pub
```
Fetch the current repo and switch to the main branch:
```console
git fetch
git checkout main
```
Paste the content of ```.env``` here:
```console
touch ~/projects/web/django/src/boxbusiness/.env
nano ~/projects/web/django/src/boxbusiness/.env
```
### Certificate
Generate the free certificate:
```console
cd ~/projects/web/django/scripts
sudo chmod +x certdomain.sh 
sudo ./certdomain.sh dev.ivanne.de
```
Automate the daily renewal (```sudo``` is important):
```console
sudo crontab -e
```
```bash
DJSCRIPTS=/home/shell/projects/web/django/scripts
0 0 * * * chmod +x $DJSCRIPTS/certdomain.sh && $DJSCRIPTS/certdomain.sh dev.ivanne.de > /var/log/certdomain.log 2>&1
```
Check the logfile:
```console
cat /var/log/certdomain.log
```
### Server
Start with the default ports:
```console
cd ~/projects/web/django/
export HTTP=80
export HTTPS=443
sudo -E docker-compose -f docker-compose-deploy.yml \
 -p stack1 up -d --build
```
To seamlessly update the project, start ```stack2``` with different ports before killing ```stack1```:
```console
git pull
export HTTP=8080
export HTTPS=8443
sudo -E docker-compose -f docker-compose-deploy.yml \
 -p stack2 up -d --build
sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j \
 REDIRECT --to-ports 8080
sudo iptables -A PREROUTING -t nat -p tcp --dport 443 -j \
 REDIRECT --to-ports 8443
sudo iptables -t nat -A OUTPUT -o lo -p tcp --dport 80 -j \
 REDIRECT --to-port 8080
sudo iptables -t nat -A OUTPUT -o lo -p tcp --dport 443 -j \
 REDIRECT --to-port 8443
```
To clean up Docker:
```console
sudo docker system prune
```
If Compose is complaining:
```console
sudo aa-remove-unknown
```
If a port is already allocated:
```console
sudo docker-compose down
sudo docker ps -a
sudo docker rm -f <container> [<other-container>]
sudo kill -9 <pid>
```
### Release
Delete old tag:
```console
git tag -l
git tag -d <tagname>
git push --delete origin <tagname>
```
Create new tag:
```console
export TAG=$(date +DEPLOYED-%F-%H-%M)
git tag $TAG
git push origin $TAG
```