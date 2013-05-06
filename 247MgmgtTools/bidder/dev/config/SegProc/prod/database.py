"""
Keep Track of all mysql queries.
Do not put True for production environment.
  /!\ WARNING /!\ DEBUG=True leads to a constant increase of memory usage.
"""
DEBUG = False

"""
Database settings
"""

ORACLE = {
    'default': {
        'ENGINE': 'oracle',
        'NAME': 'ZTUS',
        'USER': 'GP_SCHEDULER',
        'PASSWORD': '46lN4B6fEsBv4Bn',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'threaded': True,
            'use_returning_into': False,
            },
        }
    }

MYSQL = {
    'default': {
        'ENGINE': 'mysql',
        'NAME': 'gps_db',
        'USER': 'root',
        'PASSWORD': 'mypw',
        'HOST': '',
        'PORT': '',
        }
    }

DATABASES = ORACLE


"""
Django ORM special settings.
Do not modify
"""
INSTALLED_APPS = ('Sched.core',
                  'django.contrib.auth',
                  'django.contrib.contenttypes',)


TIME_ZONE = None
