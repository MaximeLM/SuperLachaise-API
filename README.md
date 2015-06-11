# superlachaise_api

### [api.superlachaise.fr](https://api.superlachaise.fr)

A touristic database and API for cemeteries, continuously updated by OpenStreetMap and Wikimedia contributors. Currently used for the Père-Lachaise cemetery in Paris.

## Usage

TODO ; see [api.superlachaise.fr](https://api.superlachaise.fr) for examples

## Installation

Required :

 * [python 2.7](https://www.python.org)
 * [django 1.8](https://www.djangoproject.com)
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

Edit the settings file *<project_name>/settings.py* :

 * Add *'django.contrib.sites',* and *'superlachaise_api',* to **INSTALLED_APPS**
 * Configure **DATABASES** with your database info ([documentation](https://docs.djangoproject.com/en/1.8/ref/settings/#databases))
 * Set **LANGUAGE_CODE** and **TIME_ZONE** to your locale e.g. *'fr-FR'* and *'Europe/Paris'*
 * Copy, paste and edit the following settings :

```python
# User agent header added to mediawiki requests ; see https://meta.wikimedia.org/wiki/User-Agent_policy
# Synchronisation may be blocked if this setting is empty
MEDIAWIKI_USER_AGENT = ''

# Identifier of the django site
SITE_ID = 1

# Uncomment and edit to enable email updates about object synchronisation
'''
# SMTP
EMAIL_HOST = 'smpt.example.com'
EMAIL_HOST_USER = 'user@example.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False &#35; TLS and SSL are mutually exclusive
EMAIL_PORT = 587      &#35; or something else

EMAIL_SUBJECT_PREFIX = '[SuperLachaise API] '
SERVER_EMAIL = 'from@example.com'

# The list of managers who should receive object synchronisation updates
MANAGERS = (
    ('Manager 1', 'manager1@example.com',),
    ('Manager 2', 'manager2@example.com',),
)
'''
```

### Initialize data

Create the database structure, configuration objects, and super user :

```sh
cd <project_path>
python manage.py migrate
./superlachaise_api/configuration/load_configuration.sh
python manage.py createsuperuser
```

### Connect to the admin interface

Start the developement server :

```sh
cd <project_path>
python manage.py runserver
```

Open the admin interface in a browser (http://yoursite.com/admin or [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)) and log in with the user created before.

Edit the default **Site** entry :

 * Click the **Sites** link on the admin home page
 * Click on the default entry *http://example.com* to edit it
 * Replace the domain name by the URL of your django application ('http://127.0.0.1:8000' for localhost)
 * Click the *save* button

Go to the **Admin commands** and **Settings** screens to begin synchronising data.

## Administration

TODO
