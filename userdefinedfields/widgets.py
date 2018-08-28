from django.contrib.contenttypes.models import ContentType
from django.forms.widgets import Textarea


class ExtraFieldsInput(Textarea):
    def __init__(self, attrs=None, model=None, *args, **kwargs):
        attrs = attrs or {}
        attrs.update({
            'class': 'react-extra-fields-renderer hidden-xs-up',
        })
        self.model = model
        super().__init__(attrs, *args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        ct = ContentType.objects.get_for_model(self.model)
        attrs.update({
            'data-content-type-id': ct.pk
        })
        return super().render(name, value, attrs, renderer=renderer)
