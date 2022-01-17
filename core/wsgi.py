# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os,sys

sys.path.append('home/ubuntu/django/myproject/')
sys.path.append('home/ubuntu/django/myprojectenv/lib/python3.8/site-packages')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
