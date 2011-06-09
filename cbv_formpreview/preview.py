"""
Formtools Preview application.
"""
from django.conf import settings
from django.shortcuts import render_to_response
from django.utils.crypto import constant_time_compare
from django.contrib.formtools.utils import form_hmac
from django.views.generic import FormView

AUTO_ID = 'formtools_%s' # Each form here uses this as its auto_id parameter.
STAGE_FIELD = 'stage'
HASH_FIELD = 'hash'

class FormPreview(FormView):
    preview_template = 'formtools/preview.html'
    form_template = 'formtools/form.html'

    # METHODS SUBCLASSES SHOULDN'T OVERRIDE ###################################

    def __init__(self, form_class, *args, **kwargs):
        super(FormPreview, self).__init__(*args, **kwargs)
        # form should be a Form class, not an instance.
        self.form_class = form_class
        # A relic from the past; override get_context_data to pass extra context
        # to the template. Left in for backwards compatibility.
        self.state = {}

    def __call__(self, request, *args, **kwargs):
        return self.dispatch(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.preview_stage = 'preview'
        self.post_stage = 'post'
        stages = {'1': self.preview_stage, '2': self.post_stage}

        posted_stage = request.POST.get(self.unused_name(STAGE_FIELD))
        self.stage = stages.get(posted_stage, self.preview_stage)

        # For backwards compatiblity
        self.parse_params(*args, **kwargs)

        return super(FormPreview, self).dispatch(request, *args, **kwargs)

    def unused_name(self, name):
        """
        Given a first-choice name, adds an underscore to the name until it
        reaches a name that isn't claimed by any field in the form.

        This is calculated rather than being hard-coded so that no field names
        are off-limits for use in the form.
        """
        while 1:
            try:
                self.form_class.base_fields[name]
            except KeyError:
                break # This field name isn't being used by the form.
            name += '_'
        return name

    def _get_context_data(self, form):
        """ For backwards compatiblity. """
        context = self.get_context_data()
        context.update(self.get_context(self.request, form))
        return context

    def get(self, request, *args, **kwargs):
        "Displays the form"
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self._get_context_data(form)
        self.template_name = self.form_template
        return self.render_to_response(context)

    def _check_security_hash(self, token, form):
        expected = self.security_hash(self.request, form)
        return constant_time_compare(token, expected)

    def preview_post(self, request):
        """ For backwards compatibility. failed_hash calls this method by
        default. """
        self.stage = self.preview_stage
        return self.post(request)

    def form_valid(self, form):
        context = self._get_context_data(form)
        if self.stage == self.preview_stage:
            self.process_preview(self.request, form, context)
            context['hash_field'] = self.unused_name(HASH_FIELD)
            context['hash_value'] = self.security_hash(self.request, form)
            self.template_name = self.preview_template
            return self.render_to_response(context)
        else:
            form_hash = self.request.POST.get(self.unused_name(HASH_FIELD), '')
            if not self._check_security_hash(form_hash, form):
                return self.failed_hash(self.request) # Security hash failed.
            return self.done(self.request, form.cleaned_data)

    def form_invalid(self, form):
        context = self._get_context_data(form)
        self.template_name = self.form_template
        return render_to_response(context)

    # METHODS SUBCLASSES MIGHT OVERRIDE IF APPROPRIATE ########################

    def get_auto_id(self):
        """
        Hook to override the ``auto_id`` kwarg for the form. Needed when
        rendering two form previews in the same template.
        """
        return AUTO_ID

    def get_initial(self, request=None):
        """
        Takes a request argument and returns a dictionary to pass to the form's
        ``initial`` kwarg when the form is being created from an HTTP get.
        """
        return self.initial

    def get_context(self, request, form):
        "Context for template rendering."
        context = {
            'form': form,
            'stage_field': self.unused_name(STAGE_FIELD),
            'state': self.state
        }
        return context

    def get_form_kwargs(self):
        """ This is overriden to maintain backward compatibility and pass
        the request to get_initial. """
        kwargs = {
            'initial': self.get_initial(self.request),
            'auto_id': self.get_auto_id()
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def parse_params(self, *args, **kwargs):
        """
        Called in dispatch() prior to delegating the request to get() or post().
        Given captured args and kwargs from the URLconf, allows the ability to
        save something on the instance and/or raises Http404 if necessary.

        For example, this URLconf captures a user_id variable:

            (r'^contact/(?P<user_id>\d{1,6})/$', MyFormPreview(MyForm)),

        In this case, the kwargs variable in parse_params would be
        {'user_id': 32} for a request to '/contact/32/'. You can use that
        user_id to make sure it's a valid user and/or save it for later, for
        use in done().
        """
        pass

    def process_preview(self, request, form, context):
        """
        Given a validated form, performs any extra processing before displaying
        the preview page, and saves any extra data in context.
        """
        pass

    def security_hash(self, request, form):
        """
        Calculates the security hash for the given HttpRequest and Form instances.

        Subclasses may want to take into account request-specific information,
        such as the IP address.
        """
        return form_hmac(form)

    def failed_hash(self, request):
        "Returns an HttpResponse in the case of an invalid security hash."
        return self.preview_post(request)

    # METHODS SUBCLASSES MUST OVERRIDE ########################################

    def done(self, request, cleaned_data):
        """
        Does something with the cleaned_data and returns an
        HttpResponseRedirect.
        """
        raise NotImplementedError('You must define a done() method on your %s subclass.' % self.__class__.__name__)
