import json

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

# Create your tests here.
from userdefinedfields.models import ExtraField, DisplayCondition


class CustomFieldTest(TestCase):
    def setUp(self) -> None:
        self.book_type = ContentType.objects.filter(model="book").first()
        self.field = ExtraField(
            content_type=self.book_type,
            label="Author",
            name="author",
            widget="text",
        )
        self.field.save()

    def test_create_field(self):
        field = ExtraField(
            content_type=self.book_type,
            label="Publish Year",
            name="published",
            widget="date",
        )
        field.save()
        self.assertIsNotNone(field.id)
        self.assertEqual(str(field), "library | book published")

    def test_metadata(self):
        from .models import Book

        # Create a book
        book = Book(name="The Way of Kings")
        book.save()
        self.assertIsNotNone(book.id)
        self.assertIsNotNone(book.get_metadata_fieldlist)

        # Test that current metadata is empty
        metadata = book.get_metadata_fieldlist()
        fields = {x[1]: x for x in metadata}
        self.assertIsNone(fields["author"][3])

        # Add metadata
        book.metadata = {"author": "Brandon Sanderson"}
        book.save()

        # Test new data
        metadata = book.get_metadata_fieldlist()
        fields = {x[1]: x for x in metadata}
        self.assertEqual(fields["author"][3], "Brandon Sanderson")

    def test_conditions(self):
        from .models import Book, Section

        fantasy = Section(name="Fantasy")
        fantasy.save()
        recipes = Section(name="Recipes")
        recipes.save()

        field = ExtraField(
            content_type=self.book_type,
            label="Contains dragons",
            name="has_dragons",
            widget="bool",
        )
        field.save()

        condition = DisplayCondition(
            field=field,
            key="section",
            values=str(fantasy.id),
        )
        condition.save()

        book = Book(
            name="Words of Radiance",
            section=fantasy,
            metadata={"author": "Brandon Sanderson", "has_dragons": False},
        )
        book.save()

        metadata = book.get_metadata_fieldlist()
        fields = {x[1]: x for x in metadata}
        self.assertIn("has_dragons", fields)

        book2 = Book(
            name="Uncook Yourself",
            section=recipes,
            metadata={"author": "Nat's What I Reckon"},
        )
        book2.save()

        metadata = book2.get_metadata_fieldlist()
        fields = {x[1]: x for x in metadata}
        self.assertNotIn("has_dragons", fields)

    def test_relational_conditions(self):
        from .models import Book, Section, SectionType

        fiction = SectionType(name="Fiction")
        fiction.save()
        nonfiction = SectionType(name="Non-Fiction")
        nonfiction.save()

        fantasy = Section(name="Fantasy", section_type=fiction)
        fantasy.save()
        science = Section(name="Science", section_type=nonfiction)
        science.save()

        field = ExtraField(
            content_type=self.book_type,
            label="Dewey Decimal",
            name="dewey_decimal",
            widget="text",
        )
        field.save()

        condition = DisplayCondition(
            field=field,
            key="section__section_type",
            values=str(nonfiction.id),
        )
        condition.save()

        book = Book(
            name="Oathbringer",
            section=fantasy,
            metadata={"author": "Brandon Sanderson"},
        )
        book.save()

        metadata = book.get_metadata_fieldlist()
        fields = {x[1]: x for x in metadata}
        self.assertNotIn("dewey_decimal", fields)

        book2 = Book(
            name="Immune",
            section=science,
            metadata={
                "author": "Philipp Dettmer",
                "dewey_decimal": "571",
            },
        )
        book2.save()

        metadata = book2.get_metadata_fieldlist()
        fields = {x[1]: x for x in metadata}
        self.assertIn("dewey_decimal", fields)
