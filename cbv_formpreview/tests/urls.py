from django.conf.urls.defaults import patterns, url

from cbv_formpreview.tests.tests import TestFormPreview

urlpatterns = patterns('',
    url(r'^preview/', TestFormPreview.as_view(), name='preview')
)
