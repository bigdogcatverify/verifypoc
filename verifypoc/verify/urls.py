from django.urls import path

from . import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('events/', views.EventListView.as_view(), name='events'),
    path('add_event/', views.add_event, name='add_event')
]