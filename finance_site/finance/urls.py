from django.urls import path

from . import views

app_name = "finance"

urlpatterns = [
    # транзакции
    path("", views.transaction_list, name="transaction_list"),
    path("add/", views.transaction_create, name="transaction_create"),
    path(
        "transactions/<int:pk>/edit/",
        views.transaction_edit,
        name="transaction_edit",
    ),
    path(
        "transactions/<int:pk>/delete/",
        views.transaction_delete,
        name="transaction_delete",
    ),

    # категории
    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.category_create, name="category_create"),
    path(
        "categories/<int:pk>/edit/",
        views.category_edit,
        name="category_edit",
    ),
    path(
        "categories/<int:pk>/delete/",
        views.category_delete,
        name="category_delete",
    ),
]
