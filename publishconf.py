#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://markphilpot.com'
RELATIVE_URLS = False

FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
FEED_MAX_ITEMS = 100

CATEGORY_SAVE_AS = 'category/{slug}/index.html'

DELETE_OUTPUT_DIRECTORY = True

PLUGINS.append('optimize_images')

# Weird TypeError
TYPOGRIFY = False

DEBUG = False
SHOW_DRAFTS = False
