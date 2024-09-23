from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Load initial data for categories and subcategories'

    def handle(self, *args, **options):
        self.stdout.write('Loading initial data...')
        call_command('loaddata', 'initial_data.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded initial data'))