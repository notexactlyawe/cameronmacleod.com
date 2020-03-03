#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

PATH = 'content'
OUTPUT_PATH = 'notexactlyawe.github.io'

GOOGLE_ANALYTICS = 'UA-76310908-1'

# only use all.atom.xml
FEED_ALL_ATOM = 'feeds/all.atom.xml'

SITEURL = 'https://www.cameronmacleod.com'
RELATIVE_URLS = False

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
