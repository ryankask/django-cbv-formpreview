======================
django-cbv-formpreview
======================

Usage
-----

I will write better documentation shortly, but for now see Django's
documentation on its `version of this class
<https://docs.djangoproject.com/en/dev/ref/contrib/formtools/form-preview/>`_.

This project is just a fork `Django's FormPreview
<https://code.djangoproject.com/browser/django/trunk/django/contrib/formtools/preview.py>`_
class. There are a few basic differences when using
django-cbv-formpreview's version of the class:

1. Specify the form you wish to use by setting ``form_class`` on your
   subclass. This is instead of constructing a ``FormPreview`` with
   the form class (i.e. don't do ``MyFormPreview(MyForm)``)
2. Include it in your URLconf just as you would a normal class-based
   view (i.e. ``MyFormPreview.as_view()``)
3. You still need to override the ``done`` method, but it only takes a
   cleaned ``form`` as an argument. Django's version takes an
   ``HttpRequest`` object and the form's ``cleaned_data``. Like all
   class-based views, the current ``HttpRequest`` is available as an
   instance attribute (i.e. ``self.request``).
4. The ``process_preview`` method is still there, but it takes a
   ``form`` and the ``context`` it will pass to the template. It is no
   longer passed an ``HttpRequest`` object for the same reason as
   above.

Along with the above backwards incompatibile changes that affect
publicly documented behavior, a comment in the source code
suggested a few methods that might be useful to override. The methods
``get_initial``, ``security_hash``, and ``failed_hash`` used to take
an ``HttpRequest`` as an argument but no longer do for the same
reason stated above. A few other changes to note:

- ``process_params`` has been removed. The ``args`` and ``kwargs``
  passed to the view are available as instance attributes with the same
  names. If you need to do something with them before the view is
  processed, override ``dispatch`` and be sure to return a call to the
  parents ``dispatch`` method (i.e. ``return super(MyFormPreview,
  self).dispatch(request, *args, **kwargs)``.
- ``get_auto_id`` has also been removed. Override ``get_form_kwargs``
  if you need it.

Please let me know if I've missed anything.

Background
----------

The ``FormPreview`` class from the ``contrib.formtools`` app is a
class based view that's been in Django for over 5 years. Originally
written by Adrian Holovaty, it hasn't changed significantly since its
release.

Starting in version 1.3, Django has a "blessed" version of class based
views. This package contains an updated version of ``FormPreview``
that inherits from the new ``FormView`` class. This enables a
consistent API for class based views in Django. Of particular
use are the methods provided by the ``FormMixin`` class, from which
``FormView`` inherits. For example, the ``get_form`` method gives you
control over the instantiation of the form class. This allows you to
construct an instance with non-standard arguments which was the
original motivation of the patch.

I originally strove for backwards compatibility but after using this
in production, decided it wasn't worth it. The final straw was when
I needed to call the ``save`` method on a form in ``done``. Django's
``FormPreview`` only passed ``cleaned_data`` and I didn't want to
reconstruct the form as recleaning it would unnecessarily hit the
database.

I previously filed a `ticket <https://code.djangoproject.com/ticket/16174>`_
on Django's trac to include the original backwards compatibile version
of ``django-cbv-formpreview`` in Django 1.4. Now that I've broken
backwards compatibility, I'm not sure how the core devs will respond
to it. I personally feel that few people actually use this
functionality and would therefore have minimal impact on the community.
