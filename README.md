![example workflow](https://github.com/learling/boxbusiness/actions/workflows/django.yml/badge.svg)
# BoxBusiness
### Django SetUp
- Make sure Python 3 is installed: ```which python3```
- To install the exact same package-versions, try:
```pip3 install -r requirements.txt```
- Read and adapt the Ubuntu [commands](commands.txt)
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
Show the **public** key to copy and paste intohttps://github.com/settings/key:
```console
cat ~/.ssh/id_rsa.pub
```
Fetch+merge and switch to main branch:

```console
git fetch
git checkout main
```
Start the server in production-mode:
```console
sudo docker-compose -f \
 docker-compose-deploy.yml up --build -d
```