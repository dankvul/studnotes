# Studnotes
A modern tool for students

# How to run 
### 1. Install virtualenv
### 2. Create virtualenv and activate it
### 3. Install requirements using ```pip install -r requirements.txt``` 
### 4. Initialize db 
```
(venv) studnotes/$ export FLASK_APP=app.py
(venv) studnotes/$ flask db install
(venv) studnotes/$ flask db upgrade
(venv) studnotes/$ flask db migrate
```
### 5. Run app ;) 
```(venv) studnotes/$> flask run```
