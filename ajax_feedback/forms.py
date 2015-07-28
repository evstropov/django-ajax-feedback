import json
from django import forms
from django.http import HttpResponse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.module_loading import import_string


class AjaxFormMixin(forms.Form):

    @classmethod
    def render_to_json_response(cls, context):
        return cls.get_json_response(cls.convert_context_to_json(context))

    @staticmethod
    def get_json_response(content, **httpresponse_kwargs):
        return HttpResponse(content, content_type='application/json', **httpresponse_kwargs)

    @staticmethod
    def convert_context_to_json(context):
        return json.dumps(context)

    def get_form_errors(self):
        if not self.prefix:
            return self.errors
        prefixed_errors = {}
        for k, v in self.errors.iteritems():
            prefixed_errors[self.prefix + '-' + k] = v
        return prefixed_errors

    def result(self, status, data):
        return self.render_to_json_response({'status': status, 'data': data})


class BaseForm(AjaxFormMixin):
    name = forms.CharField(label=_('Your Name'), max_length=64)
    email = forms.EmailField(label=_('E-mail'), max_length=100)
    message = forms.CharField(label=_('Message'),
                              max_length=getattr(settings, 'AJAX_FEEDBACK_MESSAGE_MAX_LEN', 500),
                              widget=forms.Textarea())


if getattr(settings, 'AJAX_FEEDBACK_FORM', False):
    ContactForm = import_string(settings.AJAX_FEEDBACK_FORM)
else:
    ContactForm = BaseForm


class AuthContactForm(ContactForm):
    name = forms.CharField(label=_('Your Name'), max_length=64, widget=forms.HiddenInput)


if getattr(settings, 'AJAX_FEEDBACK_CAPTCHA', False):
    from captcha.fields import ReCaptchaField

    class GuestContactForm(ContactForm):
        captcha = ReCaptchaField(label='')
else:
    class GuestContactForm(ContactForm):
        pass
