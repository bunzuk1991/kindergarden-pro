from django.utils.text import slugify
from transliterate import translit


def uniqe_slug_generator(model_instance, title, slug_field):
    slug = slugify(translit(str(title), reversed=True))
    model_class = model_instance.__class__

    if model_class.objects.filter(slug=slug).count() > 0:
        object_pk = model_class.objects.latest('pk')
        object_pk = object_pk.pk + 1

        slug = f'{slug}-{object_pk}'
    return slug


def generate_file_name(instance, filename):
    file_split = filename.split('.')

    if hasattr(instance, 'name'):
        new_field = slugify(translit(str(instance.name), reversed=True))
    else:
        new_field = slugify(translit(str(instance.fullname), reversed=True))

    return "%s/%s" % (new_field, filename)
