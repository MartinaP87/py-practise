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
        
        if validate_first_input_choice(choice):
            print("Valid input")
            break
    
    return choice


def choose_month():
    while True:
        print("Now choose the month that you wish to update or, in case you chose h,the month of which you want to view the total expences.")
        print("1: January,\n2: February,\n3: March,\n4: April,\n5: May,\n6: June,\n7: July,\n8: August,\n9: September,\n10: October,\n11: November,\n12: December")
        decided_month = input("Input 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12\n").lower()
        
        if validate_second_input_choice(decided_month):
            print("Valid input")
            break
    return decided_month


def get_expense_data(chosen_worksheet):
    """
    Get expense input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of a number.
    The loop will repeatedly request data, until it is valid.
    """
    if chosen_worksheet != "h":
        while True:
            print("Please enter how much was your expence.")
            print("Data should be a decimal number.")
            print("Example: 109.08\n")

            data = input("Enter your data here: ")

            if validate_input_data(data):
                print("Data is valid!")
                break

        return data
    else:
        view_total_data(month)

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

def update_worksheet(cost, worksheet, column):
    """
    Receives a floating point number to be inserted into a worksheet.
    Update the relevant worksheet with the data provided
    """
    row = len(worksheet.col_values(column)) + 1
    worksheet.update_cell(row, column, cost)
    
    
def view_total_data(column):
    """
    Access the value of the total expenses
    for the selected month
    """
    total_worksheet = SHEET.worksheet("total")
    row = len(total_worksheet.col_values(column)) 
    cell = total_worksheet.cell(row, column).value
    month_name = total_worksheet.cell(1, column).value
    print(f"The total of your expenses of {month_name} is £ {cell}")

def validate_first_input_choice(value):
    """
    Raise a value error if the value is not correct 
    or if it's not exactly 1
    """
    possible_choice = ("a", "b", "c", "d", "e", "f", "g", "h")
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


def validate_second_input_choice(value):
    """
    Raise a value error if the value is not correct 
    or if it's not a number
    """
    try:
        month_number = int(value)
        if month_number < 1 or month_number > 12:
            raise ValueError(
                f"Only values between 1 and 12 are acceptable, you entered {value}"
	        )  
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
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
expense = get_expense_data(picked_worksheet)

worksheet_to_update = find_worksheet(picked_worksheet)

update_worksheet(expense, worksheet_to_update, month)
    

