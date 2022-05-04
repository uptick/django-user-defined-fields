from django.db import models


class ExtraField(models.Model):
    WIDGET_CHOICES = (
        ("text", "Text"),
        ("multiline-text", "Multiline Text"),
        ("integer", "Integer"),
        ("choice", "Choice"),
        ("date", "Date"),
        ("decimal", "Decimal"),
    )
    content_type = models.ForeignKey("contenttypes.ContentType", on_delete=models.PROTECT)
    group = models.CharField("Field group", blank=True, max_length=32)
    order = models.IntegerField(default=0)
    label = models.CharField("Display name", max_length=50)
    name = models.SlugField()
    field_settings = models.JSONField(default=dict, blank=True)
    widget = models.CharField(max_length=32, default="text", choices=WIDGET_CHOICES)
    default = models.CharField(max_length=1024, blank=True, default="")
    in_list = models.BooleanField("Show in list view?", default=True)
    is_required = models.BooleanField("Should field be required?", default=False)
    help_text = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f"{self.content_type} {self.name}"

    class Meta:
        unique_together = (
            (
                "content_type",
                "name",
            ),
        )
        ordering = ("content_type", "group", "order")


class DisplayCondition(models.Model):
    field = models.ForeignKey(ExtraField, on_delete=models.CASCADE)
    key = models.CharField(max_length=32, blank=True)
    values = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.field} {self.key} {self.values}"

    class Meta:
        ordering = ("id",)
