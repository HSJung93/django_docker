from django.urls import path
from . import views

app_name = 'shortner'

urlpatterns = [
    # path('', views.shortner, name='shortner' ),
    path('', views.create, name='create'),
    path('<slug:key>', views.go, name='go'),
]