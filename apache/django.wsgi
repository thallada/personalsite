import os
import sys

sys.path.append('/home/tyler/workspace/')
sys.path.append('/home/tyler/workspace/personalsite/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'personalsite.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
