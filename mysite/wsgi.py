"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
import site

from django.core.wsgi import get_wsgi_application
from os.path import join,dirname,abspath
PROJECT_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0,PROJECT_DIR)

site.addsitedir('/home/caicai/python/my-blog/myvenv/lib/python3.5/site-packages')
sys.path.append('/home/caicai/python/my-blog/media')
sys.path.append('/home/cai')
sys.path.append('/home/caicai/python/my-blog')
sys.path.append('/home/caicai/python/my-blog/myvenv')
sys.path.append('/home/caicai/python/my-blog/myvenv/lib/python3.5')
sys.path.append('/home/caicai/python/my-blog/mysite')
sys.path.append('/home/caicai/python/my-blog/myvenv/lib/python3.5/site-packages')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = get_wsgi_application()
