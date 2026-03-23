from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Partnership)
admin.site.register(PartnershipPDF)
admin.site.register(Opportunity)
admin.site.register(Interest)
admin.site.register(CV)
admin.site.register(PastPerformance)
admin.site.register(ProposalDraft)
admin.site.register(SupportingDocument)
admin.site.register(SubmissionAudit)