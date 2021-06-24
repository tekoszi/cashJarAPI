"""Jarapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jar', views.post_jar),
    path('jars', views.get_jars),
    path('withdraw', views.withdraw),
    path('cashin', views.cashin),
    path('transactions', views.get_transactions),
    path('transactions/<int:jar_id>', views.get_transactions),
    path('transactions/<int:jar_id>/<str:order_by>', views.get_transactions),
    path('transactions/<int:jar_id>/<str:order_by>/<str:order>', views.get_transactions),
    path('transactions/<str:order_by>', views.get_transactions),
    path('transactions/<str:order_by>/<str:order>', views.get_transactions),
    path('transfer', views.transfer),
]
