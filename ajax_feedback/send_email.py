from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.template.loader import render_to_string

from ajax_feedback.conf import AJAX_FEEDBACK_SETTINGS


class SendEmail:
    def __init__(self, request):
        self.settings = AJAX_FEEDBACK_SETTINGS
        self.site_name = get_current_site(request)

    def create_email(self, form_data):
        recipient_list = AJAX_FEEDBACK_SETTINGS.get('recipient_list')
        from_email = '%s <%s>' % (form_data.get(self.settings.get('sender_name_field')), settings.DEFAULT_FROM_EMAIL)
        subject = self.get_subject(form_data)
        body = self.get_body(form_data)
        headers = self.get_headers(form_data)
        return EmailMessage(subject, body, from_email, recipient_list, headers=headers)

    def send(self, form_data, fail_silently=False):
        self.create_email(form_data).send(fail_silently=fail_silently)

    def get_subject(self, form_data):
        form_data.update(site_name=self.site_name)
        string = render_to_string(self.settings.get('subject_template'), form_data)
        return string.strip()

    def get_body(self, form_data):
        form_data.update(site_name=self.site_name)
        string = render_to_string(self.settings.get('message_template'), form_data)
        return string.lstrip()

    def get_headers(self, form_data):
        return {'Reply-To': '%s <%s>' % (form_data.get(self.settings.get('sender_name_field')),
                                         form_data.get(self.settings.get('sender_email_field')))}
