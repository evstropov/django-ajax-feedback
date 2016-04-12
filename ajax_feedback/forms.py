#!encoding=utf-8
from __future__ import unicode_literals

from django import forms
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.utils.module_loading import import_string

from ajax_feedback.conf import AJAX_FEEDBACK_SETTINGS


class AjaxFormMixin(forms.Form):

    def get_form_errors(self):
        if not self.prefix:
            return self.errors
        prefixed_errors = {}
        for k, v in self.errors.iteritems():
            prefixed_errors[self.prefix + '-' + k] = v
        return prefixed_errors

    @staticmethod
    def result(status, data):
        return JsonResponse({'status': status, 'data': data})


class BaseContactForm(AjaxFormMixin):
    name = forms.CharField(label=_('Your Name'), max_length=64)
    email = forms.EmailField(label=_('E-mail'), max_length=100)
    message = forms.CharField(label=_('Message'),
                              max_length=AJAX_FEEDBACK_SETTINGS.get('message_max_length'),
                              widget=forms.Textarea())


ContactForm = import_string(AJAX_FEEDBACK_SETTINGS.get('form'))


class AuthContactForm(ContactForm):
    name = forms.CharField(label=_('Your Name'), max_length=64, widget=forms.HiddenInput)


if AJAX_FEEDBACK_SETTINGS.get('recaptcha'):
    try:
        from captcha.fields import ReCaptchaField
    except ImportError:
        raise ImportError('Please install and configure django-recaptcha')

    class GuestContactForm(ContactForm):
        captcha = ReCaptchaField(label='')
else:
    class GuestContactForm(ContactForm):
        pass


def get_form_class(request):
    if request.user.is_authenticated():
        return AuthContactForm
    else:
        return GuestContactForm
