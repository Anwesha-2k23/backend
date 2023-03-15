from django.core.management import BaseCommand
from event.models import Team, SoloParicipants, PayUTxn, Events
from user.models import User
import pandas as pd

class XLSXtoXLSX:
    def __init__(self, input_file, output_file, offset = 0):
        self.input_file = input_file
        self.output_file = output_file
        self.data = None
        self.customFields = set()
        self.OFFSET = offset

    def convert(self):
        df = pd.read_excel(self.input_file)
        self.data = df.to_dict(orient='records')[self.OFFSET:]
        self.fetchCustomAttrib()
        self.expandCustomAttrib()
    
    def fetchCustomAttrib(self):
        COLMN_NAME = "customAttribute"
        for row in self.data:
            t = row[COLMN_NAME]
            try:
                t = t.replace('"', "").replace("{","").replace("}","").split("|")[:-1]
                t = [tt.strip() for tt in t]
                keys = [ tt.split(":")[0] for tt in t ]
                self.customFields = self.customFields.union(set(keys))
            except:
                continue

        print("Custom Fields -> ",self.customFields)
    
    def expandCustomAttrib(self):
        COLMN_NAME = "customAttribute"
        for row in self.data:
            t = row[COLMN_NAME]
            for field in self.customFields:
                row[field] = ""
            try:
                t = t.replace('"', "").replace("{","").replace("}","").split("|")[:-1]
                t = [tt.strip() for tt in t]
                keys = [ tt.split(":")[0] for tt in t ]
                values = [ tt.split(":")[1] for tt in t ]
                for key, value in zip(keys, values):
                    row[key] = value
            except:
                continue
            del row[COLMN_NAME]
        print("Expanded")

    def write(self):
        df = pd.DataFrame(self.data)
        df.to_excel(self.output_file, index=False)
        print("Wrote")


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from children.csv"

    def printf(self, msg : str, f) -> None:
        print(msg)
        f.write(msg + "\n")

    def processPayment(self,payment, f):
        if payment['paymentStatus'] != 'success':
            return
        
        try:
            user_id = payment['Anwesha ID']
            user = User.objects.get(anwesha_id=user_id)
        except:
            self.printf("User not found", f)
            return
        

    def handle(self, *args, **options):
        f = open("hardVarification.log", "a")
        input_filename = "snapshot.in.xlsx"
        output_filename = "snapshot.out.v1.xlsx"
        offset = 57

        xlsx_to_xlsx = XLSXtoXLSX(input_filename, output_filename, offset)
        xlsx_to_xlsx.convert()
        
        payments = xlsx_to_xlsx.data
        for payment in payments:
            self.processPayment(payment)