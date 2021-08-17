# BoxBusiness
### Django SetUp
- Adapt and run the [commands](commands.txt)
### MySQL Database
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
```console
pip3 install coverage
coverage run manage.py test -v 2 && coverage report && coverage html
```
Inspect in the browser:
```~/projects/web/django/src/htmlcov/index.html```