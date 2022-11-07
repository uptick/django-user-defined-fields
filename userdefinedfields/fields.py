from functools import partialmethod

from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.exceptions import FieldDoesNotExist
from django.db.models import JSONField
from django.db.models.fields.related import ForeignKey

from .models import ExtraField


class ExtraFieldsJSONField(JSONField):
    def __init__(self, *args, **kwargs):
        kwargs["default"] = kwargs.get("default", dict)
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)

    def _get_EXTRAFIELD_fieldlist(self, obj, field, use_cache=False):

        # grab the relevant extrafields for this content type
        # Cache the results, if using the cache
        if use_cache:
            cache_key = f"django-extra-fields-{hash(type(obj))}"
            relevant_fields = cache.get(cache_key)
        else:
            relevant_fields = None

        if not relevant_fields:
            ct = ContentType.objects.get_for_model(obj)
            relevant_fields = (
                ExtraField.objects.filter(content_type=ct)
                .prefetch_related("displaycondition_set")
                .all()
            )

        if use_cache:
            cache.set(cache_key, relevant_fields, 30)

        # include only the fields that aren't rejected by their display conditions.
        filtered_fields = []
        for f in relevant_fields:
            for dc in f.displaycondition_set.all():
                # Split the dc.key on '__' to create path to relevant field
                # This still works for model fields as the traversal will
                # only happen once
                fields = dc.key.split("__")

                # Set the initial target model
                target_model = type(obj)
                try:
                    # For each field_name, traverse the field and target_models
                    for field_name in fields:
                        dc_field = target_model._meta.get_field(field_name)
                        target_model = dc_field.related_model
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
                if fields[-1] != dc_field.name:
                    break

                # First target the initial obj
                target_obj = obj

                # For each field provided, walk down the tree expect the last as
                # is what the test will be performed on in the next step
                for field_name in fields[:-1]:
                    try:
                        target_obj = getattr(obj, field_name)
                    except AttributeError:
                        # This is unlikely, but provided as insurance
                        # in case the attribute doesn't resolve
                        break

                # Check to see whether the condition is satisfied.
                if str(getattr(target_obj, f"{dc_field.name}_id")) not in dc.values.split(","):
                    # Don't add the field if the id is not on the object
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
            if "choices" in f.field_settings:
                choices = {
                    choice.get("value"): choice.get("label")
                    for choice in f.field_settings["choices"]
                }
                val = choices.get(val) or val
            fieldlist.append((f.group, f.name, f.label, val))

        return fieldlist

    def _get_EXTRAFIELD_display(self, obj, field):
        """Return a dictionary of extrafields relevant to this instance.

        This lets you do something like this in a template:
        {{ asset.get_extra_fields_display.field_name }}
        """
        fieldlist = self._get_EXTRAFIELD_fieldlist(obj, field)
        return {d[1]: d[3] for d in fieldlist}

    def contribute_to_class(self, cls, name, **kwargs):
        setattr(
            cls,
            f"get_{name}_display",
            partialmethod(self._get_EXTRAFIELD_display, field=self),
        )
        setattr(
            cls,
            f"get_{name}_fieldlist",
            partialmethod(self._get_EXTRAFIELD_fieldlist, field=self),
        )
        super().contribute_to_class(cls, name)
