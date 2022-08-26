Quick reference for how to make a website with django, following [Django's tutorial](https://docs.djangoproject.com/en/4.1/intro/tutorial01/).

## Dependencies
- System-wide: ```docker```, ```python3```, ```django```
- Installed in project's python virtual environment: ```django```, ```psycopg2```
- Recommended (project python venv): ```wheel```, ```pylint```, ```redgreenunittest```

## To create project
#### Create project directory
1. ```django-admin startproject app``` (use "app", "base", or "config" instead of project name to avoid django's default of nesting a directory with the same name, and allow hyphens in project name. See [discussion on django forums](https://perma.cc/E2XF-CKZD))
1. rename project directory to [project name]
#### In project directory, set up python virtual environment and install django
1. ```python3 -m venv env``` (Create venv)
1. ```source env/bin/activate``` (Activate venv)
1. ```pip install django``` (Install django in venv)
#### Set up postgres database with docker-compose
1. Make *docker-compose.yml* in project directory, specifying default database name (e.g., ```postgres_dev```) ([Template](https://gist.github.com/opmorgan/155c8b8ee8a6a68247bad2829800c4ec))
1. Run docker.service (depends on: ```docker```)
1. ```sudo docker-compose up``` (compose database; keep this process running while developing)
1. (Later, set up a separate databse for production)
#### Hook up postgres database to django
1. Open *app/settings.py*
1. Set ```DATABASES``` to match docker-compose.yml ([Template](https://gist.github.com/opmorgan/aac753bf769b14b5c4a9ff4b14f2c660))
1. ```python manage.py migrate```(Make initial migrations)
#### Run server in venv
1. ```pip install psycopg2```
1. ```python manage.py runserver```
1. Preview site in browser at localhost:8000 (runserver's default port)

## To set up testing environment, for existing project
1. ```sudo docker compose up``` (Run the docker container)
2. ```source env/bin/activate``` (Enter python virutal environment)
3. ```python manage.py runserver```
4. Preview site in browser at localhost:8000

## To make model changes and migrations
1. Change models (models.py)
2. Run ```python manage.py makemigrations``` to create migrations for those changes
3. Run ```python manage.py migrate``` to apply those changes to the database.

## To install linter and test-output colorizer, in venv
1. ```pip install pylint```
1. ```pip install redgreenunittest```
1. In *app/settings.py*, add: ```TEST_RUNNER="redgreenunittest.django.runner.RedGreenDiscoverRunner"```

## Make admin user and modify database through admin interface
1. ```python manage.py createsuperuser```
1. Navigate to admin site: localhost:8000/admin
1. Make the app modifiable by admin, by adding to *[app name]/admin.py*:
```
from django.contrib import admin
from .models import [ModelName]
admin.site.register([ModelName])
```

