#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Cameron MacLeod'
SITENAME = u'Cameron MacLeod'
SITEURL = ''

PATH = 'content'
OUTPUT_PATH = 'notexactlyawe.github.io'

THEME='pelican-hyde'

PROFILE_IMAGE='profile.jpg'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('twitter', 'http://twitter.com/notexactlyawe'),
        ('linkedin', 'https://uk.linkedin.com/in/cameronjohnmacleod'),
        ('github', 'https://github.com/notexactlyawe'))

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
