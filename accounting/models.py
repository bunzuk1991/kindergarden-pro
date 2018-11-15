from django.db import models
from django.db.models import Sum
from garden.models import Children
from django.db.models.signals import pre_save, post_save
from kindergarden.utils import uniqe_slug_generator, generate_file_name
from django.contrib.auth import get_user_model
from django.dispatch import receiver
import uuid, datetime, calendar
from garden.mixins import get_month_list


class Service(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)


class PaymentGroup(models.Model):
    fullname = models.CharField(max_length=120, default='', blank=True)
    slug = models.SlugField(default='', blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.fullname


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
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

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


@receiver(post_save, sender=DocumentItem)
def change_total_sum(sender, instance, *args, **kwargs):
    owner = instance.owner_document
    total_sum = DocumentItem.objects.exclude(sum=None).aggregate(total=Sum('sum'))['total']
    owner.total_sum = total_sum
    owner.save()


class RegisterBalances(models.Model):
    owner_document = models.ForeignKey(Document, on_delete=models.CASCADE)
    month = models.DateField(auto_now_add=False)
    child = models.ForeignKey(Children, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    balance_start = models.DecimalField(max_digits=10, decimal_places=2)
    turnover = models.DecimalField(max_digits=10, decimal_places=2)
    balance_end = models.DecimalField(max_digits=10, decimal_places=2)

    @staticmethod
    def count_balances(child, date_start):
        list_of_month = get_month_list(date_start, datetime.date.today())
        start_month = datetime.date(date_start.year, date_start.month, 1)
        first_item = RegisterBalances.objects.filter(child=child, month=start_month)
        balance_list = {}

        if first_item.count() == 0:
            start_balances = 0
        else:
            start_balances = first_item[0].balance_start

        balance_list[start_month.strftime("%Y %m")] = [start_balances, 0, 0]
        ind = -1

        for item_ in list_of_month:
            ind += 1
            month_end = datetime.date(item_.year, item_.month, calendar.monthrange(item_.year, item_.month)[1])
            turnover_minus = DocumentItem.objects.filter(
                child=child,
                operation_date__range=(item_, month_end),
                owner_document__posted=True,
                owner_document__doc_type=Document.CH_OPLATA
            ).aggregate(opl=Sum('sum'))['opl']

            if turnover_minus is None:
                turnover_minus = 0

            turnover_plus = DocumentItem.objects.filter(
                child=child,
                operation_date__range=(item_, month_end),
                owner_document__posted=True
                ).exclude(
                owner_document__doc_type=Document.CH_OPLATA).aggregate(
                opl=Sum('sum'))['opl']

            if turnover_plus is None:
                turnover_plus = 0


            turnover = turnover_plus - turnover_minus

            if item_ == start_month:
                balance_list[start_month.strftime("%Y %m")] = [start_balances, turnover , start_balances + turnover]
            else:
                prev_month = list_of_month[ind-1].strftime("%Y %m")
                end_balances = balance_list[prev_month][2]
                balance_list[item_.strftime("%Y %m")] = [end_balances, turnover , end_balances + turnover]

        return balance_list


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        if hasattr(instance, 'name'):
            instance.slug = uniqe_slug_generator(instance, instance.name, instance.slug)
        else:
            instance.slug = uniqe_slug_generator(instance, instance.fullname, instance.slug)


pre_save.connect(slug_save, sender=PaymentGroup)
