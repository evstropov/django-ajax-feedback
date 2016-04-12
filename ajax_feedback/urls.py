from django.conf.urls import url
from ajax_feedback.views import ContactFormView

urlpatterns = (
    url(r'$', ContactFormView.as_view(), name='ajax-feedback-form'),
)
