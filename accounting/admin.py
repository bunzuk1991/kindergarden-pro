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


class VisitingItemInline(admin.TabularInline):
    model = VisitingItem
    extra = 0


class VisitingDocumentAdmin(admin.ModelAdmin):
    list_display = ('doc_type', 'create_date', 'posted', 'update_date', 'owner', 'total_sum')
    inlines = [VisitingItemInline]

    class Meta:
        model = VisitingDocument


class RegisterBalanceAdmin(admin.ModelAdmin):
    list_display = ('month', 'child', 'service', 'balance_start', 'turnover', 'balance_end')
    ordering = ['month', 'child', 'service']

    class Meta:
        model = RegisterBalances


admin.site.register(Document, DocumentAdmin)
admin.site.register(VisitingDocument, VisitingDocumentAdmin)
admin.site.register(ChildPaymentGroup)
admin.site.register(PaymentGroup)
admin.site.register(Service)
admin.site.register(PaymentPrice)
admin.site.register(RegisterBalances, RegisterBalanceAdmin)


