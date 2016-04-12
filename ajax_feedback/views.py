from django.views.generic import FormView
from django.http import HttpResponseNotAllowed
from django.conf import settings
from ajax_feedback.forms import get_form_class
from ajax_feedback.send_email import SendEmail

from ajax_feedback.conf import AJAX_FEEDBACK_SETTINGS


class ContactFormView(FormView):
    template_name = AJAX_FEEDBACK_SETTINGS.get('form_template')

    def post(self, request, *args, **kwargs):
        return super(ContactFormView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])

    def form_valid(self, form):
        sender = SendEmail(self.request)
        try:
            sender.send(form.cleaned_data)
        except:
            if settings.DEBUG:
                raise
            return form.result(False, {'__all__': AJAX_FEEDBACK_SETTINGS.get('failed_message')})

        return form.result(True, AJAX_FEEDBACK_SETTINGS.get('success_message'))

    def form_invalid(self, form):
        return form.result(False, form.get_form_errors())

    def get_form_kwargs(self):
        kwargs = super(ContactFormView, self).get_form_kwargs()
        username = self.request.user.get_username()
        sender_name_field = AJAX_FEEDBACK_SETTINGS.get('sender_name_field')
        sender_email_field = AJAX_FEEDBACK_SETTINGS.get('sender_email_field')
        if not kwargs['initial'].get(sender_name_field) and username:
            kwargs['initial'][sender_name_field] = username
            kwargs['initial'][sender_email_field] = self.request.user.email
        return kwargs

    def get_form_class(self):
        return get_form_class(self.request)
