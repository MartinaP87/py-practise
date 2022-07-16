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


def choose_sheet():
    """
    Allow the user to choose the field where the expence belongs to.
    Run a while loop to collect a valid string of data from the user 
    via terminal, which must be a string of 1 letter within the possible 
    coiches. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please select what kind of expense you are updating today:\na: Gas bill,\nb: Electricity bill,\nc: Water bill,\nd: Council tax,\ne: Phone bill,\nf: Car expenses,\ng: Food expenses,\nh: If you only want to view the total of your monthly expenses.")
        choice = input("Input a, b, c, d, e, f, g, h\n").lower()
        valid_choice = ("a", "b", "c", "d", "e", "f", "g", "h")


        if validate_input(choice, valid_choice):
            print("Valid input")
            break
    
    return choice


def choose_month():
    while True:
        print("Now choose the month that you wish to update or, in case you chose h, month of which you want to view the total expences.")
        print("a: January,\nb: February,\nc: March,\nd: April,\ne: May,\nf: June,\ng: July,\nh: August,\ni: September,\nj: October,\nk: November,\nl: December")
        decided_month = input("Input a, b, c, d, e, f, g, h, i, j, k, l\n").lower()
        new_valid_choice = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l")
    
        if validate_input(decided_month, new_valid_choice):
            print("Valid input")
            break
    return decided_month

def find_cell(expense, period):
    """
    Locate the cell that the user has chosen to update
    """
    if expense == "a":
        expense = SHEET.worksheet("gas")
    elif expense == "b":
        expense = SHEET.worksheet("electricity")
    elif expense == "c":
        expense = SHEET.worksheet("water")
    elif expense == "d":
        expense = SHEET.worksheet("council")
    elif expense == "e":
        expense = SHEET.worksheet("phone")
    elif expense == "f":
        expense = SHEET.worksheet("car")
    elif expense == "g":
        expense = SHEET.worksheet("food")
    else:
        expense = SHEET.worksheet("total")
    
    if period == "a":
        period = expense.col_values(1)
    elif period == "b":
        period = expense.col_values(2)
    elif period == "c":
        period = expense.col_values(3)
    elif period == "d":
        period = expense.col_values(4)
    elif period == "e":
        period = expense.col_values(5)
    elif period == "f":
        period = expense.col_values(6)
    elif period == "g":
        period = expense.col_values(7)
    elif period == "h":
        period = expense.col_values(8)
    elif period == "i":
        period = expense.col_values(9)
    elif period == "j":
        period = expense.col_values(10)
    elif period == "k":
        period = expense.col_values(11)
    else:
        period = expense.col_values(12)

    print(expense, period)
    

def validate_input(value, possible_choice):
    """
    Raise a value error if the value is not correct 
    or if it's not exactly 1
    """
    try:
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

expense_kind = choose_sheet()
month = choose_month()
find_cell(expense_kind, month)
    

