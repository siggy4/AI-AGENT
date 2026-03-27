from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField


# Create your models here.
class Opportunity(models.Model):
    id = models.AutoField(primary_key=True)
    source_name = models.CharField(max_length=100)
    title = models.TextField()
    url = models.URLField(unique=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    active = models.BooleanField(default=True)
    deadline = models.DateField(blank=True, null=True)
    posted_date = models.DateField(blank=True, null=True)
    scraped_at = models.DateTimeField(auto_now_add=True)
    analyzed = models.BooleanField(default=False)
    workplan_status = models.CharField(
        max_length=50,
        choices=[
            ('not_started', 'Not Started'),
            ('drafting', 'Drafting'),
            ('review', 'Under Review'),
            ('finalized', 'Finalized')
        ],
        default='not_started'
    )

    submission_status = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = RichTextField(blank=True)
    deadline = models.CharField(max_length=100, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.title



class Interest(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='interests')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('interested', 'Interested'),
        ('contacted', 'Contacted'),
        ('applied', 'Applied'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ], default='interested')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['opportunity', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.opportunity.title[:50]}"


class Partnership(models.Model):

    PARTNERSHIP_TYPE_CHOICES = [
        ('Strategic', 'Strategic'),
        ('Referral', 'Referral'),
        ('Integration', 'Integration'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    
    REACHED_CHOICES = [
        ('Not Contacted', 'Not Contacted'),
        ('Reached', 'Reached'),
    ]

    reached = models.CharField(
        max_length=20,
        choices=REACHED_CHOICES,
        default='Not Contacted'
    )
    
    partnership_type = models.CharField(
        max_length=50,
        choices=PARTNERSHIP_TYPE_CHOICES,
        null=True,
        blank=True
    )
    
    # NEW: Meeting Type (Physical or Virtual)
    meeting_type = models.CharField(
        max_length=20,
        choices=[
            ('Physical', 'Physical'),
            ('Virtual', 'Virtual')
        ],
        blank=True,
        null=True
    )
    
    partner_name = models.CharField(max_length=255, null=True, blank=True)
    point_of_contact = models.CharField(max_length=255, null=True, blank=True) # or EmailField
    start_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    is_manual = models.BooleanField(default=True)  # Flag for manual entry
    country = models.CharField(max_length=50, blank=True, null=True)
    #country = CountryField(blank=True)
    company = models.CharField(max_length=255)
    meeting_date = models.DateField(blank=True, null=True)
    followup_date = models.DateField(blank=True, null=True)
    comment = models.TextField(blank=True, default='')
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    method = models.CharField(max_length=50, null=True, blank=True)
    notes = models.TextField(blank=True, default='')
    source = models.CharField(max_length=20, choices=[
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
        ('events', 'Events'),
        ('institutional', 'Institutional'),
        ('internal', 'Internal'),
    ],blank=True, null=True)


class PartnershipPDF(models.Model):
    partnership = models.ForeignKey(Partnership,on_delete=models.CASCADE,related_name="pdfs")
    file = models.FileField(upload_to="partnership_pdfs/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return self.file.name.split("/")[-1]

    def __str__(self):
        return self.filename()


    country = models.CharField(max_length=100)
    company = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    reached = models.CharField(max_length=50)
    method = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company} - {self.country}"



class CV(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name="cvs")

    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)

    file = models.FileField(upload_to='cvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class PastPerformance(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name="past_performance")

    title = models.CharField(max_length=255)

    document = models.FileField(upload_to='past_performance/')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class ProposalDraft(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name="drafts")

    version = models.IntegerField()

    file = models.FileField(upload_to='proposal_drafts/')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-version']      

def save(self, *args, **kwargs):
    if not self.version:
        last = ProposalDraft.objects.filter(
            opportunity=self.opportunity
        ).order_by('-version').first()

        self.version = 1 if not last else last.version + 1

    super().save(*args, **kwargs)



class SupportingDocument(models.Model):

    CATEGORY_CHOICES = [
        ('budget', 'Budget'),
        ('legal', 'Legal'),
        ('technical', 'Technical'),
        ('financial', 'Financial'),
        ('other', 'Other'),
    ]

    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name="support_docs")

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    title = models.CharField(max_length=255)

    document = models.FileField(upload_to='supporting_docs/')

    uploaded_at = models.DateTimeField(auto_now_add=True)   


class SubmissionAudit(models.Model):

    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name="audit")

    status = models.CharField(max_length=100)

    notes = models.TextField(blank=True)

    source_url = models.URLField(blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    user = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.opportunity.title} - {self.status}"
    

class Tender(models.Model):
    title = models.CharField(max_length=500)
    link = models.URLField()
    deadline = models.DateField(null=True, blank=True)
    organization = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title