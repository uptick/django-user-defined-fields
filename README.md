# django-user-defined-fields

[![PyPI version](https://badge.fury.io/py/django-user-defined-fields.svg)](https://badge.fury.io/py/django-user-defined-fields)

Django Used Defined Fields is a simple way to allow your users to add extra fields to your models, based on JSONField.


## Installation

Standard pip install:

```bash
pip install django-user-defined-fields
```


## Quickstart

```python
from userdefinedfields.models import ExtraFieldsJSONField


class Example(models.Model):
  extra_fields = ExtraFieldsJSONField()

```

## Tests
Run tests in example directory with `python manage.py test testapp`


# Settings
```
USERDEFINEDFIELDS_INPUT_CLASSES = 'd-none'  # hide the textarea if you're using a frontend solution
```
