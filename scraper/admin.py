from django.contrib import admin

# Register your models here.
from .models import Partnership, PartnershipPDF, Opportunity

admin.site.register(Partnership)
admin.site.register(PartnershipPDF)
admin.site.register(Opportunity)
