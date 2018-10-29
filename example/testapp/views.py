from django.views.generic.base import TemplateView

import userdefinedfields # noqa


class TestDashboardView(TemplateView):
    template_name = 'testapp/base.html'
