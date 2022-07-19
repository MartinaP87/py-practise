import gspread
from google.oauth2.service_account import Credentials
import math

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


def choose_month(chosen_worksheet_letter):
    """
    Allow the user to choose the month to update.
    Run a while loop to collect a valid string of data from the user 
    via terminal, which must be a number within 1 and 12.
    The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Now choose the month that you wish to update or, in case you chose h,the month of which you want to view the total expences.")
        print("If you chose h and, you wish to view the yearly total, you can type 13.")
        print("1: January,\n2: February,\n3: March,\n4: April,\n5: May,\n6: June,\n7: July,\n8: August,\n9: September,\n10: October,\n11: November,\n12: December,\n13: Year Total\n")
        decided_month = input("Input 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13\n").lower()
        
        if validate_second_input_choice(decided_month, chosen_worksheet_letter):
            print("Valid input")
            break
    return decided_month


def get_expense_data(chosen_worksheet_letter, column, chosen_worksheet):
    """
    Get expense input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of a number.
    The loop will repeatedly request data, until it is valid.
    """
    if chosen_worksheet_letter != "h":
        while True:
            print("Please enter how much was your expence.")
            print("Data should be a decimal number.")
            print("Example: 109.08\n")

            data = math.ceil(float(input("Enter your data here: ")))

            if validate_input_data(data):
                print("Data is valid!")
                break

        update_worksheet(data, chosen_worksheet_letter, column, chosen_worksheet)
        return data
    else:
        view_total_data(column)

def find_worksheet(chosen_worksheet_letter):
    """
    Locate the worksheet that the user has chosen to update
    """
    bills_letters = ("a", "b", "c", "d", "e")
    if chosen_worksheet_letter in bills_letters:
        chosen_worksheet_letter= SHEET.worksheet("monthly_bills")
    elif chosen_worksheet_letter == "f":
        chosen_worksheet_letter = SHEET.worksheet("car")
    elif chosen_worksheet_letter == "g":
        chosen_worksheet_letter = SHEET.worksheet("food")
    else:
        chosen_worksheet_letter = SHEET.worksheet("total")
    print(chosen_worksheet_letter)
    return chosen_worksheet_letter

def update_worksheet(cost, chosen_worksheet_letter, column, chosen_worksheet):
    """
    Update with the data provided the first cell available 
    of the chosen month column, in the relevant worksheet 
    """
    if chosen_worksheet_letter == "a":
        row = 2
        column = int(column) + 1
    elif chosen_worksheet_letter == "b":
        row = 3
        column = int(column) + 1
    elif chosen_worksheet_letter == "c":
        row = 4
        column = int(column) + 1
    elif chosen_worksheet_letter == "d":
        row = 5
        column = int(column) + 1
    elif chosen_worksheet_letter == "e":
        row = 6
        column = int(column) + 1
    else:
        row = len(chosen_worksheet.col_values(column)) + 1
    
    chosen_worksheet.update_cell(row, column, cost)
    print(f"Your {chosen_worksheet} has been updated with value: {cost}")
    
    
def view_total_data(column):
    """
    Access the value of the total expenses
    for the selected month
    """
    total_worksheet = SHEET.worksheet("total")
    month_column = int(column) + 1
    #It takes the last value of the column
    row = len(total_worksheet.col_values(month_column)) 
    cell = total_worksheet.cell(row, month_column).value
    month_name = total_worksheet.cell(1, month_column).value
    print(f"The total of your expenses for {month_name} is £ {cell}")


def update_totals(chosen_worksheet_letter):
    bills_letters = ("a", "b", "c", "d", "e")
    print("Updating total worksheet...")
    
    if chosen_worksheet_letter in bills_letters:
        calculate_totals(2, SHEET.worksheet("monthly_bills"), "B2")
    elif chosen_worksheet_letter == "f":
        calculate_totals(1, SHEET.worksheet("car"), "B3")
    elif chosen_worksheet_letter == "g":
        calculate_totals(1, SHEET.worksheet("food"), "B4")
    else:
       print("Nothing to update")
    print("Updating Year totals...")
    calculate_year_totals()
    print("Updating totals in total worksheet...")
    SHEET.worksheet("total").batch_clear(["B5:M5"])
    calculate_totals(2, SHEET.worksheet("total"), "B5")
    print("Total worksheet updated!")
    
def calculate_totals(row, worksheet, coordinate):
    total_worksheet = SHEET.worksheet("total")
    total_list_of_list = []
    total_list = []
    column_number = len(worksheet.row_values(1))
    for num in range(row, column_number + 1):
        column = worksheet.col_values(num)
        column.pop(0)
        int_column = [int(value) for value in column]
        totals = sum(int_column)
        total_list.append(totals)
    total_list_of_list.append(total_list)
    print(total_list_of_list)
    total_worksheet.update(coordinate, total_list_of_list)

def calculate_year_totals():
    total_worksheet = SHEET.worksheet("total")
    total_list_of_list = []
    total_list = []
    column_number = len(total_worksheet.row_values(1))
    for num in range(2, 5):
        row = total_worksheet.row_values(num)
        print(row)
        row.pop(0)
        int_row = [int(value) for value in row]
        totals = sum(int_row)
        total_list.append(totals)
    total_list_of_list.append(total_list)
    print(total_list_of_list)
    total_worksheet.update("N2:N5", total_list_of_list)


def validate_first_input_choice(value):
    """
    Inside the try, state that the value must be included in possible choice.
    Raise a value error if the value is not exactly 1
    or if it's not correct 
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
                f"You have input {value}; your value must be either a, b, c, d, e, f, g or h"
                )
    
    except ValueError as e:
        print(f"invalid data: {e}. Please try again.\n")
        return False

    return True


def validate_second_input_choice(value, chosen_worksheet_letter):
    """
    If the worksheet chosen is not the Total worksheet
    it converts the string into integer and raise a value error 
    if it's not a number between 1 and 12 or if the value is not correct.
    If the worksheet chosen is the Total worksheet, it changes 
    the range in which the number can be to between 1 and 13.
    """
    if chosen_worksheet_letter != "h":
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
    else:
        try:
            month_number = int(value)
            if month_number < 1 or month_number > 13:
                raise ValueError(
                    f"Only values between 1 and 13 are acceptable, you entered {value}"
	            )
        except ValueError as e:
            print(f"Invalid data: {e}, please try again.\n")
            return False
        return True
        
   

def validate_input_data(value):
    """
    Inside the try, converts the string value into an approximated integer.
    Raises ValueError if string cannot be converted into integer.
    """
    try:
        math.ceil(float(value))
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True



worksheet_letter = choose_worksheet()
worksheet_to_update = find_worksheet(worksheet_letter)
month = choose_month(worksheet_letter)
expense = get_expense_data(worksheet_letter, month, worksheet_to_update)
update_totals(worksheet_letter)
