from django.db import models
from django.db.models.signals import pre_save
from kindergarden.utils import uniqe_slug_generator, generate_file_name
from django.urls import reverse, reverse_lazy


class Organisation(models.Model):
    name = models.CharField(max_length=120)
    name_printable = models.CharField(max_length=256)
    slug = models.SlugField(default='', blank=True)
    address = models.CharField(max_length=150)
    kod_zkpo = models.CharField(max_length=10)
    kod_ipn = models.CharField(max_length=15)
    actual = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    update_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return 'Організація: %s, код ЗКПО: %s' % (self.name, self.kod_zkpo)


class GardenGroup(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=40)
    slug = models.SlugField(default='', blank=True)
    description = models.CharField(max_length=200)
    actual = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    update_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    gardengroup = models.ForeignKey(GardenGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, default='', blank=True)
    yearin = models.DateField(auto_now=False)
    yearout = models.DateField(auto_now=False)
    slug = models.SlugField(default='', blank=True)

    def __str__(self):
        return self.name


class Children(models.Model):
    fullname = models.CharField(max_length=200, default='')
    date_of_birth = models.DateField(auto_now=False)
    growth = models.PositiveIntegerField(default=0)
    weight = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    image = models.ImageField(upload_to=generate_file_name, default="no-image.png", blank=True, null=True)
    slug = models.SlugField(default='', blank=True)
    active = models.BooleanField(default=True)
    date_start = models.DateField(auto_now=False, blank=True)
    date_end = models.DateField(auto_now=False, blank=True)
    address = models.CharField(max_length=250, default='', blank=True)
    actual_group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.fullname

    def get_absolute_image_url(self):
        return "%s%s" % ('', self.image.url)

    def get_absolute_url(self):
        return reverse('child-detail', kwargs={'slug': self.slug})


class Relation(models.Model):
    name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    slug = models.SlugField(default='', blank=True)

    def __str__(self):
        return self.name


class Parent(models.Model):
    child = models.ForeignKey(Children, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=200, default='', blank=True)
    date_of_birth = models.DateField(auto_now=False)
    phone = models.CharField(max_length=40, default='', blank=True)
    address = models.CharField(max_length=250, default='', blank=True)
    work = models.CharField(max_length=250, default='')
    workplace = models.CharField(max_length=90, default='')
    with_child = models.BooleanField(default=True)
    relation = models.ForeignKey(Relation, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '%s(%s)' % (self.fullname, self.child.fullname)


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        if hasattr(instance, 'name'):
            instance.slug = uniqe_slug_generator(instance, instance.name, instance.slug)
        else:
            instance.slug = uniqe_slug_generator(instance, instance.fullname, instance.slug)


def GroupNameCreate(sender, instance, *args, **kwargs):
    if not instance.name:
        instance.name = '%s (%s/%s)' % (instance.gardengroup.name, instance.yearin.year, instance.yearout.year)
        print(dir(instance.yearin))


pre_save.connect(slug_save, sender=Organisation)
pre_save.connect(slug_save, sender=GardenGroup)
pre_save.connect(GroupNameCreate, sender=Group)
pre_save.connect(slug_save, sender=Group)
pre_save.connect(slug_save, sender=Children)
pre_save.connect(slug_save, sender=Relation)