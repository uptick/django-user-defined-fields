User Defined Fields is a simple Django package to allow users to create virtual
fields and add them to your models.

The package provides the models, fields and formfields to make this process simple.

This package relies on postgres' JSONField for data storage.


In your models.py
```
from userdefinedfields import ExtraFieldsJSONField


class Property(models.Model):
    extra_fields = ExtraFieldsJSONField()
```


In your forms.py
```
class PropertyForm(forms.ModelForm):
    extra_fields = ExtraFieldsField(Property)
```
