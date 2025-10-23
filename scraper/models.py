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

    def __str__(self):
        return self.title