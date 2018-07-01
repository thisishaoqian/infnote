from django.core.management.base import BaseCommand

from blockchain.crons import collect_transactions


class Command(BaseCommand):
    help = 'Sync with blockchain server, load new blocks.'

    def handle(self, *args, **options):
        collect_transactions()
