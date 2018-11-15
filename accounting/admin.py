from django.contrib import admin
from . models import *


class DocumentItemInline(admin.TabularInline):
    model = DocumentItem
    extra = 0


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['_all_']
    inlines = [DocumentItemInline]

    class Meta:
        model = Document


admin.site.register(Document, DocumentAdmin)
admin.site.register(ChildPaymentGroup)
admin.site.register(PaymentGroup)
admin.site.register(Service)


