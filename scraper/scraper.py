import os
from unittest import result
from firecrawl import FirecrawlApp
from firecrawl.types import ScrapeOptions
from pydantic import BaseModel
from typing import List
from .models import Opportunity, Interest, Partnership
from .models import Tender
from datetime import datetime



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



def run_firecrawl_scraper():
    target_url = "https://tenders.go.ke/tenders"

    scrape_opts = ScrapeOptions(
        only_main_content=False,
        max_age=600000,
        parsers=["pdf"],
        formats=["markdown"]
    )

    try:
        # Perform the crawl
        result = firecrawl.crawl(
            url=target_url,
            limit=1,
            scrape_options=scrape_opts,
        )

        # Transform raw result into structured data
        # Example: list of dicts with title, link, deadline, org
        items = []
        for r in result:  # adjust according to your Firecrawl output
            items.append({
                "title": r.get("title", ""),
                "link": r.get("link", ""),
                "deadline": r.get("deadline", None),
                "organization": r.get("organization", "")
            })

        return {"status": "success", "items": items}

    except Exception as e:
        return {"status": "error", "message": str(e)}

  
    



def save_tenders_to_db(items):
    for item in items:
        # Convert deadline to date object if needed
        deadline = None
        if item.get("deadline"):
            try:
                deadline = datetime.strptime(item["deadline"], "%Y-%m-%d").date()
            except:
                pass

        # Save or update based on unique link
        Tender.objects.update_or_create(
            link=item["link"],
            defaults={
                "title": item.get("title", ""),
                "deadline": deadline,
                "organization": item.get("organization", ""),
            }
        )


def run_scraper():
    """Legacy function name for backward compatibility"""
    return run_firecrawl_scraper()