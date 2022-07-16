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


def choose_worksheet():
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


        if validate_input_choice(choice, valid_choice):
            print("Valid input")
            break
    
    return choice


def choose_month():
    while True:
        print("Now choose the month that you wish to update or, in case you chose h, month of which you want to view the total expences.")
        print("a: January,\nb: February,\nc: March,\nd: April,\ne: May,\nf: June,\ng: July,\nh: August,\ni: September,\nj: October,\nk: November,\nl: December")
        decided_month = input("Input a, b, c, d, e, f, g, h, i, j, k, l\n").lower()
        new_valid_choice = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l")
    
        if validate_input_choice(decided_month, new_valid_choice):
            print("Valid input")
            break
    return decided_month

def get_expense_data():
    """
    Get expense input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of a number.
    The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter how much was your expence.")
        print("Data should be a decimal number.")
        print("Example: 109.08\n")

        data = input("Enter your data here: ")

        if validate_input_data(data):
            print("Data is valid!")
            break

    return data

def find_worksheet(chosen_worksheet):
    """
    Locate the worksheet that the user has chosen to update
    """
    if chosen_worksheet == "a":
        chosen_worksheet = SHEET.worksheet("gas")
    elif chosen_worksheet == "b":
        chosen_worksheet = SHEET.worksheet("electricity")
    elif chosen_worksheet == "c":
        chosen_worksheet = SHEET.worksheet("water")
    elif chosen_worksheet == "d":
        chosen_worksheet = SHEET.worksheet("council")
    elif chosen_worksheet == "e":
        chosen_worksheet = SHEET.worksheet("phone")
    elif chosen_worksheet == "f":
        chosen_worksheet = SHEET.worksheet("car")
    elif chosen_worksheet == "g":
        chosen_worksheet = SHEET.worksheet("food")
    else:
        chosen_worksheet = SHEET.worksheet("total")
    print(chosen_worksheet)
    return chosen_worksheet
    
def find_column(column_number):
    if column_number == "a":
        column_number = 1
    elif column_number == "b":
        column_number = 2
    elif column_number == "c":
        column_number = 3
    elif column_number == "d":
        column_number = 4
    elif column_number == "e":
        column_number = 5
    elif column_number == "f":
        column_number = 6
    elif column_number == "g":
        column_number = 7
    elif column_number == "h":
        column_number = 8
    elif column_number == "i":
        column_number = 9
    elif column_number == "j":
        column_number = 10
    elif column_number == "k":
        column_number = 11
    else:
        column_number = 12
    print(column_number)
    return(column_number)

def update_worksheet(cost, worksheet, column):
    """
    Receives a floating point number to be inserted into a worksheet.
    Update the relevant worksheet with the data provided
    """
    number = len(worksheet.col_values(column)) + 1
    worksheet.update_cell(number, column, cost)
    #worksheet.append_row(cost)
    print(number)
    
    

def validate_input_choice(value, possible_choice):
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

def validate_input_data(value):
    """
    Inside the try, converts the string value into floating point number.
    Raises ValueError if string cannot be converted into float.
    """
    try:
        float(value)
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

picked_worksheet = choose_worksheet()
month = choose_month()
expense = get_expense_data()

worksheet_to_update = find_worksheet(picked_worksheet)
column_to_update = find_column(month)

update_worksheet(expense, worksheet_to_update, column_to_update)
    

