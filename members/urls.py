from django.urls import path, include
from . import views 

urlpatterns = [
    path('login_user', views.login_user, name = 'login'),
    path('success_user',views.success_user,name='success'),
    path('logout_user',views.logout_user,name='logout')
]
