from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.initiate_phonepe_payment,name="initiate_phonepe_payment"),

]