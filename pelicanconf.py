#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Cameron MacLeod'
SITENAME = u'Cameron MacLeod'
SITEURL = ''

PATH = 'content'
OUTPUT_PATH = 'develop-output'

THEME='pelican-hyde'

PROFILE_IMAGE='profile.jpg'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'

GOOGLE_ANALYTICS = 'UA-76310908-1'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

PAGE_URL = "{slug}.html"
PAGE_SAVE_AS = "{slug}.html"
ARTICLE_URL = "blog/{slug}"
ARTICLE_SAVE_AS = "blog/{slug}.html"

# Blogroll
LINKS = (('About', '/about'),
         ('CV', '/cv.pdf'),
         ('Projects', '/projects'),)

# Social widget
SOCIAL = (('twitter', 'http://twitter.com/notexactlyawe'),
        ('linkedin', 'https://uk.linkedin.com/in/cameronjohnmacleod'),
        ('github', 'https://github.com/notexactlyawe'),
        ('flickr', 'https://www.flickr.com/photos/rotor132'))

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
