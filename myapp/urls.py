"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('blog/',views.blog,name='blog'),
    path('contact/',views.contact,name='contact'),
    path('product/ <str:cat>/',views.product,name='product'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('fpass/',views.fpass,name='fpass'),
    path('otp/',views.otp,name='otp'),
    path('newpass/',views.newpass,name='newpass'),
    path('cpassword/',views.cpassword,name='cpassword'),
    path('sindex/',views.sindex,name='sindex'),
    path('ajax/',views.ajax,name='ajax'),

    #path('profile/',views.profile,name='profile'),
    path('add/',views.add,name='add'),
    path('view/',views.view,name='view'),
    path('pdetail/ <int:pk>/',views.pdetail,name='pdetail'),
    path('pedit/ <int:pk>/',views.pedit,name='pedit'),
    path('pdelete/ <int:pk>/',views.pdelete,name='pdelete'),
    path('bpdetails/ <int:pk>/',views.bpdetails,name='bpdetails'),
    path('addwhis/ <int:pk>/',views.addwhis,name='addwhis'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('dwhish/ <int:pk>/',views.dwhish,name='dwhish'),
    path('addcart/ <int:pk>/',views.addcart,name='addcart'),
    path('dcart/ <int:pk>/',views.dcart,name='dcart'),
    path('scart/',views.scart,name='scart'),
    path('changeqty/ <int:pk>/',views.changeqty,name='changeqty'),
    #path('payments/',views.payments,name='payments'),
    path('jssignup/',views.jssignup,name='jssignup'),
    path('sucess/',views.sucess,name='sucess'),
    path('myorder/',views.myorder,name='myorder'),

]