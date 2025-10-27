import requests
from bs4 import BeautifulSoup
from .models import Opportunity


def run_scraper():
    url = "https://tenders.go.ke"  # replace later
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    scraped = 0

    for item in soup.select(".opportunity"):  # example selector
        title = item.text.strip()
        link = item.get("href")

        if not Opportunity.objects.filter(url=link).exists():
            Opportunity.objects.create(
                source_name="Example Source",
                title=title,
                url=link,
                category="RFP"
            )
            scraped += 1

    return {"message": f"{scraped} new opportunities scraped."}
