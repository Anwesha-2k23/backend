from csv import DictReader
from django.core.management import BaseCommand

# Import the model 
from event.models import Events


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from children.csv"

    def handle(self, *args, **options):
    
        # Show this if the data already exist in the database
        # if Events.objects.exists():
        #     print('child data already loaded...exiting.')
        #     print(ALREDY_LOADED_ERROR_MESSAGE)
        #     return
            
        # Show this before loading the data into the database
        print("Loading childrens data")


        #Code to load the data into database
        for row in DictReader(open('./events.csv')):
            print(row)
            data=Events.objects.create(
                # name=row['Name'],
                # sex=row['Sex'], 
                # age=row['Age']
                id=row['id'],
                name=row['name'],
                organizer=row['organizer'],
                venue=row['venue'],
                description=row['description'],
                start_time=row['start_time'],
                end_time=row['end_time'],
                prize=row['prize'],
                registration_fee=row['registration_fee'],
                registration_deadline=row['registration_deadline'],
                video=row['video'],
                poster=row['poster'],
                tags=row['tags'],
                max_team_size=row['max_team_size'],
                min_team_size=row['min_team_size'],
                is_active=True,
                is_online=False,
                registration_link="blank",
            )  
            data.save()