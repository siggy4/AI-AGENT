from django.core.management.base import BaseCommand
from scraper.scraper import run_firecrawl_scraper


class Command(BaseCommand):
    help = 'Fetches new tenders using Firecrawl for Aura Safira Consulting'

    def handle(self, *args, **options):
        self.stdout.write("Agent is searching for opportunities...")
        result = run_firecrawl_scraper()

        if result["status"] == "success":
            self.stdout.write(self.style.SUCCESS("Successfully added {result['new_items']} new tenders!"))
        else:
            self.stdout.write(self.style.ERROR("Scraper failed to run."))