#!/usr/bin/env python
import os
import sys

from django.conf import settings

if not settings.configured:
    databases = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
    settings.configure(
        DATABASES=databases,
        ROOT_URLCONF='cbv_formpreview.tests.urls',
        INSTALLED_APPS=('cbv_formpreview', 'cbv_formpreview.tests')
    )

from django.test.simple import DjangoTestSuiteRunner

def runtests(*test_args):
    parent = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
    sys.path.insert(0, parent)
    test_runner = DjangoTestSuiteRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(test_args)
    sys.exit(failures)

if __name__ == '__main__':
    runtests(*sys.argv[1:])
