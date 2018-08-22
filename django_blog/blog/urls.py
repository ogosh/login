from django.conf.urls import url
from .import views

urlpatterns = [
    url (r'^login/$', views.user_login, name='login'),
    url(r'^email_sign_up/', views.email_sign_up, name='email_sign_up'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),

]
