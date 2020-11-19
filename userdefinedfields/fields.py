from functools import partialmethod

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist
from django.db.models import JSONField
from django.db.models.fields.related import ForeignKey

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

        # include only the fields that aren't rejected by their display conditions.
        filtered_fields = []
        for f in relevant_fields:
            for dc in f.displaycondition_set.all():
                try:
                    dc_field = type(obj)._meta.get_field(dc.key)
                except FieldDoesNotExist:
                    # Well this won't do. Poorly defined field. Since this'll be commonly used
                    # in templates though, we opt to squelch the error, rather than be noisy about
                    # it. Users will quickly notice their extra field is not coming up.
                    break

                if not isinstance(dc_field, ForeignKey):
                    # We only support FK-based display conditions, by design! Here's why:
                    # - Other attributes on the object -- Having business logic based on random
                    #    fields like, eg. the objects name, promotes bad design. Exception could
                    #    perhaps be choice fields, but let's just reject attribs across the board
                    #    for now.
                    # - M2Ms -- These are generally less persistent than FKs, and we generally want
                    #    extra fields to stay visible once set up. Also, certain M2Ms, such as tags,
                    #    already cover a similar space to what extra fields are trying to achieve.
                    #    Also, most importantly, checking against these would incur an extra db hit.
                    # - Attributes on related objects -- Would incur additional db hits too. This'd
                    #    be quite costly when trying to display a whole bunch of objects and their
                    #    extra fields in a list. So we opt to avoid this headache altogether.
                    break

                # To avoid letting users have multiple ways of doing the same thing, we reject
                # conditions that have tried to supply the `_id` suffix themselves.
                # (The earlier get_field call tolerates for both with and without.)
                if dc.key != dc_field.name:
                    break

                # Check to see whether the condition is satisfied.
                if str(getattr(obj, f'{dc_field.name}_id')) not in dc.values.split(','):
                    break
            else:
                # We didn't trip any display condition failures; field is good to add.
                filtered_fields.append(f)

        # loop through and create a list of field info and values from the JSON blob
        data = getattr(obj, field.attname)
        fieldlist = []
        for f in filtered_fields:
            val = data.get(f.name, None)

            # overwrite val with the pretty value if it's a choice field
            if 'choices' in f.field_settings:
                choices = {choice.get('value'): choice.get('label') for choice in f.field_settings['choices']}
                val = choices.get(val) or val
            fieldlist.append((f.group, f.name, f.label, val))

        return fieldlist

    def _get_EXTRAFIELD_display(self, obj, field):
        """ Return a dictionary of extrafields relevant to this instance.

        This lets you do something like this in a template:
        {{ asset.get_extra_fields_display.field_name }}
        """
        fieldlist = self._get_EXTRAFIELD_fieldlist(obj, field)
        return {d[1]: d[3] for d in fieldlist}

    def contribute_to_class(self, cls, name, **kwargs):
        setattr(cls, f'get_{name}_display', partialmethod(self._get_EXTRAFIELD_display, field=self))
        setattr(cls, f'get_{name}_fieldlist', partialmethod(self._get_EXTRAFIELD_fieldlist, field=self))
        super().contribute_to_class(cls, name)
