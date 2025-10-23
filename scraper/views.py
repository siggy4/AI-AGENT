from django.shortcuts import models

class Opportunity(models.Model):
    source_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.TextField()
    url = models.URLField(unique=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    posted_date = models.DateField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    scraped_at = models.DateTimeField(auto_now_add=True)
    analyzed = models.BooleanField(default=False)

    def __str__(self):
        return self.title[:120]

