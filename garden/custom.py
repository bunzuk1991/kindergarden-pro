from . models import *
from django.http.response import JsonResponse


def get_relation_list():
    new_list = list(Relation.objects.all().values('id', 'name'))

    json_data = {
        "list": new_list
    }
    return JsonResponse(json_data)

