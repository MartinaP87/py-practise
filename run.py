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
        print("Please select what kind of expense you are updating \
today:\na: Gas bill,\nb: Electricity bill,\nc: Water bill\
,\nd: Council tax,\ne: Phone bill,\nf: Car expenses,\ng\
: Food expenses,\nh: If you only want to view the \
total of your monthly expenses.")
        letter_choice = input("Input a, b, c, d, e, f, g, h\n").lower()
        if validate_first_input_choice(letter_choice):
            print("Valid input")
            break
    return letter_choice


def choose_month(chosen_letter):
    """
    Allow the user to choose the month to update.
    Run a while loop to collect a valid string of data from the user
    via terminal, which must be a number within 1 and 12.
    The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Now choose the month that you wish to update or,\
in case you chose h,the month of which you want to view \
the total expences. If you chose h and, you wish to \
view the yearly total, you can type 13.")
        print("1: January,\n2: February,\n3: March,\n\
4: April,\n5: May,\n6: June,\n7: July,\n8: August,\
\n9: September,\n10: October,\n11: November,\
\n12: December\n")
        month_choice = input("Input 1, 2, 3, 4, 5, 6, 7,\
8, 9, 10, 11, 12\n")
        num_months = 12

        if validate_second_input_choice(month_choice, num_months):
            print("Valid input")
            break
    return month_choice


def find_worksheet(chosen_letter):
    """
    Locate the worksheet that the user has chosen to update
    """
    bills_letters = ("a", "b", "c", "d", "e")
    if chosen_letter in bills_letters:
        chosen_letter = SHEET.worksheet("monthly_bills")
    elif chosen_letter == "f":
        chosen_letter = SHEET.worksheet("car")
    elif chosen_letter == "g":
        chosen_letter = SHEET.worksheet("food")
    else:
        chosen_letter = SHEET.worksheet("total")
    print(chosen_letter)
    return chosen_letter


def get_expense_data(chosen_letter, column, chosen_worksheet):
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

        data = math.ceil(float(input("Enter your data here: ")))

        if validate_input_data(data):
            print("Data is valid!")
            break

    update_worksheet(data, chosen_letter, column, chosen_worksheet)
    return data


def update_worksheet(cost, chosen_letter, column, chosen_worksheet):
    """
    Update with the data provided the first cell available
    of the chosen month column, in the relevant worksheet
    """
    if chosen_letter == "a":
        row = 2
        column = int(column) + 1
    elif chosen_letter == "b":
        row = 3
        column = int(column) + 1
    elif chosen_letter == "c":
        row = 4
        column = int(column) + 1
    elif chosen_letter == "d":
        row = 5
        column = int(column) + 1
    elif chosen_letter == "e":
        row = 6
        column = int(column) + 1
    else:
        row = len(chosen_worksheet.col_values(column)) + 1

    chosen_worksheet.update_cell(row, column, cost)
    month_name = chosen_worksheet.row_values(1)[column - 1]
    print(f"Your {chosen_worksheet} has been updated:\n\
The new value for the month of {month_name} is: {cost}")


def totals_to_update(chosen_letter):
    print("Updating Total Worksheet...")
    if chosen_letter == "f":
        update_monthly_totals(1, SHEET.worksheet("car"), "B3")
        totals_of_totals()
    elif chosen_letter == "g":
        update_monthly_totals(1, SHEET.worksheet("food"), "B4")
        totals_of_totals()
    else:
        update_monthly_totals(2, SHEET.worksheet("monthly_bills"), "B2")
        totals_of_totals()


def calculate_totals(row, worksheet):
    """
    Adds all values for each column in a worksheet and
    returns a list of list of the results.
    """
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
    return total_list_of_list


def update_monthly_totals(row, worksheet, coordinate):
    """
    Updates total worksheet with the new calculated totals
    in the respective row.
    """
    total_worksheet = SHEET.worksheet("total")
    updated_list = calculate_totals(row, worksheet)
    total_worksheet.update(coordinate, updated_list)


def totals_of_totals():
    """
    Clears the previous values in the year totals column.
    Sums the values of each row in total worksheet to view
    the yearly total costs of each expense type.
    Updates the year totals column with the new values.
    """
    print("Updating year totals...")
    total_worksheet = SHEET.worksheet("total")
    total_worksheet.batch_clear(["N2:N4"])
    total_list = []
    for num in range(2, 5):
        row = total_worksheet.row_values(num)
        row.pop(0)
        int_row = [int(value) for value in row]
        totals = [sum(int_row)]
        total_list.append(totals)
    print(total_list)
    total_worksheet.update("N2:N4", total_list)

    print("Updating monthly totals...")
    total_worksheet.batch_clear(["B5:N5"])
    update_monthly_totals(2, SHEET.worksheet("total"), "B5")
    print("Total Worksheet Updated!")


def view_total_data():
    """
    Access the value of the total expenses for the selected month
    or the year total of an expense type
    """
    total_type = choose_total()
    total_worksheet = SHEET.worksheet("total")
    if total_type == 1:
        month_total = choose_month(worksheet_letter)
        month_column = int(month_total) + 1
        row = len(total_worksheet.col_values(month_column))
        cell = total_worksheet.cell(row, month_column).value
        month_name = total_worksheet.cell(1, month_column).value
        print(f"The total of your expenses for {month_name} is £ {cell}")
    else:
        exp_year_total = choose_expense_year_total()
        requested_value = total_worksheet.col_values(14)[exp_year_total]
        print(requested_value)


def choose_total():
    while True:
        print("- If you would like to view the total \
of your expenses by month, type: 1;\n- If you prefer \
to see how much you spent during this year so far, of an expense \
type such as food or monthly bills, type: 2")
        total_type = input("Input 1 or 2")
        max_choice = 2
        if validate_second_input_choice(total_type, max_choice):
            print("Valid input")
            break
        return total_type

def choose_expense_year_total():
    while True:
        print("Now type which kind of expense you would like to view:\n\
1. Monthly Bills;\n2. Car expenses\n3. Food expenses;\n4. Total of Totals\n")
        exp_type = input("Input 1, 2, 3 or 4")
        max_choice = 4
        if validate_second_input_choice(exp_type, max_choice):
            print("Valid input")
            break
        return exp_type


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
                f"You have input {value}; your value must be either \
                    a, b, c, d, e, f, g or h"
                )
    except ValueError as e:
        print(f"invalid data: {e}. Please try again.\n")
        return False

    return True


def validate_second_input_choice(value, choice_num):
    """
    it converts the string into integer and raise a value error
    if it's not a number between 1 and 12 or if the value is not correct.
    """
    try:
        month_number = int(value)
        if month_number < 1 or month_number > choice_num:
            raise ValueError(
                f"Only values between 1 and {choice_num} are acceptable, you entered {value}"
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


def main():
    worksheet_letter = choose_worksheet()
    if worksheet_letter != "h":
        worksheet_to_update = find_worksheet(worksheet_letter)
        month = choose_month(worksheet_letter)
        expense = get_expense_data(worksheet_letter, month, worksheet_to_update)
        totals_to_update(worksheet_letter)
    else:
        view_total_data()
        
