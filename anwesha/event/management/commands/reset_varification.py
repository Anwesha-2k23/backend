from django.core.management import BaseCommand
from event.models import Team, SoloParicipants, PayUTxn, Events
from user.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        txns = PayUTxn.objects.filter(is_processed=True)
        for txn in txns:
            txn.is_processed = False
            txn.save()
        print("[+] All transactions varification reset")
