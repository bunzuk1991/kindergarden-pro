from django.contrib import admin
from . models import *


class ParentsInline(admin.TabularInline):
    model = Parent
    extra = 0


class ChildrenAdmin(admin.ModelAdmin):
    list_display = ["fullname", "date_of_birth", "active", "address", "actual_group"]
    inlines = [ParentsInline]

    class Meta:
        model = Children

admin.site.register(Organisation)
admin.site.register(GardenGroup)
admin.site.register(Group)
admin.site.register(Relation)
admin.site.register(Parent)
admin.site.register(Children, ChildrenAdmin)