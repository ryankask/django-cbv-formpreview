from django.conf import settings
from django.utils.crypto import constant_time_compare
from django.contrib.formtools.utils import form_hmac
from django.views.generic import FormView

PREVIEW_STAGE = 'preview'
POST_STAGE = 'post'
STAGE_FIELD = 'stage'
HASH_FIELD = 'hash'


class FormPreview(FormView):
    preview_template = None
    form_template = None

    def dispatch(self, request, *args, **kwargs):
        self._preview_stage = PREVIEW_STAGE
        self._post_stage = POST_STAGE
        stages = {'1': self._preview_stage, '2': self._post_stage}

        posted_stage = request.POST.get(self.unused_name(STAGE_FIELD))
        self._stage = stages.get(posted_stage, self._preview_stage)

        return super(FormPreview, self).dispatch(request, *args, **kwargs)

    def unused_name(self, name):
        """ Given a first-choice name, adds an underscore to the name until it
        reaches a name that isn't claimed by any field in the form.

        This is calculated rather than being hard-coded so that no field names
        are off-limits for use in the form. """
        while 1:
            try:
                self.form_class.base_fields[name]
            except KeyError:
                break # This field name isn't being used by the form.
            name += '_'
        return name

    def get(self, request, *args, **kwargs):
        self.template_name = self.form_template
        return super(FormPreview, self).get(request, *args, **kwargs)

    def _check_security_hash(self, token, form):
        expected = self.security_hash(form)
        return constant_time_compare(token, expected)

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        hash_field_name = self.unused_name(HASH_FIELD)

        if self._stage == self._preview_stage:
            self.process_preview(form, context)
            context['hash_field'] = hash_field_name
            context['hash_value'] = self.security_hash(form)
            self.template_name = self.preview_template
            return self.render_to_response(context)
        else:
            form_hash = self.request.POST.get(hash_field_name, '')
            if not self._check_security_hash(form_hash, form):
                return self.failed_hash(context) # Security hash failed.
            return self.done(form)

    def form_invalid(self, form):
        self.template_name = self.form_template
        return super(FormPreview, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        kwargs.update({'stage_field': self.unused_name(STAGE_FIELD)})
        return kwargs

    def process_preview(self, form, context):
        """ Given a validated form, performs any extra processing before
        displaying the preview page, and saves any extra data in
        context. """
        pass

    def security_hash(self, form):
        """ Calculates the security hash for the given HttpRequest and
        Form instances.

        Subclasses may want to take into account request-specific information,
        such as the IP address. """
        return form_hmac(form)

    def failed_hash(self, context):
        """ Returns an HttpResponse in the case of an invalid security
        hash. """
        self._stage = self._preview_stage
        return self.post(self.request)

    def done(self, form):
        """ The only method required to be overriden by subclasses. Does
        something with the form and returns an HttpResponseRedirect. """
        msg = 'You must define a done() method on your %s subclass.'
        raise NotImplementedError(msg % self.__class__.__name__)
