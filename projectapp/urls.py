from django.urls import path
from .views import page_am, page_am_result

urlpatterns = [
    path('', page_am, name='page_am'),
    path('antimortem/', page_am, name='page_am'),
    path('antimortem/result/', page_am_result, name='page_am_result'),

]
