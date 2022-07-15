import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("practise")


bills = SHEET.worksheet("bills")
data = bills.get_all_values()
print(data)

def choose_data_sheeet():
    """
    Allow the user to choose the field where the expence belongs to
    """
    print("Please select what kind of expence you are updating today:\na: House bills,\nb: Car expences,\nc: Food expences,\nd: If you only want to view the total of your monthly expences.")
    choice = input("Input a, b, c or d\n")

choose_data_sheeet()