# scraper/services.py
import requests
from bs4 import BeautifulSoup
from models import Opportunity



def scrape_undp_tenders():
    url = "https://www.kenyatenders.com/tender/individual-consultant-environmental-policy-specialist-7112512.php"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Title
    title = soup.find("h1").text.strip()

    # Extract list items
    details = soup.find_all("li")

    deadline = ""
    organization = ""

    for item in details:
        text = item.text

        if "Deadline" in text:
            deadline = text.split(":")[-1].strip()

        if "Financier" in text:
            organization = text.split(":")[-1].strip()

    # Description
    description_block = soup.find("div", string=lambda x: x and "Description" in x)

    description = ""
    if description_block:
        description = description_block.find_next("p").text.strip()

    return {
        "title": title,
        "deadline": deadline,
        "organization": organization,
        "description": description,
        "url": url
    }



def save_undp_tender():
    tender = scrape_undp_tenders()

    Opportunity.objects.get_or_create(
        title=tender["title"],
        source_url=tender["url"],
        defaults={
            "organization": tender["organization"],
            "deadline": tender["deadline"],
            "description": tender["description"]
        }
    )