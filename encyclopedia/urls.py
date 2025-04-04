from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/",views.entry_page,name="entry_page"),
    path("wiki/search",views.search,name="search"),
    path("wiki/new",views.new_page,name="new_page"),
    path("wiki/<str:title>/edit",views.edit_page,name="edit_page"),
    path("wiki/random",views.random_page,name="random_page")
]
