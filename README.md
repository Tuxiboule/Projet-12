# TITLE CRM EPic Event
![](icon.png)

## About
Epic Events is an event consulting and management company catering to the needs of startups aiming to organize "epic parties." Epic Events aims to equip itself with an internal secure CRM (Customer Relationship Management) system.

## Features
The application will manage a database to securely store and manipulate client information, as well as contracts and events organized by Epic Events. The application operates via command line interface. The principle of least privilege is applied when granting data access.

Different permissions are summarized in this table (docs/permissions.pdf).
## Usage
This locally executable application can be installed using pipenv by following the steps described below.

If you prefer to use pip instead of pipenv, you have the requirements.txt file available to install all project dependencies. You will then need to activate the virtual environment manually (in this case, remove "pipenv" or "pipenv run" from all commands).

1. Clone the repository
```
git clone https://github.com/Tuxiboule/Projet-12
```
2. Rename config_helper.ini in config.ini and provide the required information.
Make sure you created a database named epic_events [DOC](https://www.pgadmin.org/docs/pgadmin4/development/database_dialog.html)
3. Open terminal in the app folder, install dependencies and launch virtual env
```
pipenv install
pipenv shell
```
4. Initiate database and create first user with
```
python reset_db.py
```
5. Launch app with 
```
python main.py
```



## Context - Develop a secure back-end architecture with Python and SQL
First project with an ORM that is not Django.
I struggled to choose the right tools to use, but once started, I really enjoyed creating this project.

## Skills
Front :
- Rich display

Back : 
- SQLAlchemy
- Postgresql
- JW Token
- Sentry


## Credits
[Tuxiboule](https://github.com/Tuxiboule)
