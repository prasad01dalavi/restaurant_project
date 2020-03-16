# Restaurant Project
Flask Microservices

## Installation
```
# Install required Pythogn Packages
pip install -r requirements.txt

# Connect Flask Models to Mysql Database
1. Go into the Interpreter and run the following commands to get tables in restaurant_db:
from app import db
db.create_all()
```

## Credentials
We need following credentials:
```
1. Github Tokens
Github > setting > Developer Setting > OAuth Apps > New App 
Set Home Page Url: http://127.0.0.1:5000
Authorization callback URL: http://127.0.0.1:5000/github_login/github

2. Mysql Credentials in app.py file

3. Email username and password in email_notification.py file
```
