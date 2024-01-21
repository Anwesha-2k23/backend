from csv import DictReader
from django.core.management import BaseCommand

# Import the model 
from CA.models import Campus_ambassador


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from ca.csv"

    def handle(self, *args, **options):
    
        print("Loading CA data")


        #Code to load the data into database
        for row in DictReader(open('./ca.csv')):
            print(row)
            data=Campus_ambassador.objects.create(
                # name=row['Name'],
                # sex=row['Sex'], 
                # age=row['Age']
                ca_id=row['ca_id'],
                anwesha=None,
                password=row['password'],
                phone_number=row['phone_number'],
                email_id=row['email_id'],
                full_name=row['full_name'],
                college_name=row['college_name'],
                college_city=row['college_city'],
                refferal_code=row['refferal_code'],
                age=row['age'],
                intrests=row['intrests'],
                gender=row['gender'],
                score=row['score'],
                is_loggedin=row['is_loggedin'],
                validation=row['validation'],
                instagram_id=row['instagram_id'],
                facebook_id=row['facebook_id'],
                linkdin_id=row['linkdin_id'],
                twitter_id=row['twitter_id'],
                date_of_birth=None,
                time_of_registration=row['time_of_registration'],
                profile_photo=row['profile_photo'],
            )  
            data.save()
        print("data succesfully migrated")