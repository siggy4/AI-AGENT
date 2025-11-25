# scraper/urls.py
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import run_scraper_api, home, dashboard_page, new_partnership_page, about_page

from scraper import views
from scraper.views import OpportunityViewSet

router = DefaultRouter()
router.register(r'opportunities', OpportunityViewSet, basename='opportunity')

urlpatterns = [
    path('api', include(router.urls)),
    path('run-scraper/', run_scraper_api, name='run_scraper_api'),
    path('', home, name='home'),
    path('dashboard/', dashboard_page, name='dashboard_page'),
    path('new/', new_partnership_page, name='new_partnership'),
    path('about/', about_page, name='about'),

    path('login/', auth_views.LoginView.as_view(template_name='home.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
