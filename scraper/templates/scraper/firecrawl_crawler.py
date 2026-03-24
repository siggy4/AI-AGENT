from firecrawl import Crawler
from bs4 import BeautifulSoup
from models import Opportunity

class TenderSpider(Crawler):
    start_urls = [
        "https://www.kenyatenders.com/"  # Replace with actual tender aggregator list
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        # Find tender links on the list page
        for link_tag in soup.find_all("a", href=True):
            if "tender" in link_tag["href"]:
                url = link_tag["href"]

                # Follow the tender detail page
                yield self.follow(url, self.parse_detail)

    def parse_detail(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1").text.strip() if soup.find("h1") else ""
        organization = ""
        deadline = ""
        description = ""

        for li in soup.find_all("li"):
            text = li.text
            if "Deadline" in text:
                deadline = text.split(":")[-1].strip()
            if "Financier" in text:
                organization = text.split(":")[-1].strip()

        desc_block = soup.find("div", string=lambda x: x and "Description" in x)
        if desc_block:
            p = desc_block.find_next("p")
            description = p.text.strip() if p else ""

        # Save tender to Django DB
        Opportunity.objects.get_or_create(
            title=title,
            source_url=response.url,
            defaults={
                "organization": organization,
                "deadline": deadline,
                "description": description,
            }
        )