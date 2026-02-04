import os
from firecrawl import FirecrawlApp
from pydantic import BaseModel
from typing import List
from .models import Opportunity
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-0d3f0027ab614353a6256aefc731844a")


# 1. Define the structure you want Firecrawl to find
class TenderSchema(BaseModel):
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


class TenderList(BaseModel):
    tenders: List[TenderSchema]


def run_firecrawl_scraper():
    doc = firecrawl.scrape("https://tenders.go.ke/tenders", formats=["markdown", "html"])
    print(doc)
    target_url = "https://tenders.go.ke/tenders"

    # 2. Tell Firecrawl to scrape and extract based on your schema
    # This replaces all the BeautifulSoup 'find' and 'select' logic
    result = app.scrape_url(
        url=target_url,
        params={
            "formats": ["json"],
            "jsonOptions": {
                "schema": TenderList.model_json_schema()
            }
        }
    )

    scraped_count = 0

    # 3. Save to your Django Database
    if "json" in result:
        for item in result["json"]["tenders"]:
            # Standard Django duplicate check
            if not Opportunity.objects.filter(url=item['url']).exists():
                Opportunity.objects.create(
                    source_name="PPIP Kenya",
                    title=item['title'],
                    url=item['url'],
                    category=item['category']
                )
                scraped_count += 1

    return {"status": "success", "new_items": scraped_count}