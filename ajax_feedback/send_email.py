from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template import Context, Template


def _render_template(template, data):
    return Template(template).render(Context(data))


class SendEmail:

    def __init__(self, site_name):
        self.site_name = site_name
        self.subject_title = getattr(settings, 'AJAX_FEEDBACK_SUBJECT', _('Message from website'))
        self.body_template = getattr(settings, 'AJAX_FEEDBACK_BODY_TEMPLATE', '{{ message }}')
        self.subject_template = getattr(settings, 'AJAX_FEEDBACK_SUBJECT_TEMPLATE',
                                        _('{{ site_name }}: {{ subject }} from {{ form_data.name }}'))

    def create_email(self, form_data):
        recipient_list = self.get_recipient_list()
        from_email = self.get_from_email(form_data)
        subject = self.get_subject(form_data)
        body = self.get_body(form_data)
        headers = self.get_headers(form_data)
        return EmailMessage(subject, body, from_email, recipient_list, headers=headers)

    def send(self, form_data, fail_silently=False):
        email = self.create_email(form_data)
        email.send(fail_silently=fail_silently)

    @staticmethod
    def get_recipient_list():
        try:
            return settings.AJAX_FEEDBACK_RECIPIENT_LIST
        except AttributeError:
            raise ImproperlyConfigured('Please provide a AJAX_FEEDBACK_RECIPIENT_LIST')

    @staticmethod
    def get_from_email(form_data):
        return '%s <%s>' % (form_data.get('name'), settings.DEFAULT_FROM_EMAIL)

    def get_subject(self, form_data):
        subject = self.subject_title
        string = _render_template(self.subject_template, {
            'subject': subject,
            'site_name': self.site_name,
            'form_data': form_data
        })
        return string.strip()

    def get_body(self, form_data):
        message = form_data.get('message')
        template = self.body_template
        string = _render_template(template, {
            'message': message,
            'site_name': self.site_name,
            'form_data': form_data,
        })
        return string.lstrip()

    @staticmethod
    def get_headers(form_data):
        reply_to = '%s <%s>' % (form_data.get('name'), form_data.get('email'))
        return {'Reply-To': reply_to}
