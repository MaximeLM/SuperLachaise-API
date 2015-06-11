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

```
django-admin startproject <project_name>
```

Move into the directory that was created and use git to clone the application :

```
cd <project_name>
git clone https://github.com/MaximeLM/superlachaise_api.git
```

(optional) Create and activate a new virtual environment ([documentation](https://virtualenv.pypa.io/en/latest/userguide.html)) :

```
virtualenv <env_name>
. <env_name>/bin/activate
```

Install Python dependencies :

```
pip install -r superlachaise_api/requirements.txt
```

### Configure the project

Edit the settings file *&lt;project\_name>/settings.py* :

 * Add *'django.contrib.sites',* to **INSTALLED_APPS**
 * Configure **DATABASES** with your database info ([documentation](https://docs.djangoproject.com/en/1.8/ref/settings/#databases))
 * Set **LANGUAGE\_CODE** and **TIME\_ZONE** to your locale e.g. *'fr-FR'* and *'Europe/Paris'*
 * Copy, paste and edit the following settings :

```
&#35; User agent header added to mediawiki requests ; see https://meta.wikimedia.org/wiki/User-Agent_policy
&#35; Synchronisation may be blocked if this setting is empty
MEDIAWIKI\_USER\_AGENT = ''  
&#35; Uncomment and edit to enable email updates about object synchronisation
'''
&#35; SMTP
EMAIL\_HOST = 'smpt.example.com'
EMAIL\_HOST\_USER = 'user@example.com'
EMAIL\_HOST\_PASSWORD = 'password'
EMAIL\_USE\_TLS = True
EMAIL\_USE\_SSL = False &#35; TLS and SSL are mutually exclusive
EMAIL\_PORT = 587      &#35; or something else  
EMAIL\_SUBJECT\_PREFIX = '[SuperLachaise API] '
SERVER\_EMAIL = 'from@example.com'  
&#35; The list of managers who should receive object synchronisation updates
MANAGERS = (
    ('Manager 1', 'manager1@example.com',),
    ('Manager 2', 'manager2@example.com',),
)
'''  
&#35; Identifier of the django site
SITE\_ID = 1
```

### Initialize data

Create the database structure, configuration objects, and super user :

```
cd <project_path>
python manage.py migrate
./superlachaise_api/configuration/load_configuration.sh
python manage.py createsuperuser
```

### Connect to the admin interface

Start the developement server :

```
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
