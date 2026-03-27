
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
import os

from scraper.models import Opportunity, Partnership
from scraper.scraper import run_scraper
from scraper.serializer import OpportunitySerializer
import pycountry

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Partnership,PartnershipPDF
from .forms import PartnershipForm, PDFUploadForm
from django.contrib import messages

import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.views.decorators.http import require_POST

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Opportunity, Partnership, Interest
import pycountry
from django.contrib.auth.decorators import login_required
from scraper.serializer import OpportunitySerializer
import pycountry
from rest_framework import viewsets
from django.utils import timezone
from django.contrib.gis.geoip2 import GeoIP2
from ckeditor.fields import RichTextField

from django.http import JsonResponse
from .scraper import save_tenders_to_db



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

    opportunities = Opportunity.objects.all().order_by('-id')
    countries = [(country.name) for country in pycountry.countries]


    countries = [(country.name) for country in pycountry.countries]
    
    # Define categories
    categories = [
        'Expression of Interest',
        'Request for Proposal', 
        'Grants',
        'Invitation to Bid',
        'Grant Support',
        'Call for Individual',
        'Call for Implementing Partners',
        'Others'
    ]
    
    # Get filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category_filter = request.GET.get('category')
    country_filter = request.GET.get('country')
    
    # Base queryset
    opportunities = Opportunity.objects.all().order_by('-id')
    
    # Apply date filtering
    if start_date:
        opportunities = opportunities.filter(posted_date__gte=start_date)
    if end_date:
        opportunities = opportunities.filter(posted_date__lte=end_date)
    
    # Apply category filtering
    if category_filter:
        opportunities = opportunities.filter(category__iexact=category_filter)
    
    # Apply country filtering
    if country_filter:
        opportunities = opportunities.filter(country__iexact=country_filter)
    
    latest = opportunities[:10]  # Get latest from filtered results
    
    # Get user's interests
    user_interests = Interest.objects.filter(user=request.user).select_related('opportunity').order_by('-created_at')
    
    # Calculate submission statistics
    total_submissions = user_interests.count()
    pending_submissions = user_interests.filter(status='interested').count()
    submitted_submissions = user_interests.filter(status='applied').count()
    failed_submissions = user_interests.filter(status='rejected').count()
    
    # Calculate response statistics (based on contact status)
    total_responses = user_interests.filter(status__in=['contacted', 'applied', 'rejected']).count()
    positive_responses = user_interests.filter(status='applied').count()  # Applied = positive response
    negative_responses = user_interests.filter(status='rejected').count()  # Rejected = negative response
    pending_responses = user_interests.filter(status='contacted').count()  # Contacted = pending response
    

    return render(request, 'scraper/opportunities.html', {
        'total_opportunities': total,
        'total_analyzed': analyzed,
        'latest': latest,


        'opportunities': opportunities,
        'countries': countries,
        'opportunities': opportunities,
        'countries': countries,
        'categories': categories,
        'user_interests': user_interests,
        'total_submissions': total_submissions,
        'pending_submissions': pending_submissions,
        'submitted_submissions': submitted_submissions,
        'failed_submissions': failed_submissions,
        'total_responses': total_responses,
        'positive_responses': positive_responses,
        'negative_responses': negative_responses,
        'pending_responses': pending_responses,

    })


def opportunities_list(request):
    flt = request.GET.get("filter")
    opportunities = Opportunity.objects.all().order_by('-id')
    if flt == "analyzed":
        opportunities = opportunities.filter(analyzed=True)
    
    title = "All Opportunities" if flt != "analyzed" else "Analyzed Opportunities"

    return render(request, 'scraper/opportunities_list.html', {
        'opportunities': opportunities,
        'title': title,
    })

def opportunity_list(request):
    opportunities = Opportunity.objects.all().order_by('-created_at')

    return render(request, 'opportunities/list.html', {
        'opportunities': opportunities
    })

def new_opportunities(request):
    if request.method =='POST':
        #process form and save the data to the database
        Opportunity.objects.create(
            source_name=request.POST.get('company'),   
            title=request.POST.get('Title'),
            url=request.POST.get('url'),
            category=request.POST.get('Category'),
            country=request.POST.get('country'),
            active=request.POST.get('active') == 'Active',
            deadline=request.POST.get('Deadline') or None,
            posted_date=request.POST.get('Posted Date') or None,
            analyzed=request.POST.get('analyzed') == 'Analyzed',
        )
        return redirect('opportunities_page')
    
    # pass countries from a lib to template for rendering
    countries = [(country.name) for country in pycountry.countries]
    return render(request, 'scraper/opportunities.html', {
        'countries': countries,
    })


def run_scraper_api(request):
    if request.method == "GET":
        # Step 1: Run scraper
        data = run_scraper()

        # Step 2: If successful, save to DB
        if data.get("status") == "success":
            save_tenders_to_db(data.get("items", []))
            return JsonResponse({"status": "success", "message": "Tenders scraped and saved to DB"})

        # If scraper failed
        return JsonResponse({"status": "error", "message": data.get("message")}, status=500)

    return JsonResponse({"error": "Only GET allowed"}, status=405)

# NEW PARTNERSHIP
@login_required
def new_partnership_page(request):
    if request.method == 'POST':
        # process form and save the data to the database
        Partnership.objects.create(
            country=request.POST.get('country'),
            company=request.POST.get('company'),
            source=request.POST.get('source'),
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

def edit_partnership(request, pk):
    partnership = get_object_or_404(Partnership, pk=pk)
    form = PartnershipForm(request.POST or None, instance=partnership)
    if form.is_valid():
        form.save()
        return redirect('manual_partnerships')
    return render(request, "scraper/edit_partnership.html", {"form": form})

# Interest Management Views
@require_POST
@login_required
def add_interest(request, opportunity_id):
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)
    
    # Check if interest already exists
    if Interest.objects.filter(opportunity=opportunity, user=request.user).exists():
        return JsonResponse({'success': False, 'error': 'Already interested in this opportunity'})
    
    # Create new interest
    Interest.objects.create(
        opportunity=opportunity,
        user=request.user,
        status='interested'
    )
    
    return JsonResponse({'success': True})


@require_POST
@login_required
def remove_interest(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id, user=request.user)
    interest.delete()
    
    return JsonResponse({'success': True})



@require_POST
@login_required
def update_interest(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id, user=request.user)
    
    try:
        import json
        data = json.loads(request.body)
        new_status = data.get('status')
        
        if new_status in ['interested', 'contacted', 'applied', 'rejected', 'withdrawn']:
            interest.status = new_status
            interest.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid status'})
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'success': False, 'error': 'Invalid request'})


# partnerships list
@login_required
def partnerships_list(request):
    flt = request.GET.get("filter")
    
    # pass countries from a lib to template for rendering
    countries = [(country.name) for country in pycountry.countries]
    
    # Calculate statistics for cards
    total_partnerships = Partnership.objects.count()
    total_partnerships_contacted = Partnership.objects.filter(reached="Reached").count()
    not_contacted = Partnership.objects.filter(reached="Not Contacted").count()

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
        "countries": countries,
    })

#delete partnerships
@require_POST
def delete_partnership(request, pk):

    partnership = get_object_or_404(Partnership, pk=pk)

    if request.method == "POST":
        partnership.delete()
        #"total_partnerships": total_partnerships,
        #"total_partnerships_contacted": total_partnerships_contacted,
        #"not_contacted": not_contacted,

    return redirect("partnerships")

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

#partnership detail 
def partnership_detail(request, partnership_id):
    """Display partnership details with PDF management"""
    partnership = get_object_or_404(Partnership, id=partnership_id)
    context = {
        'partnership': partnership,
        'upload_form': PartnershipPDFForm(instance=partnership)
    }
    return render(request, 'scraper/partnerships_list.html', context)


# Bulk delete partnerships 
def bulk_delete(request):

    if request.method == "POST":

        data = json.loads(request.body)
        ids = data.get("ids", [])

        Partnership.objects.filter(id__in=ids).delete()

        return JsonResponse({"success": True})

#upload pdf
@csrf_exempt
def upload_pdf(request, pk):
    if request.method == "POST":
        partnership = get_object_or_404(Partnership, pk=pk)
        files = request.FILES.getlist("files")  # matches input name="files"

        if not files:
            return JsonResponse({"success": False, "error": "No files uploaded"})

        saved = []
        for f in files:
            pdf = PartnershipPDF.objects.create(partnership=partnership, file=f)
            saved.append({
                "id": pdf.id,
                "url": pdf.file.url,
                "name": pdf.filename()
            })
    return redirect("partnerships")



# View PDF content (for iframe)
def view_pdf(request, pdf_id):
    pdf = get_object_or_404(PartnershipPDF, id=pdf_id)
    try:
        return FileResponse(pdf.file.open('rb'), content_type='scraper/pdf', filename=pdf.filename())
    except FileNotFoundError:
        return JsonResponse({'success': False, 'error': 'PDF not found'})

# Delete PDF (AJAX)
@csrf_exempt
def delete_pdf(request, pdf_id):
    if request.method == "POST":
        pdf = get_object_or_404(PartnershipPDF, id=pdf_id)
        # Delete file from storage
        if pdf.file and os.path.isfile(pdf.file.path):
            os.remove(pdf.file.path)
        pdf.delete()
        return redirect("partnerships")


def mark_submitted(self):
    self.submission_status = True
    self.submitted_at = timezone.now()
    self.save()