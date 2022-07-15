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


def choose_data_sheet():
    """
    Allow the user to choose the field where the expence belongs to
    """
    while True:
        print("Please select what kind of expence you are updating today:\na: House bills,\nb: Car expences,\nc: Food expences,\nd: If you only want to view the total of your monthly expences.")
        choice = input("Input a, b, c or d\n").lower()

        if validate_input(choice):
            print("Valid input")
            break


def validate_input(value):
    """
    Raise a value error if the value is not correct 
    or if it's not exactly 1
    """
    try:
        possible_choice = ("a", "b", "c", "d")
        value in possible_choice
        if len(value) != 1:
            raise ValueError(
                f"Only 1 value is required, you entered {len(value)} values"
	        )
        if value not in possible_choice:
            raise ValueError(
                f"You have input {value}; your value must be either a, b, c or d"
                )
    
    except ValueError as e:
        print(f"invalid data: {e}. Please try again.\n")
        return False

    return True


choose_data_sheet()