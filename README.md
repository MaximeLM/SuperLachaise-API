# superlachaise_api

### [api.superlachaise.fr](https://api.superlachaise.fr)

A touristic database and API for cemeteries, continuously updated by OpenStreetMap and Wikimedia contributors. Currently used for the Père-Lachaise cemetery in Paris.

## Usage

TODO ; see [api.superlachaise.fr](https://api.superlachaise.fr) for examples

## Installation

Required :

 * [python 2.7](https://www.python.org)
 * [django 1.9](https://www.djangoproject.com)
 * [pip](https://pypi.python.org/pypi/pip)
 * git
 * a database
 
Recommended :

 * [virtualenv](https://pypi.python.org/pypi/virtualenv)

### Create the django project

Open a directory in a terminal window and create a new django project (don't call it *superlachaise_api*) :

```sh
django-admin startproject <project_name>
```

Move into the directory that was created and use git to clone the application :

```sh
cd <project_name>
git clone https://github.com/MaximeLM/superlachaise_api.git
```

(optional) Create and activate a new virtual environment ([documentation](https://virtualenv.pypa.io/en/latest/userguide.html)) :

```sh
virtualenv <env_name>
. <env_name>/bin/activate
```

Install Python dependencies :

```sh
pip install -r superlachaise_api/requirements.txt
```

### Configure the project

Edit the settings file *project_name/settings.py* :

 * Add *'superlachaise_api',* to **INSTALLED_APPS**
 * Make sure that *'django.contrib.admin',* and *'django.contrib.messages',* are listed in **INSTALLED_APPS**
 * Configure **DATABASES** with your database info ([documentation](https://docs.djangoproject.com/en/1.9/ref/settings/#databases))
 * Set **LANGUAGE_CODE** and **TIME_ZONE** to your locale e.g. *'fr-FR'* and *'Europe/Paris'*. The admin interface is available in english and french.
 * Copy, paste and edit the following settings at the end of the file :

```python
# User agent header added to mediawiki requests ; see https://meta.wikimedia.org/wiki/User-Agent_policy
# Synchronisation may fail if this setting is empty
MEDIAWIKI_USER_AGENT = ''

# Send an email to managers at the end of the sync_all operation
EMAIL_ENABLED = False
EMAIL_HOST = 'smpt.example.com'
EMAIL_PORT = 587      # or something else
EMAIL_USE_SSL = False # TLS and SSL are mutually exclusive
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = '[SuperLachaise API] '
SERVER_EMAIL = 'from@example.com'
EMAIL_HOST_USER = 'user@example.com'
EMAIL_HOST_PASSWORD = 'password'

# The list of managers who should receive synchronisation updates by email
MANAGERS = (
    ('Manager 1', 'manager1@example.com',),
    ('Manager 2', 'manager2@example.com',),
)

# Dump the database at the end of the sync_all operation
DUMP_DATABASE = False
DATABASE_DUMP_NAME = 'superlachaise_database.json'
DATABASE_DUMP_DIR = '/home/user/superlachaise_api_/database/'

# Commit the database dump ; there must be a git repo in DATABASE_DUMP_DIR
COMMIT_DATABASE_DUMP_DIR = False
COMMIT_DATABASE_DUMP_MESSAGE = '[SuperLachaise API] Dump database'
COMMIT_DATABASE_DUMP_PUSH = False
COMMIT_DATABASE_DUMP_REMOTE_NAME = 'origin'

```

Edit the URLs file *project_name/urls.py* and include the application URLs in *urlpatterns* :

```
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('superlachaise_api.urls')),
]
```

### Initialize data

Create the database structure, configuration objects, and super user :

```sh
python manage.py migrate
python manage.py load_configuration
python manage.py createsuperuser
```

### Connect to the admin interface

Start the developement server :

```sh
cd <project_path>
python manage.py runserver
```

Open the admin interface in a browser (http://yoursite.com/admin/ or [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)) and log in with the user created before.

The application is now ready to synchronize data and serve requests.

 * Go to the **Settings** and **Synchronizations** screens to begin synchronising data.
 * The API is located at http://yoursite.com/api/

## Administration

TODO
