from django.urls import path

from . import views

urlpatterns = [
    path('triggers_actives', views.TriggersActivesView.as_view(), name="triggers_actives"),
    path('triggers_by_description', views.TriggersDescriptionView.as_view(), name="triggres_by_description"),
    path('triggers_by_host', views.TriggersHostView.as_view(), name="triggres_by_host"),
]
