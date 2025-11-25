from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import viewsets

from scraper.models import Opportunity
from scraper.scraper import run_scraper
from scraper.serializer import OpportunitySerializer

# API VIEWSET
class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.all().order_by('-id')
    serializer_class = OpportunitySerializer

# DASHBOARD
@login_required
def dashboard_page(request):
    total = Opportunity.objects.count()
    analyzed = Opportunity.objects.filter(analyzed=True).count()
    latest = Opportunity.objects.order_by('-scraped_at')[:10]

    return render(request, 'scraper/dashboard.html', {
        'total': total,
        'analyzed': analyzed,
        'latest': latest,
        'pending': total - analyzed,
    })

# RUN SCRAPER API
def run_scraper_api(request):
    if request.method == 'GET':
        return JsonResponse(run_scraper())
    return JsonResponse({'error': 'Only GET allowed'}, status=405)

# NEW PARTNERSHIP
@login_required
def new_partnership_page(request):
    if request.method == 'POST':
        # process form
        return redirect('dashboard_page')
    return render(request, 'scraper/new_partnership.html')

# ABOUT
def about_page(request):
    return render(request, 'scraper/about.html')

# HOME / ROOT
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard_page')
    return render(request, 'scraper/home.html')
