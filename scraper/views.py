import django.contrib.gis.geoip2.resources
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import viewsets

from scraper.models import Opportunity, Partnership
from scraper.scraper import run_scraper
from scraper.serializer import OpportunitySerializer
import pycountry


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
    total_partnerships = Partnership.objects.count()
    total_partnerships_contacted = Partnership.objects.exclude(reached='Not Contacted').count()

    return render(request, 'scraper/dashboard.html', {
        'total_partnerships': total_partnerships,
        'total_partnerships_contacted': total_partnerships_contacted,
        'not_contacted': total_partnerships - total_partnerships_contacted,
        'partnership_completion_rate': (total_partnerships_contacted / total_partnerships * 100).__round__(
            0) if total_partnerships_contacted > 0 else 0,
    })


# OPPORTUNITIES PAGE
@login_required
def opportunities_page(request):
    total = Opportunity.objects.count()
    analyzed = Opportunity.objects.filter(analyzed=True).count()
    latest = Opportunity.objects.order_by('-scraped_at')[:10]
    return render(request, 'scraper/opportunities.html', {
        'total': total,
        'analyzed': analyzed,
        'latest': latest,
    })


def opportunities_list(request):
    flt = request.GET.get("filter")
    opportunities = Opportunity.objects.all().order_by('-id')
    if flt == "analyzed":
        opportunities = opportunities.filter(analyzed=True)

    return render(request, 'scraper/opportunities_list.html', {
        'opportunities': opportunities,
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
        # process form and save the data to the database
        Partnership.objects.create(
            country=request.POST.get('country'),
            company=request.POST.get('company'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            reached=request.POST.get('reached'),
            method=request.POST.get('method'),
            notes=request.POST.get('notes', ''),
        )

        return redirect('dashboard_page')
    # pass countries from a lib to template for rendering
    countries = [(country.name) for country in pycountry.countries]
    return render(request, 'scraper/new_partnership.html', {
        'countries': countries,
    })


# ABOUT
def about_page(request):
    return render(request, 'scraper/about.html')


# HOME / ROOT
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard_page')
    return render(request, 'scraper/home.html')


# partnerships list
@login_required
def partnerships_list(request):
    flt = request.GET.get("filter")

    if flt == "contacted":
        partnerships = Partnership.objects.filter(reached="Reached")
        title = "Contacted Companies"

    elif flt == "not_contacted":
        partnerships = Partnership.objects.filter(reached="Not Contacted")
        title = "Not Contacted Companies"

    else:
        partnerships = Partnership.objects.all().order_by("-id")
        title = "All Companies"

    return render(request, "scraper/partnerships_list.html", {
        "partnerships": partnerships,
        "title": title,
    })


# update partnerships
def update_partnership(request, pk):
    partnership = Partnership.objects.get(id=pk)

    if request.method == "POST":
        partnership.reached = request.POST.get("reached")
        partnership.method = request.POST.get("method")
        partnership.notes = request.POST.get("notes")
        partnership.save()
        return redirect("partnerships")

    return render(request, "scraper/update_partnership.html", {
        "p": partnership
    })
