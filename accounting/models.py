import calendar
import datetime
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from django.db.models.signals import pre_save
from django.dispatch import receiver

from garden.mixins import get_month_list
from garden.models import Children
from kindergarden.utils import uniqe_slug_generator


class Service(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PaymentGroup(models.Model):
    PAY_DAY = 'DAY'
    PAY_MONTH = 'MONTH'
    PAY_ONCE = 'ONCE'

    PAY_PERIOD = (
        (PAY_DAY, 'ДЕНЬ'),
        (PAY_MONTH, 'МІСЯЦЬ'),
        (PAY_ONCE, 'ОДНОРАЗОВО')
    )

    fullname = models.CharField(max_length=120, default='', blank=True)
    slug = models.SlugField(default='', blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    period = models.CharField(max_length=20, choices=PAY_PERIOD, default=PAY_DAY, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.fullname


class PaymentPrice(models.Model):
    payment_group = models.ForeignKey(PaymentGroup, on_delete=models.CASCADE)
    date_start = models.DateField(auto_now_add=False)
    date_end = models.DateField(auto_now_add=False, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class ChildPaymentGroup(models.Model):
    child = models.ForeignKey(Children, on_delete=models.CASCADE)
    payment_group = models.ForeignKey(PaymentGroup, on_delete=models.CASCADE)
    date_start = models.DateField(auto_now=False)
    date_end = models.DateField(auto_now=False, blank=True, null=True)
    enable = models.BooleanField(default=True)

    def __str__(self):
        return '%s:%s' % (self.child.fullname, self.payment_group.fullname)


class Document(models.Model):
    CH_OPLATA = 'OPL'
    CH_NARAH = 'NAR'
    CH_PERERAH = 'PER'

    DOC_TYPE_CHOICES = (
        (CH_OPLATA, "Оплата"),
        (CH_NARAH, "Нарахування"),
        (CH_PERERAH, "Перерахунок")
    )

    USER_MODEL = get_user_model()
    posted = models.BooleanField(default=False)
    owner = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    doc_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        if self.id is not None:
            old_document = Document.objects.get(id=self.id)
            if old_document.posted != self.posted:
                super(Document, self).save(*args, **kwargs)

                for doc_item in self.documentitem_set.all():
                    RegisterBalances.count_balances(doc_item.child, doc_item.service, doc_item.operation_date)
            else:
                super(Document, self).save(*args, **kwargs)
        else:
            super(Document, self).save(*args, **kwargs)

    def __str__(self):
        date_format = '%s.%s.%s' % (self.update_date.day, self.update_date.month, self.update_date.year)
        status = 'проведено' if self.posted else 'не проведено'
        return '%s від %s (%s)' % (self.doc_type, date_format, status)


class DocumentItem(models.Model):
    owner_document = models.ForeignKey(Document, on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    child = models.ForeignKey(Children, on_delete=models.CASCADE, related_name='item')
    operation_date = models.DateField(auto_now_add=False, verbose_name='Даат операції')
    sum = models.DecimalField(max_digits=10, decimal_places=2)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        super(DocumentItem, self).save(*args, **kwargs)
        print(self)
        RegisterBalances.count_balances(self.child, self.service, self.operation_date)

        owner = self.owner_document
        owner.total_sum = DocumentItem.objects.exclude(sum=None).aggregate(total=Sum('sum'))['total']
        owner.save()

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        super(DocumentItem, self).delete(*args, **kwargs)
        RegisterBalances.count_balances(self.child, self.service, self.operation_date)

        owner = self.owner_document
        owner.total_sum = DocumentItem.objects.exclude(sum=None).aggregate(total=Sum('sum'))['total']
        owner.save()


class VisitingDocument(Document):
    operation_date = models.DateField(auto_now_add=False)
    present_amount = models.PositiveIntegerField(default=0, blank=True)
    missing_amount = models.PositiveIntegerField(default=0, blank=True)
    total_amount = models.PositiveIntegerField(default=0, blank=True)


class VisitingItem(DocumentItem):
    present = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class RegisterBalances(models.Model):
    month = models.DateField(auto_now_add=False)
    child = models.ForeignKey(Children, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    balance_start = models.DecimalField(max_digits=10, decimal_places=2)
    turnover = models.DecimalField(max_digits=10, decimal_places=2)
    balance_end = models.DecimalField(max_digits=10, decimal_places=2)

    @staticmethod
    def count_balances(child, service, date_start, owner_exclude=None):
        list_of_month = get_month_list(date_start, datetime.date.today())
        start_month = datetime.date(date_start.year, date_start.month, 1)
        first_item = RegisterBalances.objects.filter(child=child, month=start_month)
        balance_list = {}

        if first_item.count() == 0:
            start_balances = 0
        else:
            start_balances = first_item[0].balance_start

        balance_list[start_month.strftime("%Y %m")] = [start_balances, 0, 0, start_month]
        ind = -1

        for item_ in list_of_month:
            ind += 1
            month_end = datetime.date(item_.year, item_.month, calendar.monthrange(item_.year, item_.month)[1])
            if owner_exclude is None:
                turnover_minus = DocumentItem.objects.filter(
                    child=child,
                    service=service,
                    operation_date__range=(item_, month_end),
                    owner_document__posted=True,
                    owner_document__doc_type=Document.CH_OPLATA
                ).aggregate(opl=Sum('sum'))['opl']
            else:
                turnover_minus = DocumentItem.objects.exclude(owner_document=owner_exclude).filter(
                    child=child,
                    service=service,
                    operation_date__range=(item_, month_end),
                    owner_document__posted=True,
                    owner_document__doc_type=Document.CH_OPLATA
                ).aggregate(opl=Sum('sum'))['opl']

            if turnover_minus is None:
                turnover_minus = 0

            if owner_exclude is None:
                turnover_plus = DocumentItem.objects.filter(
                    child=child,
                    service=service,
                    operation_date__range=(item_, month_end),
                    owner_document__posted=True
                ).exclude(
                    owner_document__doc_type=Document.CH_OPLATA).aggregate(
                    opl=Sum('sum'))['opl']
            else:
                turnover_plus = DocumentItem.objects.exclude(owner_document=owner_exclude).filter(
                    child=child,
                    service=service,
                    operation_date__range=(item_, month_end),
                    owner_document__posted=True
                ).exclude(
                    owner_document__doc_type=Document.CH_OPLATA).aggregate(
                    opl=Sum('sum'))['opl']

            if turnover_plus is None:
                turnover_plus = 0

            turnover = turnover_plus - turnover_minus

            if item_ == start_month:
                balance_list[start_month.strftime("%Y %m")] = [start_balances, turnover, start_balances + turnover,
                                                               item_]
            else:
                prev_month = list_of_month[ind - 1].strftime("%Y %m")
                end_balances = balance_list[prev_month][2]
                balance_list[item_.strftime("%Y %m")] = [end_balances, turnover, end_balances + turnover, item_]

        items = RegisterBalances.objects.filter(child=child, service=service, month__gte=start_month)
        for balance_item in balance_list:
            values = balance_list[balance_item]
            elem_balance = items.filter(month=values[3])
            if elem_balance.count() > 0:
                for elem in elem_balance:
                    elem.balance_start = values[0]
                    elem.turnover = values[1]
                    elem.balance_end = values[2]
                    elem.save()
            else:
                print('new')
                new_item = RegisterBalances(
                    child=child,
                    service=service,
                    month=values[3],
                    balance_start=values[0],
                    turnover=values[1],
                    balance_end=values[2]
                )
                new_item.save()


@receiver(pre_save, sender=PaymentGroup)
def slug_save(instance):
    if not instance.slug:
        if hasattr(instance, 'name'):
            instance.slug = uniqe_slug_generator(instance, instance.name, instance.slug)
        else:
            instance.slug = uniqe_slug_generator(instance, instance.fullname, instance.slug)
