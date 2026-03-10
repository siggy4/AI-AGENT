from django.db import models


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
