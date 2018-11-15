from datetime import date
from typing import List

from .models import *
from django.views.generic.list import MultipleObjectMixin
import datetime
import calendar


class UniversalMixins(object):

    def add_childrens_with_parents(self, *,  context=None, **kwargs):
        children_list = []

        for child in Children.objects.all():
            child_element = {}
            child_element['child'] = child
            child_element['parents'] = Parent.objects.filter(child=child)
            children_list.append(child_element)

        if context == None:
            context = {'children_with_parents': children_list}
        else:
            context['children_with_parents'] = children_list

        return context


def add_month(d, x):
    newday = d.day
    newmonth = (((d.month - 1) + x) % 12) + 1
    newyear  = d.year + (((d.month - 1) + x) // 12)
    if newday > calendar.mdays[newmonth]:
        newday = calendar.mdays[newmonth]
        if newyear % 4 == 0 and newmonth == 2:
            newday += 1
    return datetime.date(newyear, newmonth, newday)


def get_month_list(start_date, end_date):
    date1 = start_date.year * 12 + start_date.month
    date2 = end_date.year * 12 + end_date.month

    date1_first_day = datetime.date(start_date.year, start_date.month, 1)
    month_delta = date2 - date1 + 1

    month_list = [(lambda i: add_month(date1_first_day, i))(i) for i in range(month_delta)]
    return month_list
