from django.core.management.base import BaseCommand

from nlp.resources import ensure_nltk_data


class Command(BaseCommand):
    help = "Download the NLTK data packages required by the NLP pipeline."
    requires_system_checks = []

    def add_arguments(self, parser):
        parser.add_argument("--dir", default=None, help="Target directory (default: NLTK's default).")

    def handle(self, *args, **options):
        downloaded = ensure_nltk_data(options["dir"])
        if downloaded:
            self.stdout.write(self.style.SUCCESS(f"Downloaded: {', '.join(downloaded)}"))
        else:
            self.stdout.write("All NLTK packages are already installed.")
