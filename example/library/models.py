from django.db import models

from userdefinedfields.fields import ExtraFieldsJSONField


class SectionType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=100)
    section_type = models.ForeignKey(
        SectionType,
        null=True,
        default=None,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100)
    metadata = ExtraFieldsJSONField()
    section = models.ForeignKey(
        Section,
        null=True,
        default=None,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.name
