from __future__ import unicode_literals

import sys
import django
from django.conf import settings
import logging
log = logging.getLogger()
log.setLevel(10)

import traceback

def log_traceback(ex, ex_traceback=None):
    if ex_traceback is None:
        ex_traceback = ex.__traceback__
    tb_lines = [ line.rstrip('\n') for line in
                 traceback.format_exception(ex.__class__, ex, ex_traceback)]
    exception_logger.log(tb_lines)

if __name__ == '__main__':
    settings.configure(
        DEBUG = True,
        DATABASES = {
                'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        INSTALLED_APPS = (
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'shopify_sync',
        ),
        MIDDLEWARE_CLASSES = (),
        ROOT_URLCONF = 'shopify_sync.tests.urls',
        USE_TZ = True,
        SHOPIFY_APP_API_SECRET = 'hush',
        log = log,
    )

    django.setup()

    from django.test.runner import DiscoverRunner

    test_runner = DiscoverRunner()
    failures = test_runner.run_tests(['shopify_sync'])
    if failures:
        sys.exit(failures)
