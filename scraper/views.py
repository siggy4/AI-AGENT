import django.contrib.gis.geoip2.resources
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import viewsets

from scraper.models import Opportunity, Partnership
from scraper.scraper import run_scraper
from scraper.serializer import OpportunitySerializer
import pycountry

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Partnership
from .forms import PartnershipForm
from django.contrib import messages

from django.http import JsonResponse
from .models import Partnership
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


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

    opportunities = Opportunity.objects.all().order_by('-id')
    return render(request, 'scraper/opportunities.html', {
        'total_opportunities': total,
        'total_analyzed': analyzed,
        'latest': latest,

        'opportunities': opportunities
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
        form = PartnershipForm(request.POST, request.FILES)  # NOTE: request.FILES for file upload
        if form.is_valid():
            partnership = form.save(commit=False)
            partnership.is_manual = True
            partnership.save()
            return redirect('dashboard_page')  # or wherever you want
    else:
        form = PartnershipForm()

    return render(request, 'scraper/new_partnership.html', {'form': form})

    countries = [country.name for country in pycountry.countries]

    return render(request, 'scraper/new_partnership.html', {
        'form': form,
        'countries': countries
    })

def manual_partnerships(request):
    partnerships = Partnership.objects.filter(is_manual=True)
    return render(request, "scraper/manual_partnership.html", {
        "partnerships": partnerships
    })

# ABOUT
def about_page(request):
    return render(request, 'scraper/about.html')


# HOME / ROOT
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard_page')
    return render(request, 'scraper/home.html')




#new partnership pGE
def create_partnership_api(request):
    if request.method == "POST":
        form = PartnershipForm(request.POST)
        if form.is_valid():
            partnership = form.save(commit=False)
            partnership.is_manual = True
            partnership.save()
            return JsonResponse({"status": "success", "id": partnership.id})
        return JsonResponse({"status": "error", "errors": form.errors}, status=400)
    return JsonResponse({"status": "error", "message": "POST required"}, status=405)

#delete/edit partnership
from django.shortcuts import get_object_or_404

def edit_partnership(request, pk):
    partnership = get_object_or_404(Partnership, pk=pk)
    form = PartnershipForm(request.POST or None, instance=partnership)
    if form.is_valid():
        form.save()
        return redirect('manual_partnerships')
    return render(request, "scraper/edit_partnership.html", {"form": form})


#update partnership
def update_partnership_details(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            p = Partnership.objects.get(pk=pk)

            # Convert string to date if provided
            meeting_date_str = data.get('meeting_date')
            followup_date_str = data.get('followup_date')

            p.meeting_date = datetime.strptime(meeting_date_str, '%Y-%m-%d').date() if meeting_date_str else None
            p.followup_date = datetime.strptime(followup_date_str, '%Y-%m-%d').date() if followup_date_str else None

            p.meeting_type = data.get('meeting_type') or None
            p.comment = data.get('comment') or ''
            p.save()

            return JsonResponse({'success': True})
        except Partnership.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Partnership not found'})
        except ValueError as ve:
            # This catches invalid date formats
            return JsonResponse({'success': False, 'error': f'Invalid date format: {ve}'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

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
    # pass countries from a lib to template for rendering
    countries = [(country.name) for country in pycountry.countries]

#delete partnerships
@login_required
def delete_selected_partnerships(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_partnerships')
        if not selected_ids:
            messages.warning(request, "No partnerships selected for deletion.")
            return redirect('partnerships')

        # Delete the selected partnerships
        Partnership.objects.filter(id__in=selected_ids).delete()
        messages.success(request, f"{len(selected_ids)} partnership(s) deleted successfully.")
        return redirect('partnerships')

    # If GET request, just redirect
    return redirect('partnerships')
    
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



