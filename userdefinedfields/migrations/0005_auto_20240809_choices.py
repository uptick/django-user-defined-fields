from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userdefinedfields", "0004_alter_extrafield_widget"),
    ]

    operations = [
        migrations.AlterField(
            model_name="extrafield",
            name="widget",
            field=models.CharField(
                choices=[
                    ("text", "Text"),
                    ("multiline-text", "Multiline Text"),
                    ("integer", "Integer"),
                    ("decimal", "Decimal"),
                    ("choice", "Choice"),
                    ("date", "Date"),
                    ("decimal", "Decimal"),
                ],
                default="text",
                max_length=32,
            ),
        ),
    ]