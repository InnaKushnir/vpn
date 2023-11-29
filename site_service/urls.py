from django.urls import path
from . import views

urlpatterns = [
    path('sites/', views.SiteListView.as_view(), name='site-list'),
    path('sites/create/', views.SiteCreateView.as_view(), name='site-create'),
    path('sites/delete/<int:pk>/', views.SiteDeleteView.as_view(), name='site-delete'),
    path('sites/update/<int:pk>/', views.SiteUpdateView.as_view(), name='site-update'),
    path('proxy/<str:user_site_name>/', views.proxy_view, name='proxy-view'),
    path('proxy/<str:user_site_name>/<path:routes_on_original_site>/', views.proxy_view_with_path, name='proxy-view-with-path'),
]

app_name = "site_service"
