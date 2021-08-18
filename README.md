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