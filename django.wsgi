import os, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_store.settings")

path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)

import app_store.monitor
app_store.monitor.start(interval=1.0)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
