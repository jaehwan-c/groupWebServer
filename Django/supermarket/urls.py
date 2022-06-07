from django.urls import path, include
from supermarket import views
from .models import *
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from supermarket.views import *

urlpatterns = [

  # for home

  path("", views.home_page, name="home"),
  
  # for items
  path("items/", views.items_home, name="items_home"),

  path("items/view_items", ItemListView.as_view(), name="view_items"),
  path("items/view_items/<id>/update", views.update_view, name="update_view"),

  # managing Item Instances

  path("item_instance/", ItemInstanceView.as_view(), name="stock_home"),
  path("item_instance/<id>/<status>/update", views.update_stock, name="update_stock"),
  path("item_instance/data_analytics", views.data_analytics, name="data_analytics"),

  # stock-tacking
  path("stock_taking/", StockTakingJobsView.as_view(), name="stock_taking_home"),

  path("stock_taking/<id>/<status>/update", views.delete_jobs, name="delete_jobs"),
  path("stock_taking/create_jobs", views.create_jobs, name="create_jobs"),

# for login / signup
  path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
  path("accounts/logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
  path('accounts/join/', views.signup, name="join"),

  path("accounts/", views.view_personal_information, name="account_information"),
  path('accounts/change_password', views.change_password, name='change_password'),
  path('accounts/change_personal_information', views.change_personal_information, name='change_personal_information'),
]


# redirection
urlpatterns += [
  path("accounts/confirm.html", RedirectView.as_view(url="/")),
  path("items/view_items/<slug>/confirm", RedirectView.as_view(url="/items/view_items")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
