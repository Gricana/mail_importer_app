from django.urls import path

from .views import AccountLoginView, AccountLogoutView


urlpatterns = [
    path('login/', AccountLoginView.as_view(), name='acc_login'),
    path('logout/', AccountLogoutView.as_view(), name='acc_logout'),
]
