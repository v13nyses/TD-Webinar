# -*- coding: utf-8 -*-
# Django settings for basic pinax project.

import os.path
import posixpath
import pinax
import logging

PINAX_ROOT = os.path.abspath(os.path.dirname(pinax.__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# tells Pinax to use the default theme
PINAX_THEME = 'default'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# tells Pinax to serve media through django.views.static.serve.
SERVE_MEDIA = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'dev.db'       # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Vancouver'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'site_media', 'media')

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/site_media/media/'

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'site_media', 'static')

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
STATIC_URL = '/site_media/static/'

# Additional directories which hold static files
STATICFILES_DIRS = (
    ('TD-Webinar', os.path.join(PROJECT_ROOT, 'media')),
    ('pinax', os.path.join(PINAX_ROOT, 'media', PINAX_THEME)),
)

GEOIP_PATH = 'apps/geoip/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

# Make this unique, and don't share it with anybody.
#
# This one was from the old version, so it's here just in case
#SECRET_KEY = 'v&_tt0it07k1!cnh+q*sohvifutnp2i^uta+!1v4)&lxg8^1p3'
SECRET_KEY = 'lt@ugf^nzsbb3lchr3fmzn%_gn^ue(2ukd&mpp#0oyfe7&^^#x'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_openid.consumer.SessionConsumer',
    'account.middleware.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'pinax.middleware.security.HideSensistiveFieldsMiddleware',
)

ROOT_URLCONF = 'TD-Webinar.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates"),
    os.path.join(PINAX_ROOT, "templates", PINAX_THEME),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    
    "pinax.core.context_processors.pinax_settings",
    
    "notification.context_processors.notification",
    #"announcements.context_processors.site_wide_announcements",
    "account.context_processors.openid",
    "account.context_processors.account",
)

INSTALLED_APPS = (
    # TD-Webinar
    'events',
    'presentations',
    'polls',
    'dashboard',
    'form_utils',
    'django_extensions',
    'reporting',
    'registration',
		'userprofiles',
    'exitsurvey',
    'eventmailer',
    'sorl.thumbnail',
    #'autofixture',
    # included
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.humanize',
    'pinax.templatetags',
    
    # external
    'notification', # must be first
    #'django_openid',
    'emailconfirmation',
    'mailer',
    'announcements',
    'pagination',
    #'timezones',
    'ajax_validation',
    #'uni_form',
    'staticfiles',
    
    # internal (for now)
    'basic_profiles',
    'account',
    #'signup_codes',
    #'about',
    'django.contrib.admin',

)

FIXTURE_DIRS = (
  'events/fixtures',
  'userprofiles/fixtures',
  #'presentations/fixtures',
  'exitsurvey/fixtures',
  'fixtures'
)

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/profiles/profile/%s/" % o.username,
}

MARKUP_FILTER_FALLBACK = 'none'
MARKUP_CHOICES = (
    ('restructuredtext', u'reStructuredText'),
    ('textile', u'Textile'),
    ('markdown', u'Markdown'),
    ('creole', u'Creole'),
)
WIKI_MARKUP_CHOICES = MARKUP_CHOICES

AUTH_PROFILE_MODULE = 'basic_profiles.Profile'
NOTIFICATION_LANGUAGE_MODULE = 'account.Account'

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_VERIFICATION = False

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG
CONTACT_EMAIL = "feedback@example.com"
SITE_NAME = "Pinax"
LOGIN_URL = "/account/login/"
LOGIN_REDIRECT_URLNAME = "what_next"

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'v13nyses@gmail.com'
EMAIL_HOST_PASSWORD = 's34nandl1nds3y'
DEFAULT_FROM_EMAIL = 'v13nyses@gmail.com'
SERVER_EMAIL = 'v13nyses@gmail.com'
EMAIL_USE_TLS = True

# TD Webinar Specific Settings
EVENT_SLUG_WORDS = 4 # the number of words to use when creating an event 'slug'
EVENT_SLUG_CHARS = 25
VIDEO_URL = "http://content.bitsontherun.com/players/%s-%s.js"

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass

# sorl-thumbnail settings
THUMBNAIL_DEBUG = True

# eventmailer
#MAILCHIMP_API_KEY = "a9bd7260067c1faf8f2e52268b8cd855-us2"
MAILCHIMP_API_KEY = "4a6f04fce75f55d03cae2c46ecb2fc43-us1"
#MAILCHIMP_LIST_ID = '68a096ab69'
MAILCHIMP_LIST_ID = '4970ced8ae'
MAILCHIMP_SUBJECTS = {
    'reminder': 'Reminder! {event} starts in {time}',
    'finished_thank_you': 'Thank you for participating',
    'finished_sorry_we_missed': 'Sorry we missed you'
}
MAILCHIMP_FROM_EMAIL = "v13inc@gmail.com"
MAILCHIMP_FROM_NAME = "Sean"
MAILCHIMP_TO_EMAIL = "Event Members"
WELCOME_EMAIL_SUBJECT = 'Thank you for registering for {event}, {first_name}!'
REGISTRATION_MESSAGE = 'Thank you for registering.'
SITE_URL = 'http://event.blinkmediaworks.com'

# logging
if not hasattr(logging, "set_up_done"):
  logging.set_up_done = True
  logging.basicConfig(level = logging.INFO)
  logging.basicConfig(file_name = "letstry.log")
