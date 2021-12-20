from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("userdefinedfields", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="extrafield",
            old_name="required",
            new_name="is_required",
        ),
    ]
