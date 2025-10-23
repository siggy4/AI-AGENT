from django.shortcuts import render
from rest_framework import viewsets

from scraper.models import Opportunity
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