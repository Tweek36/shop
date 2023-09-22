from django.urls import path
from . import views

app_name = "edit"

urlpatterns = [
    path("", views.edit_list, name="edit_list"),
    # path('<str:url>', views.edit_product, name='edit_product'),
    path("edit_ajax/", views.edit_ajax, name="edit_ajax"),
]
