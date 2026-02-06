import os
from typing import List
from pydantic import BaseModel
from firecrawl import Firecrawl
from django.conf import settings
from .models import Opportunity


# Firecrawl client (env-based)
firecrawl = Firecrawl(api_key=settings.FIRECRAWL_API_KEY)


# ---------- Pydantic schemas (JSON only) ----------

class TenderSchema(BaseModel):
    title: str
    url: str
    category: str | None = None
    country: str | None = None
    deadline: str | None = None
    posted_date: str | None = None


class TenderList(BaseModel):
    tenders: List[TenderSchema]


# ---------- Scraper logic ----------

def run_firecrawl_scraper():
    target_url = "https://tenders.go.ke/tenders"

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

    if "json" not in result:
        return {"status": "failed", "reason": "No JSON returned"}

    for item in result["json"]["tenders"]:
        if not Opportunity.objects.filter(url=item["url"]).exists():
            Opportunity.objects.create(
                source_name="PPIP Kenya",
                title=item["title"],
                url=item["url"],
                category=item.get("category"),
                country=item.get("country"),
            )
            scraped_count += 1

    return {
        "status": "success",
        "new_items": scraped_count
    }
