from django.urls import path
from .views import *

urlpatterns = [
    path('childrens/', ChildrenListView.as_view(), name='childrens-list'),
    path('child/<slug:slug>/', ChildDetail.as_view(), name='child-detail'),
]
