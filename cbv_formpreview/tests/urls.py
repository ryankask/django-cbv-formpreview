from django.conf.urls.defaults import patterns, url

from cbv_formpreview.tests.tests import (
    TestForm,
    TestFormPreview
)

urlpatterns = patterns('',
    url(r'^preview/', TestFormPreview(TestForm)),
)
