# scraper/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from scraper import views
from scraper.views import OpportunityViewSet

router = DefaultRouter()
router.register(r'opportunities', OpportunityViewSet, basename='opportunity')

urlpatterns = [
    path('api', include(router.urls)),
    path('', views.landing_page, name='landing_page'),
]
