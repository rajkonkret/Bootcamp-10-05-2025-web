from django.urls import path
# urls.py w aplikacji
from .views import home

urlpatterns = [
    path('', home, name="home")  # endpoint '/'
]
