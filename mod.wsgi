
import os, sys
sys.path.append('D:\\OpenServer\\domains\\tangotest')
sys.path.append('D:\\OpenServer\\domains\\virtualenv\\tango\\Lib\\site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'tangotest.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()




