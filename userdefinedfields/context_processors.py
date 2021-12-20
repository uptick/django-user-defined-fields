from collections import defaultdict

from .models import DisplayCondition, ExtraField


def get_extra_fields():
    conditions = defaultdict(list)
    for condition in DisplayCondition.objects.all():
        conditions[condition.field_id].append(
            {
                "key": condition.key,
                "values": condition.values,
            }
        )

    extra_fields = defaultdict(list)
    for field in ExtraField.objects.all():
        extra_fields[field.content_type_id].append(
            {
                "name": field.name,
                "label": field.label,
                "widget": field.widget,
                "settings": field.field_settings,
                "conditions": conditions[field.id],
                "help_text": field.help_text,
                "is_required": field.is_required,
            }
        )

    return extra_fields
