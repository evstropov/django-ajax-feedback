#!encoding=utf-8
from __future__ import unicode_literals

from django import template

from ajax_feedback.conf import AJAX_FEEDBACK_SETTINGS
from ajax_feedback.forms import get_form_class

register = template.Library()


@register.inclusion_tag(AJAX_FEEDBACK_SETTINGS.get('form_template'), takes_context=True)
def feedback_form(context):
    form = get_form_class(context['request'])

    username = context['request'].user.get_username()
    sender_name_field = AJAX_FEEDBACK_SETTINGS.get('sender_name_field')
    sender_email_field = AJAX_FEEDBACK_SETTINGS.get('sender_email_field')
    from_initial = {}
    if username:
        from_initial = {sender_name_field: username,
                        sender_email_field: context['request'].user.email}

    return {
        'form': form(initial=from_initial),
    }
