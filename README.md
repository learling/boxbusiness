![workflow](https://github.com/learling/boxbusiness/actions/workflows/django.yml/badge.svg)
---
**DISCLAIMER**: This is just an experimental project for learning purposes only.
---
# BoxBusiness
### Django SetUp
- Make sure Python 3 is installed: ```which python3```
- To install the exact same package-versions, try:
```pip3 install -r requirements.txt```
- Read and adapt the Ubuntu [commands](setup/commands.txt)
- Run the first [functional tests](src/functional_tests.py)
### MySQL-Database
Edit ```.env``` and ```settings.py``` as described in the [comments](src/boxbusiness/__init__.py)
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
### Server

Install Docker, Compose and Git:

```console
sudo apt update
sudo apt docker docker-compose
sudo apt install git
```
```console
mkdir -p ~/projects/web/django
cd ~/projects/web/django
git init
git remote add origin git@github.com:learling/boxbusiness.git
```
Create key-pair into the default path:
```console
ssh-keygen -t rsa
```
Show the **public** key to copy and paste into https://github.com/settings/key:
```console
cat ~/.ssh/id_rsa.pub
```
Fetch and switch to main branch:
```console
git fetch
git checkout main
```
Paste the content of ```.env```:
```console
touch ~/projects/web/django/src/boxbusiness/.env
nano ~/projects/web/django/src/boxbusiness/.env
```
Start the server in production-mode (remove -d to see the logs):
```console
sudo docker-compose -f \
 docker-compose-deploy.yml up --build -d
```
To update:
```console
git pull
```
To clean up:
```console
sudo docker system prune
```
### Certificate
Create/Renew certificate:
```console
shell@ubuntu-2gb-fsn1-1:~/projects/web/django/scripts$ sudo chmod +x certdomain.sh 
shell@ubuntu-2gb-fsn1-1:~/projects/web/django/scripts$ sudo ./certdomain.sh dev.ivanne.de
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator standalone, Installer None
Cert not yet due for renewal
Keeping the existing certificate

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Certificate not yet due for renewal; no action taken.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
```
Automate daily renewal (sudo is important):
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
### Release
Delete tag:
```console
git tag -l
git tag -d <tagname>
git push --delete origin <tagname>
```
Create tag:
```console
export TAG=$(date +DEPLOYED-%F-%H-%M)
git tag $TAG
git push origin $TAG
```