# scraper/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import run_scraper_api

from scraper import views
from scraper.views import OpportunityViewSet

router = DefaultRouter()
router.register(r'opportunities', OpportunityViewSet, basename='opportunity')

urlpatterns = [
    path('api', include(router.urls)),
    path('', views.landing_page, name='landing_page'),
    path('run-scraper/', run_scraper_api, name='run_scraper_api'),
]
