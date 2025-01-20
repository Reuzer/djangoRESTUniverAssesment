""""
module string
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kursach3sem.settings')

application = get_wsgi_application()
