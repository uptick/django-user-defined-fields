from django.contrib import admin

from .models import DisplayCondition, ExtraField


@admin.register(ExtraField)
class ExtraFieldAdmin(admin.ModelAdmin):
    pass


@admin.register(DisplayCondition)
class DisplayConditionAdmin(admin.ModelAdmin):
    pass
