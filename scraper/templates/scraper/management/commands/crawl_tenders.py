from django.core.management.base import BaseCommand
from scraper.firecrawl_crawler import TenderSpider

class Command(BaseCommand):
    help = "Run FireCrawl spider to scrape multiple tenders"

    def handle(self, *args, **kwargs):
        spider = TenderSpider()
        spider.run()
        self.stdout.write(self.style.SUCCESS("FireCrawl tender crawl complete"))