from django.contrib.sites.models import get_current_site
from django.views.generic import FormView
from ajax_feedback.forms import AuthContactForm, GuestContactForm
from ajax_feedback.send_email import SendEmail


class ContactFormView(FormView):
    template_name = 'ajax_feedback/contact_form.html'

    def _get_site_name(self):
        return get_current_site(self.request)

    def form_valid(self, form):
        sender = SendEmail(self._get_site_name())
        sender.send(form.cleaned_data)
        return form.result(True, None)

    def form_invalid(self, form):
        return form.result(False, form.get_form_errors())

    def get_form_kwargs(self):
        kwargs = super(ContactFormView, self).get_form_kwargs()
        username = self.request.user.get_username()
        if not kwargs['initial'].get('name') and username:
            kwargs['initial']['name'] = username
            kwargs['initial']['email'] = self.request.user.email
        return kwargs

    def get_form_class(self):
        if self.request.user.is_authenticated():
            return AuthContactForm
        else:
            return GuestContactForm
