from django.db import models
from garden.models import Children
from django.db.models.signals import pre_save
from kindergarden.utils import uniqe_slug_generator, generate_file_name
from django.contrib.auth import get_user_model
import uuid


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
    USER_MODEL = get_user_model()
    posted = models.BooleanField(default=False)
    owner = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)


class DocumentItem(models.Model):
    CH_OPLATA  = 'OPL'
    CH_NARAH   = 'NAR'
    CH_PERERAH = 'PER'

    DOC_TYPE_CHOICES = (
        (CH_OPLATA, "Оплата"),
        (CH_NARAH, "Нарахування"),
        (CH_PERERAH, "Перерахунок")
    )

    doc_type = models.CharField(max_length=25, choices=DOC_TYPE_CHOICES)
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    child = models.ForeignKey(Children, on_delete=models.CASCADE, related_name='item')
    operation_date = models.DateField(auto_now_add=False, verbose_name='Даат операції')
    sum = models.DecimalField(max_digits=10, decimal_places=2)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)



def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        if hasattr(instance, 'name'):
            instance.slug = uniqe_slug_generator(instance, instance.name, instance.slug)
        else:
            instance.slug = uniqe_slug_generator(instance, instance.fullname, instance.slug)


pre_save.connect(slug_save, sender=PaymentGroup)