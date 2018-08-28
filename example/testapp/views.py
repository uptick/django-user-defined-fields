from django.urls import reverse
from django.views.generic.edit import TemplateView

import userdefinedfields

from .models import Citation


class TestDashboardView(TemplateView):
    template_name = 'testapp/base.html'
