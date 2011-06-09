import os
from setuptools import setup, find_packages

version = '0.1.0a1'

readme = open(os.path.join(os.path.dirname(__file__), 'README.md'))
long_description = readme.read()
readme.close()

setup(
    name='django-cbv-formpreview',
    version=version,
    author='Ryan Kaskel',
    author_email='dev@ryankaskel.com',
    url='https://github.com/ryankask/django-cbv-formpreview',
    description='Django\'s FormPreview updated to use class based views.',
    long_description=long_description,
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    test_suite='cbv_formpreview.tests.runtests.runtests'
)
