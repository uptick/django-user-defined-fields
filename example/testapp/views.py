from django.views.generic.base import TemplateView

from userdefinedfields.models import ExtraField

from .models import Book


class TestDashboardView(TemplateView):
    template_name = "testapp/base.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["books"] = Book.objects.all()
        ctx["extrafields"] = ExtraField.objects.all()
        return ctx
