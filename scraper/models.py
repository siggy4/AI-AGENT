from django.db import models

# Create your models here.
class Opportunity(models.Model):
    source_name = models.CharField(max_length=100)
    title = models.TextField()
    url = models.URLField(unique=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    posted_date = models.DateField(blank=True, null=True)
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title