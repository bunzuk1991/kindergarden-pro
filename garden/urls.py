from django.urls import path
from .views import *

urlpatterns = [
    path('childrens/', ChildrenListView.as_view(), name='childrens-list'),
    path('child/edit/<slug:slug>/', ChildDetailView.as_view(), name='child-detail'),
    path('child/create/', ChildDetailView.as_view(), name='child-create'),
]
