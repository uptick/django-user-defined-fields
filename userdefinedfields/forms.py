from django.forms import JSONField

from .widgets import ExtraFieldsInput


class ExtraFieldsField(JSONField):
    def __init__(self, model, *args, **kwargs):
        kwargs["required"] = False
        kwargs["initial"] = dict
        kwargs["widget"] = ExtraFieldsInput(model=model)
        super().__init__(*args, **kwargs)

    # Using widget_attrs would be good but it gets evaluated too early during __init__ when
    # the content types module is not active.
    #
    # Instead, we need to do this lazily, so we pass the ContentType to the widget.
    # See `ExtraFieldsInput`
    #
    # Leaving this block of code here to document the failed attempt.
    #
    # def widget_attrs(self, widget):
    #     attrs = super().widget_attrs(widget)
    #     ct = ContentType.objects.get_for_model(self.model)
    #     attrs.update({
    #         'class': settings.USERDEFINEDFIELDS_INPUT_CLASSES,
    #         'data-content-type-id': ct.pk,
    #     })
    #     return attrs
