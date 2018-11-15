from django.contrib import admin
from . models import *


class DocumentItemInline(admin.TabularInline):
    model = DocumentItem
    extra = 0


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('doc_type', 'create_date', 'posted', 'update_date', 'owner', 'total_sum')
    inlines = [DocumentItemInline]

    class Meta:
        model = Document


admin.site.register(Document, DocumentAdmin)
admin.site.register(ChildPaymentGroup)
admin.site.register(PaymentGroup)
admin.site.register(Service)
admin.site.register(RegisterBalances)


