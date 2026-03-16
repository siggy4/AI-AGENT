import os
from firecrawl import FirecrawlApp
from pydantic import BaseModel
from typing import List
from .models import Opportunity, Interest, Partnership

firecrawl = FirecrawlApp(api_key="fc-0d3f0027ab614353a6256aefc731844a")


# 1. Define the structure you want Firecrawl to find
class TenderSchema(BaseModel):
    source: str
    title: str
    url: str
    category: str = ""
    country: str = ""
    active: bool = True
    deadline: str = ""
    posted_date: str = ""
    analyzed: bool = False


class TenderList(BaseModel):
    tenders: List[TenderSchema]



def run_scraper():
 pass
def run_firecrawl_scraper():

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