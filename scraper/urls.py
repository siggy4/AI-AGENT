# scraper/urls.py
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import opportunities_page, run_scraper_api, home, dashboard_page, new_partnership_page, about_page, \
    partnerships_list, opportunities_list, new_opportunities, update_partnership, update_partnership_details, delete_partnership
from .views import create_partnership_api
from .views import manual_partnerships, edit_partnership

from scraper import views
from scraper.views import OpportunityViewSet
from .views import upload_pdf, view_pdf, delete_pdf


router = DefaultRouter()
router.register(r'opportunities', OpportunityViewSet, basename='opportunity')

urlpatterns = [
    path('api/partnerships/', views.create_partnership_api, name='create_partnership_api'),
    path('api/', include(router.urls)),
    path('run-scraper/', run_scraper_api, name='run_scraper_api'),
    path('', home, name='home'),
  

    path('dashboard/', dashboard_page, name='dashboard_page'),
    path('new/', new_partnership_page, name='new_partnership'),
    path('list/', partnerships_list, name='partnerships'),
    path('update_partnership/<int:pk>/', views.update_partnership, name='update_partnership'),
    path('update-partnership-details/<int:pk>/', views.update_partnership_details, name='update_partnership_details'),
  

    # opportunity detail view
    path('opportunities/', opportunities_page, name='opportunities_page'),
    path('opportunity_list/', opportunities_list, name='opportunities'),
    path('new_opportunity/', new_opportunities, name='new_opportunities'),
    path('scap_opportunities/', run_scraper_api, name='scrap_opportunities'),

    path('about/', about_page, name='about'),
    path('login/', auth_views.LoginView.as_view(template_name='scraper/home.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Partnership
    path('manual/', views.manual_partnerships, name='manual_partnerships'),
    path('edit/<int:pk>/', views.edit_partnership, name='edit_partnership'),
    path("partnership/delete/<int:pk>/",views.delete_partnership,name="delete_partnership"),



    # PDF Management URLs
    path("upload_pdf/<int:pk>/", views.upload_pdf, name="upload_pdf"),
    path( "view-pdf/<int:pdf_id>/",views.view_pdf,name="view_pdf"),
    path("delete-pdf/<int:pdf_id>/",views.delete_pdf,name="delete_pdf"),


    ]
