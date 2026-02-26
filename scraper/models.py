from django.db import models
from django_countries.fields import CountryField

# Create your models here.
class Opportunity(models.Model):
    id = models.AutoField(primary_key=True)
    source_name = models.CharField(max_length=100)
    title = models.TextField()
    url = models.URLField(unique=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    country = CountryField(blank=True)
    active = models.BooleanField(default=True)
    deadline = models.DateField(blank=True, null=True)
    posted_date = models.DateField(blank=True, null=True)
    scraped_at = models.DateTimeField(auto_now_add=True)
    analyzed = models.BooleanField(default=False)


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
    partnership_type = models.CharField(max_length=50, choices=PARTNERSHIP_TYPE_CHOICES)
    start_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    is_manual = models.BooleanField(default=True)  # Flag for manual entry
    country = CountryField(blank=True)
    company = models.CharField(max_length=255)
    meeting_date = models.DateField(blank=True, null=True)
    followup_date = models.DateField(blank=True, null=True)
    comment = models.TextField(blank=True, default='')
    meeting_type = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    reached = models.CharField(max_length=50)
    method = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.partner_name


 
    #created_at = models.DateTimeField(auto_now_add=True)
    #source = models.CharField(max_length=200, blank=True, null=True)
    #office_location = models.CharField(max_length=200, blank=True, null=True)
    #comment = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.company} - {self.country}"

    def __str__(self):
        return f"{self.company} - {self.country}"

    def __str__(self):
        return self.title
