#!/usr/bin/env python
import os
import sys

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASE_ENGINE='sqlite3',
        ROOT_URLCONF='cbv_formpreview.tests.urls',
        INSTALLED_APPS=('cbv_formpreview', 'cbv_formpreview.tests')
    )

from django.test.simple import run_tests

def runtests(*test_args):
    parent = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
    sys.path.insert(0, parent)
    failures = run_tests(test_args, verbosity=1, interactive=True)
    sys.exit(failures)

if __name__ == '__main__':
    runtests(*sys.argv[1:])
