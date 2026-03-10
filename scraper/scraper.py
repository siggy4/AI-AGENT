import os
from firecrawl import FirecrawlApp
from pydantic import BaseModel
from typing import List
from .models import Opportunity
<<<<<<< HEAD
from firecrawl import Firecrawl
#from django.db import models
=======
>>>>>>> asc

firecrawl = FirecrawlApp(api_key="fc-0d3f0027ab614353a6256aefc731844a")


# 1. Define the structure you want Firecrawl to find
class TenderSchema(BaseModel):
<<<<<<< HEAD
    id: int | None = None
    source_name: str
    title: str
    url: str
    category: str | None = None
    country: str | None = None
    active: bool = True
    deadline: str | None = None
    posted_date: str | None = None
    scraped_at: str | None = None
=======
    source_name: str
    title: str
    url: str
    category: str = ""
    country: str = ""
    active: bool = True
    deadline: str = ""
    posted_date: str = ""
>>>>>>> asc
    analyzed: bool = False


class TenderList(BaseModel):
    tenders: List[TenderSchema]

<<<<<<< HEAD
def run_scraper():
    doc = firecrawl.scrape("https://tenders.go.ke/tenders", formats=["markdown", "html"])
    print(doc)
=======

def run_firecrawl_scraper():
>>>>>>> asc
    target_url = "https://tenders.go.ke/tenders"

    # 2. Tell Firecrawl to scrape and extract based on your schema
    # This replaces all the BeautifulSoup 'find' and 'select' logic
    result = firecrawl.scrape_url(
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


def run_scraper():
    """Legacy function name for backward compatibility"""
    return run_firecrawl_scraper()