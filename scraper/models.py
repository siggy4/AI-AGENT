from django.db import models
from django_countries.fields import CountryField

# Create your models here.
class Opportunity(models.Model):
    id = models.AutoField(primary_key=True)
    source_name = models.CharField(max_length=100)
    title = models.TextField()
    url = models.URLField(unique=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    #country = CountryField(blank=True)
    active = models.BooleanField(default=True)
    deadline = models.DateField(blank=True, null=True)
    posted_date = models.DateField(blank=True, null=True)
    scraped_at = models.DateTimeField(auto_now_add=True)
    analyzed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


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

    # PDF File
    #pdf_file = models.FileField(upload_to='partnership_pdfs/', blank=True, null=True)
    #pdf_title = models.CharField(max_length=200, blank=True, null=True, help_text="Custom name for the PDF document")



class PartnershipPDF(models.Model):
    partnership = models.ForeignKey(
        Partnership,
        on_delete=models.CASCADE,
        related_name="pdfs"
    )
    file = models.FileField(upload_to="partnership_pdfs/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return self.file.name.split("/")[-1]

    def __str__(self):
        return self.filename()


    @property
    def pdf_display_name(self):
        """Return the custom PDF title or generate one from partnership details"""
        if self.pdf_title:
            return self.pdf_title
        elif self.pdf_file:
            return f"{self.partner_name or self.company} - Partnership Document"
        return None

    def has_pdf(self):
        """Check if partnership has an associated PDF"""
        return bool(self.pdf_file)

    def __str__(self):
        return f"{self.company} - {self.country}"

    # created_at = models.DateTimeField(auto_now_add=True)
    # source = models.CharField(max_length=200, blank=True, null=True)
    # office_location = models.CharField(max_length=200, blank=True, null=True)
    # comment = models.TextField(blank=True, null=True)
