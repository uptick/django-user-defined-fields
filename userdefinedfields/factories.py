try:
    import factory
except ImportError:
    import sys

    sys.stderr.write("Use of factories requires factory_boy\n")
    exit(1)

try:
    from factory.django import DjangoModelFactory
except ImportError:
    from factory import DjangoModelFactory

from django.utils.text import slugify

from .models import ExtraField


class ExtraFieldFactory(DjangoModelFactory):
    label = factory.Faker("company")
    name = factory.LazyAttribute(lambda o: slugify(o.label))
    widget = "TextInput"

    class Meta:
        model = ExtraField
