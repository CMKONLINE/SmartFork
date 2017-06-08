#!/usr/bin/eval PYTHON_VERSION=2.7 DJANGO_VERSION=1.8.1 python
import os, site, sys

site.addsitedir("/home/smartfork/.virtualenvs/myprojectenv/lib/python2.7/site-packages/")
_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PROJECT_DIR)
sys.path.insert(0, os.path.dirname(_PROJECT_DIR))

_PROJECT_NAME = _PROJECT_DIR.split('/')[-1]
os.environ['DJANGO_SETTINGS_MODULE'] = "smartfork.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
