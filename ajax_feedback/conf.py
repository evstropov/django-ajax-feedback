from django.conf import settings
from django.utils.translation import ugettext as _

changed_settings = getattr(settings, 'AJAX_FEEDBACK_SETTINGS', {})

AJAX_FEEDBACK_SETTINGS = {
    # form
    'form': changed_settings.get('form', 'ajax_feedback.forms.BaseContactForm'),
    'message_max_length': changed_settings.get('message_max_length', 500),
    'recaptcha': changed_settings.get('recaptcha', False),
    'sender_name_field': changed_settings.get('sender_name_field', 'name'),
    'sender_email_field': changed_settings.get('sender_email_field', 'email'),
    # templates
    'form_template': changed_settings.get('form_template', 'ajax_feedback/contact_form.html'),
    'subject_template': changed_settings.get('subject_template', 'ajax_feedback/subject.txt'),
    'message_template': changed_settings.get('message_template', 'ajax_feedback/message.html'),
    # send settings
    'recipient_list': changed_settings.get('recipient_list', []),
    # messages
    'success_message': changed_settings.get('success_message', _('Message sent successfully')),
    'failed_message': changed_settings.get('failed_message', _('Failed send message, please try again or contact with administrator')),
}