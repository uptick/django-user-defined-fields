from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userdefinedfields", "0002_auto_20200923_0122"),
    ]

    operations = [
        migrations.AlterField(
            model_name="displaycondition",
            name="values",
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
