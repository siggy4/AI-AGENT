# scraper/urls.py
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import opportunities_page, run_scraper_api, home, dashboard_page, new_partnership_page,partnerships_list, opportunities_list, new_opportunities, update_partnership, delete_partnership, about_page 
from .views import create_partnership_api
from .views import  edit_partnership,partnerships_list, opportunities_list, new_opportunities, add_interest, remove_interest, update_interest


from scraper import views
from scraper.views import OpportunityViewSet
from .views import upload_pdf, view_pdf, delete_pdf


router = DefaultRouter()
router.register(r'opportunities', OpportunityViewSet, basename='opportunity')

urlpatterns = [
    path('api/', include(router.urls)),
    path('run-scraper/', run_scraper_api, name='run_scraper_api'),
    path('', home, name='home'),

    path('dashboard/', dashboard_page, name='dashboard_page'),
    path('new/', new_partnership_page, name='new_partnership'),
    path('list/', partnerships_list, name='partnerships'),
    path('update_partnership/<int:pk>/', views.update_partnership, name='update_partnership'),


    # opportunity detail view
    path('opportunities/', opportunities_page, name='opportunities_page'),
    path('opportunity_list/', opportunities_list, name='opportunities'),
    path('new_opportunities/', new_opportunities, name='new_opportunities'),
    path('scap_opportunities/', run_scraper_api, name='scrap_opportunities'),
    
    # interest management
    path('add-interest/<int:opportunity_id>/', add_interest, name='add_interest'),
    path('remove-interest/<int:interest_id>/', remove_interest, name='remove_interest'),
    path('update-interest/<int:interest_id>/', update_interest, name='update_interest'),

    path('about/', about_page, name='about'),
    path('login/', auth_views.LoginView.as_view(template_name='scraper/home.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Partnership
    path('edit/<int:pk>/', views.edit_partnership, name='edit_partnership'),
    path("partnership/delete/<int:pk>/",views.delete_partnership,name="delete_partnership"),
    path('partnerships/bulk-delete/', views.bulk_delete, name='bulk_delete_partnerships'),


    # PDF Management URLs
    path("upload_pdf/<int:pk>/", views.upload_pdf, name="upload_pdf"),
    path( "view-pdf/<int:pdf_id>/",views.view_pdf,name="view_pdf"),
    path("delete-pdf/<int:pdf_id>/",views.delete_pdf,name="delete_pdf"),


    ]

