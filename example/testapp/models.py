from django.db import models

from userdefinedfields.fields import ExtraFieldsJSONField


class Book(models.Model):
    name = models.CharField(max_length=100)
    metadata = ExtraFieldsJSONField()

    def __str__(self):
        return self.name
