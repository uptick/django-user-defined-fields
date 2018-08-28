from functools import partialmethod

from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField

from .models import ExtraField


class ExtraFieldsJSONField(JSONField):
    def __init__(self, *args, **kwargs):
        kwargs['default'] = dict
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)

    def _get_FIELD_fieldlist(self, obj, field):
        ct = ContentType.objects.get_for_model(obj)

        # grab the relevant extrafields for this content type
        relevant_fields = (
            ExtraField.objects
            .filter(content_type=ct)
            .prefetch_related('displaycondition_set')
        )

        # use the displaycondition_set to limit the fields
        filtered_fields = []
        for f in relevant_fields:
            dcset = f.displaycondition_set.all()
            if dcset:
                for dc in dcset:
                    if str(getattr(obj, f'{dc.key}_id')) in dc.values.split(','):
                        filtered_fields.append(f)
            else:
                # if there's no display conditions, include this field
                filtered_fields.append(f)

        # loop through and create a list of field info and values from the JSON blob
        data = getattr(obj, field.attname)
        fieldlist = []
        for f in filtered_fields:
            fieldlist.append((f.group, f.name, f.label, data.get(f.name, None)))
        return fieldlist

    def contribute_to_class(self, cls, name, **kwargs):
        # @todo change this to get_extra_fields_fieldlist
        setattr(cls, 'get_%s_display' % name, partialmethod(self._get_FIELD_fieldlist, field=self))
        # @todo add a get_FOO_display for each extra field which would eliminate the "display_value" templatetag filter
        super().contribute_to_class(cls, name)
