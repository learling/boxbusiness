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

**AWS RDS SSL**:
-> Security Group - Inbound rules <-
| IP version | Type         | Protocol | Port range | Source    |
|------------|--------------|----------|------------|-----------|
| IPv4       | MYSQL/Aurora | TCP      | 3306       | 0.0.0.0/0 |
| IPv6       | MYSQL/Aurora | TCP      | 3306       | ::/0      |

Open a separate mysql-session:
```console
sudo apt install mysql-client-core-8.0
wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
cp global-bundle.pem ~/projects/web/django/src/boxbusiness
mysql -h dbname.ffffffffffff.eu-west-1.rds.amazonaws.com \
 --ssl-ca=global-bundle.pem -P 3306 -u masterusername -p
```
```settings.py```:
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
Open a second shell to verify encryption:
```console
sudo tcpdump -X port 3306
```
In the first shell, create a superuser and you should not be able to capture any SQL in the second shell:
```console
python3 manage.py createsuperuser
```
The app requires groups, so add them in the mysql-session:
```sql
INSERT INTO `auth_group` (`id`, `name`) VALUES
(1, 'admin'),
(2, 'customer');
```
**DB-testing-problem**:
Currently test-workflows cannot run in parallel because they share the same test-database.
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
sudo apt install -y docker docker-compose
sudo apt install -y certbot
sudo apt install -y git
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
Generate the free certificate (here for *ivanne.de*):
```console
cd ~/projects/web/django/scripts
sudo chmod +x certdomain.sh
sudo ./certdomain.sh ivanne.de
```
Automate the daily (midnight) renewal (```sudo``` is important):
```console
sudo crontab -e
```
Remember to adapt the domain-name:
```bash
DJSCRIPTS=/home/shell/projects/web/django/scripts
0 0 * * * chmod +x $DJSCRIPTS/certdomain.sh && $DJSCRIPTS/certdomain.sh ivanne.de > /var/log/certdomain.log 2>&1
```
To check the logfile:
```console
cat /var/log/certdomain.log
```
### Container-test
For the ```functional_tests```, 2GB RAM are ***not*** enough!
They work with 2 vCPUs and 4GB RAM (check it with ```htop``` in a parallel SSH-session).
```console
cd ~/projects/web/django/
sudo docker-compose -f docker-compose-test.yml up --build
```
### Server
Start with the default ports (don't forget to adapt the domain-name, otherwise you could get a 400-status):
```console
export HTTP=80
export HTTPS=443
export DOMAIN=ivanne.de
sudo -E docker-compose -p stack1 up -d --build
```
To seamlessly update the project, temporarily run ```stack2``` with different ports - before killing ```stack1```:
```console
git pull
export HTTP=8080
export HTTPS=8443
export DOMAIN=ivanne.de
sudo -E docker-compose -p stack2 up -d --build
```
Refer to the [firewall-settings](scripts/iptables-export) and add these rules:
```console
sudo iptables -A PREROUTING -t nat -i eth0 -p tcp \
 --dport 443 -j REDIRECT --to-port 8443
sudo iptables -A PREROUTING -t nat -i eth0 -p tcp \
 --dport 80 -j REDIRECT --to-port 8443
sudo iptables -A INPUT -i eth0 -p tcp -m tcp \
 --dport 8443 -j ACCEPT
```
To undo an added rule, replace ```-A``` into ```-D```. 
To clean up Docker:
```console
sudo docker ps -a
sudo docker rm -f <container1> [<container2>]
sudo docker system prune
```
If Compose is complaining (?) - somehow:
```console
sudo aa-remove-unknown
```
### Release
Create new tag:
```console
export TAG=$(date +DEPLOYED-%F-%H-%M)
git tag $TAG
git push origin $TAG
```
Delete old tag:
```console
git tag -l
git tag -d <tagname>
git push --delete origin <tagname>
```