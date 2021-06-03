from django.urls import path
from . import views

app_name = "services"

urlpatterns = [

    # Options URL
    path("add_service/<int:id>/", views.add_service, name="add_service"),
    path("view_services/<int:id>/", views.view_services, name="view_services"),

    # Pathway URLS
    path("pathways/create/<int:id>/", views.pathway_create, name="pathway_create"),
    path("pathways/list/<int:id>/", views.pathway_list, name="pathway_list"),
    path("pathways/delete/<int:id>/", views.pathway_delete, name="pathway_delete"),
    path("pathways/edit/<int:id>/", views.pathway_edit, name="pathway_edit"),
    path("referral_source/create/<int:id>/", views.referral_source_create, name="referral_source_create"),

    # D2A URLS
    path("D2A/create/<int:id>/", views.D2A_create, name="D2A_create"),
    path("D2A/list/<int:id>/", views.D2A_list, name="D2A_list"),
    path("D2A/delete/<int:id>/", views.D2A_delete, name="D2A_delete"),
    path("D2A/edit/<int:id>/", views.D2A_edit, name="D2A_edit"),

    # Referral URLS
    path("referral/create/<int:id>/", views.referral_create, name="referral_create"),
    path("referral/list/<int:id>/", views.referral_list, name="referral_list"),
    path("referral/delete/<int:id>/", views.referral_delete, name="referral_delete"),
    path("referral/edit/<int:id>/", views.referral_edit, name="referral_edit"),

    # Discharge URLS
    path("discharge/create/<int:id>/", views.discharge_create, name="discharge_create"),
    path("discharge/list/<int:id>/", views.discharge_list, name="discharge_list"),
    path("discharge/delete/<int:id>/", views.discharge_delete, name="discharge_delete"),
    path("discharge/edit/<int:id>/", views.discharge_edit, name="discharge_edit"),
    path("discharge_service/create/<int:id>/", views.discharge_service_create, name="discharge_service_create"),
]
