from django.core.management.base import BaseCommand
from scraper.services import save_undp_tender


class Command(BaseCommand):
    help = "Scrape UNDP tender"

    def handle(self, *args, **kwargs):
        save_undp_tender()
        print("✅ UNDP tender scraped")