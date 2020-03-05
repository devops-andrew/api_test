from django.urls import path
from .views      import MissionView 

urlpatterns = [
    path('', MissionView.as_view()),
]
