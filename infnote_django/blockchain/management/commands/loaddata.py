from django.core.management.base import BaseCommand
from blockchain.core import load_all_data


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--start', type=int, default=0, help='The start height to load data.')
        parser.add_argument('--end', type=int, default=None, help='The end height to load data.')

    def handle(self, *args, **options):
        load_all_data(options['start'], options['end'])
