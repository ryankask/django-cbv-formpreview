======================
django-cbv-formpreview
======================

The ``FormPreview`` class from the ``contrib.formtools`` app is a class based view that's been in Django for over 5 years. Originally written by Adrian Holovaty, it hasn't changed significantly since its release.

Starting in version 1.3, Django has a "blessed" version of class based views. This package contains an updated version of ``FormPreview`` that inherits from the new ``FormView`` class. This enables a consistent API for class based views in Django but also mantains 100% compatibility with ``FormPreview`` as it is `found in Django 1.3 <https://code.djangoproject.com/browser/django/tags/releases/1.3/django/contrib/formtools/preview.py>`_. Of particular use are the methods provided by the ``FormMixin`` class, from which ``FormView`` inherits. For example, the ``get_form`` method gives you control over the instantiation of the form class. This allows you to construct an instance with non-standard arguments which was the original motivation of the patch.

I've filed a `ticket <https://code.djangoproject.com/ticket/16174>`_ on Django's trac to include these changes in Django 1.4.

Note that this package is just a modified version of ``FormPreview`` currently in Django packaged for ease of use on `Languagelab.com <http://www.languagelab.com>`_. For the authors of the Django project, see its `AUTHORS file <https://code.djangoproject.com/browser/django/trunk/AUTHORS>`_.
