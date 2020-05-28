from functools import partialmethod

from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField

from .models import ExtraField


class ExtraFieldsJSONField(JSONField):
    def __init__(self, *args, **kwargs):
        kwargs['default'] = dict
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)

    def _get_EXTRAFIELD_fieldlist(self, obj, field):
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
            val = data.get(f.name, None)

            # overwrite val with the pretty value if it's a choice field
            if 'choices' in f.field_settings:
                choices = dict([(choice.get('value'), choice.get('label')) for choice in f.field_settings['choices']])
                val = choices.get(val) or val
            fieldlist.append((f.group, f.name, f.label, val))

        return fieldlist

    def _get_EXTRAFIELD_display(self, obj, field):
        """ Return a dictionary of extrafields relevant to this instance.

        This lets you do something like this in a template:
        {{ asset.get_extra_fields_display.field_name }}
        """
        fieldlist = self._get_EXTRAFIELD_fieldlist(obj, field)
        return dict([(d[1], d[3]) for d in fieldlist])

    def contribute_to_class(self, cls, name, **kwargs):
        setattr(cls, 'get_%s_display' % name, partialmethod(self._get_EXTRAFIELD_display, field=self))
        setattr(cls, 'get_%s_fieldlist' % name, partialmethod(self._get_EXTRAFIELD_fieldlist, field=self))
        super().contribute_to_class(cls, name)
