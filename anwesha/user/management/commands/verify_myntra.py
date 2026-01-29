from django.core.management.base import BaseCommand
from google.oauth2 import service_account
from googleapiclient.discovery import build
from user.models import User
from django.conf import settings
import datetime
import os

class Command(BaseCommand):
    help = 'Verify users from Myntra Google Sheet'

    def handle(self, *args, **kwargs):
        # Configuration - Update these with actual values from env or file
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        # Assuming service_account.json is in project root
        SERVICE_ACCOUNT_FILE = os.path.join(settings.BASE_DIR, 'service_account.json') 
        
        # PLEASE CONFIGURE THESE
        SPREADSHEET_ID = os.environ.get('MYNTRA_SPREADSHEET_ID', '1HsKe7rPy6dK3kwRepgq0sPC-cFodo24bzN6Sc0ySQrc')
        RANGE_NAME = 'Form Responses 1!A:Z' 

        self.stdout.write(f"Looking for credentials at: {SERVICE_ACCOUNT_FILE}")
        
        if not os.path.exists(SERVICE_ACCOUNT_FILE):
             self.stdout.write(self.style.WARNING(f'Service account file not found at {SERVICE_ACCOUNT_FILE}. Please place it there.'))
             return

        creds = None
        try:
             creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Could not load credentials: {e}'))
            return

        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        
        self.stdout.write("Fetching sheet data...")
        values = []
        try:
            # Try default Form Responses 1
            result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Form Responses 1!A:Z').execute()
            values = result.get('values', [])
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Could not read 'Form Responses 1': {e}"))
            self.stdout.write("Trying 'Sheet1' instead...")
            try:
                # Fallback to Sheet1
                result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Sheet1!A:Z').execute()
                values = result.get('values', [])
            except Exception as e2:
                self.stdout.write(self.style.ERROR(f"Could not read 'Sheet1' either: {e2}. Please check the sheet tab name."))
                return

        if not values:
            self.stdout.write('No data found in sheet.')
            return

        header = values[0]
        # Robust column finding
        email_idx = -1
        festival_idx = -1
        # timestamp_idx = 0 # Usually first
        
        for i, col in enumerate(header):
            c_lower = col.lower()
            if 'email' in c_lower:
                email_idx = i
            if 'festival' in c_lower or 'college' in c_lower: # "Festival Name"
                if 'festival' in c_lower:
                    festival_idx = i
        
        self.stdout.write(f"Columns identifying - Email: {email_idx}, Festival: {festival_idx}")

        if email_idx == -1: # Fallback to common indices if header not matching
             self.stdout.write(self.style.WARNING('Could not identify Email column by name. using index 1.'))
             email_idx = 1
        
        if festival_idx == -1:
             self.stdout.write(self.style.WARNING('Could not identify Festival column by name. using index 2.'))
             festival_idx = 2

        count = 0
        updated_count = 0
        
        target_festival_value = "IIT Patna – Anwesha, Patna"

        for row in values[1:]: # Skip header
            if len(row) <= max(email_idx, festival_idx):
                continue
            
            email = row[email_idx].strip()
            festival = row[festival_idx].strip() if len(row) > festival_idx else ""
            
            # self.stdout.write(f"Checking {email} - {festival}")

            if festival == target_festival_value:
                try:
                    user = User.objects.get(email_id=email)
                    if not user.myntraVerified:
                        user.myntraVerified = True
                        user.myntraFestival = festival
                        user.myntraVerifiedAt = datetime.datetime.now()
                        user.save()
                        updated_count += 1
                        self.stdout.write(self.style.SUCCESS(f'Verified user: {email}'))
                    else:
                        # Already verified
                        pass 
                except User.DoesNotExist:
                    # User not in DB
                    pass
            count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Processed {count} rows. Verified {updated_count} new users.'))
