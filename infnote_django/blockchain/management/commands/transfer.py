from django.core.management.base import BaseCommand

from blockchain.core import Tool


class Command(BaseCommand):
    help = 'Transfer a coin to specific address.'

    def add_arguments(self, parser):
        parser.add_arguments('address', type=str, default=None, help='The public address which you want transfer to.')

    def handle(self, *args, **options):
        txid = Tool.transfer_a_coin_to(options['address'])
        print('Transfered with transaction:', txid)
