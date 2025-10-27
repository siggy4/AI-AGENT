from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets

from scraper.models import Opportunity
from scraper.scraper import run_scraper
from scraper.serializer import OpportunitySerializer


# should  contain your viewsets
class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.all().order_by('-id')
    serializer_class = OpportunitySerializer


def landing_page(request):
    total = Opportunity.objects.count()
    # analyzed = Opportunity.objects.filter(analyzed=True).count()
    latest = Opportunity.objects.order_by('-scraped_at')[:10]

    context = {
        'total': total,
        'analyzed': total,
        'latest': latest,
    }
    return render(request, 'scraper/landing.html', context)


def run_scraper_api(request):
    def run_scraper_api(request):
        if request.method == 'GET':
            result = run_scraper()
            return JsonResponse(result)  # ✅ must return a response object
        else:
            return JsonResponse({'error': 'Only GET allowed'}, status=405)
