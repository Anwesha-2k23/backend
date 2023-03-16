from django.core.management import BaseCommand
from user.models import User
from utility import createId,hash_id, generate_qr

class Command(BaseCommand):

    help = "Regenerate QR for all users"

    def handle(self, *args, **options):
        try:
            users = User.objects.all()
            for user in users:
                user.secret = createId("secret",10)
                user.signature = hash_id(user.anwesha_id,user.secret)
                user.qr_code = generate_qr(user.signature)
                user.save()
            print("Regeneration successful")
        except:
            print("Regeneration failed")