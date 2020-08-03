"""front_end_code URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from front_end_main_app import views
from django.urls import path,include
from django.conf.urls import url
from django.views.generic.base import TemplateView


urlpatterns = [

    url(r'^$',views.index,name='index'),
    path('accounts/',include('django.contrib.auth.urls')),
    url(r'^input_form',views.patientForm,name='input_form'),
    url(r'^result', views.result),
    url(r'^status',views.status),
    url(r'^information/', TemplateView.as_view(template_name='information.html'), name='Information_page'),
    url(r'^what_is_sepsis', TemplateView.as_view(template_name='what_is_sepsis.html'),
        name='Information_page_what_is_sepsis'),
    url(r'^how_can_i_get_ahead_of_sepsis', TemplateView.as_view(template_name='get_ahead_from _sepsis.html'),
        name='Information_page_get_ahead_of_sepsis'),
    url(r'^sepsis_diagnosed_and_treatment', TemplateView.as_view(template_name='sepsis_treatment.html'),
        name='Information_page_sepsis_treatment'),
    url(r'^educational_info_pt', TemplateView.as_view(template_name='educational_info1.html'),
        name='Information_page_educational_info1'),
    url(r'^educational_info_pro', TemplateView.as_view(template_name='educational_info2.html'),
        name='Information_page_educational_info2'),
    url(r'^sepsis_data_and_reports', TemplateView.as_view(template_name='sepsis_data_and_reports.html'),
        name='Information_page_sepsis_data_and_reports'),

    path('admin/', admin.site.urls),
]
