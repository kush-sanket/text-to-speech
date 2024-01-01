from django.urls import path,include
from . import views

urlpatterns = [
    path("signin",views.signin,name="signin"),
    path("register",views.register,name = "register"),
    path("signout",views.signout,name="signout"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]