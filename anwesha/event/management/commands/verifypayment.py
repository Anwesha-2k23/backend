from django.core.management import BaseCommand
from event.models import Team, SoloParicipants, PayUTxn, Events
from user.models import User

class Command(BaseCommand):

    help = "verifys existing payment"

    def printf(self, msg : str, f) -> None:
        print(msg)
        f.write(msg + "\n")

    def verify(self, txn, f):
        if txn.status != "success":
            self.printf(f"status : [failed] {txn.txnid}", f)
            txn.is_processed = True
            txn.save()
            return
        
        self.printf(f"status : [success] {txn.txnid}", f)
        try:
            user = User.objects.get(email_id=txn.email)
            self.printf(f"\t|- [+] User found {txn.email} -> {user.anwesha_id}", f)
        except User.DoesNotExist:
            self.printf(f"\t|- [!] User not found {txn.email}", f)
            txn.is_processed = True
            txn.save()
            return
        
        try:
            event = Events.objects.get(payment_key=txn.productinfo)
            self.printf(f"\t|- [+] Event found {txn.productinfo} -> {event.name}", f)
        except Events.DoesNotExist:
            self.printf(f"\t|- [!] Event not found {txn.productinfo}", f)
            txn.is_processed = True
            txn.save()
            return

        try:
            solo_participants = SoloParicipants.objects.get(anwesha_id=user, event_id=event )
            _event_name = solo_participants.event_id.name
            self.printf(f"\t|- [+] Solo participant found in event -> {_event_name}", f)
            solo_participants.payment_done = True
            solo_participants.order_id = txn.txnid
            solo_participants.save()
            txn.is_processed = True
            txn.save()
            self.printf(f"\t|- [+] Payment verified.", f)
            return
        except SoloParicipants.DoesNotExist:
            pass

        try:
            team_participants = Team.objects.get(leader_id=user, event_id=event)
            _event_name = team_participants.event_id.name
            self.printf(f"\t|- [+] Team participant found in event -> {_event_name}", f)
            team_participants.payment_done = True
            team_participants.txnid = txn.txnid
            team_participants.save()
            txn.is_processed = True
            txn.save()
            self.printf(f"\t|- [+] Payment verified.", f)
            return
        except Team.DoesNotExist:
            pass
        self.printf(f"\t|- [!] No participant found for {txn.email}", f)
        return

    def handle(self, *args, **options):
        unverified_txn = PayUTxn.objects.filter(is_processed=False)
        f = open("verified.txt", "a")

        if len(unverified_txn) == 0:
            self.printf("[!] Found 0 unverified transactions", f)
            f.close()
            return
        
        for txn in unverified_txn:
            self.verify(txn, f)
        
        print("[+] All transactions verified")
        f.close()
