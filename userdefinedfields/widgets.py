from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.forms.widgets import Textarea

DEFAULT_INPUT_CLASSNAME = ""


class ExtraFieldsInput(Textarea):
    def __init__(self, attrs=None, model=None, *args, **kwargs):
        attrs = attrs or {}
        attrs.update(
            {
                "class": getattr(settings, "CUSTOM_FIELDS_INPUT_CLASSES", DEFAULT_INPUT_CLASSNAME),
            }
        )
        self.model = model
        super().__init__(attrs, *args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        ct = ContentType.objects.get_for_model(self.model)
        attrs.update({"data-content-type-id": ct.pk})
        return super().render(name, value, attrs, renderer=renderer)
