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
    Allow the user to choose the field to which the expense belongs
    or to access total worksheet.
    Run a while loop to collect a valid string from the user
    via terminal, which must be a string of 1 letter within the possible
    choices. The loop will repeatedly request data until it is valid.
    """
    while True:
        print("Please select what kind of expense you are updating \
today:\n1: Gas bill,\n2: Electricity bill,\n3: Water bill\
,\n4: Council tax,\n5: Phone bill,\n6: Car expenses,\n7\
: Food expenses,\n8: If you only want to view the \
total of your monthly expenses.")
        worksheet_choice = input("Input 1, 2, 3, 4, 5, 6, 7, 8:\n")
        max_num_choices = 8
        if validate_choice(worksheet_choice, max_num_choices):
            print("Valid input")
            break
    return worksheet_choice


def choose_month():
    """
    Allow the user to choose the month to update.
    Run a while loop to collect a valid string of data from the user
    via terminal, which must be a number within 1 and 12.
    The loop will repeatedly request data until it is valid.
    """
    while True:
        print("Now choose the month for your operation.")
        print("1: January,\n2: February,\n3: March,\n\
4: April,\n5: May,\n6: June,\n7: July,\n8: August,\
\n9: September,\n10: October,\n11: November,\
\n12: December\n")
        month_choice = input("Input 1, 2, 3, 4, 5, 6, 7,\
8, 9, 10, 11, 12:\n")
        max_num_months = 12

        if validate_choice(month_choice, max_num_months):
            print("Valid input")
            break
    return month_choice


def find_worksheet(chosen_worksheet_num):
    """
    Locate the worksheet that the user has chosen to update
    """
    if chosen_worksheet_num == "6":
        chosen_worksheet = SHEET.worksheet("car")
    elif chosen_worksheet_num == "7":
        chosen_worksheet = SHEET.worksheet("food")
    else:
        chosen_worksheet = SHEET.worksheet("monthly_bills")
    print(chosen_worksheet)
    return chosen_worksheet


def get_expense_data(chosen_worksheet_num, column, chosen_worksheet):
    """
    Get expense input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of a number.
    The loop will repeatedly request data until it is valid.
    """
    while True:
        print("Please enter how much your expense was.")
        print("Data should be a decimal number.")
        print("Example: 109.08\n")

        data = math.ceil(float(input("Enter your data here: ")))

        if validate_input_data(data):
            print("Data is valid!")
            break

    update_worksheet(data, chosen_worksheet_num, column, chosen_worksheet)
    return data


def update_worksheet(data, chosen_worksheet_num, column, chosen_worksheet):
    """
    With the data provided, update the relevant cell
    if the first choice was a monthly bill.
    Otherwise, update the first cell available of
    the chosen month column in the relevant worksheet.
    """
    if int(chosen_worksheet_num) <= 5:
        row = int(chosen_worksheet_num) + 1
        column = int(column) + 1
    else:
        row = len(chosen_worksheet.col_values(column)) + 1

    chosen_worksheet.update_cell(row, column, data)
    month_name = chosen_worksheet.row_values(1)[int(column) - 1]
    print(f"Your {chosen_worksheet} has been updated:\n\
The new value for {month_name} is: {data}")


def totals_to_update(chosen_worksheet_num):
    """
    Assign the arguments to update monthly total
    function in base of the letter choice
    """
    print("Updating Total Worksheet...")
    if chosen_worksheet_num == "6":
        update_monthly_totals(1, SHEET.worksheet("car"), "B3")
        totals_of_totals()
    elif chosen_worksheet_num == "7":
        update_monthly_totals(1, SHEET.worksheet("food"), "B4")
        totals_of_totals()
    else:
        update_monthly_totals(2, SHEET.worksheet("monthly_bills"), "B2")
        totals_of_totals()


def calculate_totals(row, chosen_worksheet):
    """
    Add all values for each column in a worksheet and
    return the results as a list of list.
    """
    total_list_of_list = []
    total_list = []
    column_number = len(chosen_worksheet.row_values(1))
    for num in range(row, column_number + 1):
        column = chosen_worksheet.col_values(num)
        column.pop(0)
        int_column = [int(value) for value in column]
        totals = sum(int_column)
        total_list.append(totals)
    total_list_of_list.append(total_list)
    return total_list_of_list


def update_monthly_totals(row, chosen_worksheet, coordinate):
    """
    Updat total worksheet with the new calculated totals
    in the respective row.
    """
    total_worksheet = SHEET.worksheet("total")
    updated_list = calculate_totals(row, chosen_worksheet)
    total_worksheet.update(coordinate, updated_list)


def totals_of_totals():
    """
    Clear the previous values in the Year Totals column.
    Sum the values of each row in the total worksheet to view
    the yearly costs of each expense type.
    Update the year totals column with the new values.
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
    or the year total of an expense type.
    """
    total_type = choose_total()
    total_worksheet = SHEET.worksheet("total")
    if total_type == "1":
        month_total = choose_month()
        month_column = int(month_total) + 1
        row = len(total_worksheet.col_values(month_column))
        cell = total_worksheet.cell(row, month_column).value
        month_name = total_worksheet.cell(1, month_column).value
        print(f"The total of your expenses for {month_name} is £ {cell}")
    else:
        exp_year_total = choose_expense_year_total()
        requested_exp_type = total_worksheet.col_values(1)[int(exp_year_total)]
        requested_value = total_worksheet.col_values(14)[int(exp_year_total)]
        print(f"So far this year your {requested_exp_type} amount is:\n\
£ {requested_value}")


def choose_total():
    """
    Allow the user to view the totals by month or expense type.
    Run a while loop to collect a valid string of data from the user
    via terminal, which must be a number within 1 and 2.
    The loop will repeatedly request data until it is valid.
    """
    while True:
        print("Type 1:\n If you would like to view the total \
of your expenses by month;\nType 2:\n If you prefer \
to see how much you spent during this year so far, of an expense \
type such as food or monthly bills.")
        total_choice = input("Input 1 or 2:\n")
        max_choices = 2
        if validate_choice(total_choice, max_choices):
            print("Valid input")
            break
    return total_choice


def choose_expense_year_total():
    """
    Allow the user to choose the expense type.
    Run a while loop to collect a valid string of data from the user
    via terminal, which must be a number within 1 and 4.
    The loop will repeatedly request data until it is valid.
    """
    while True:
        print("Now type which kind of expense you would like to view:\n\
1. Monthly Bills;\n2. Car expenses\n3. Food expenses;\n4. Total of Totals\n")
        expense_type = input("Input 1, 2, 3 or 4\n")
        max_types = 4
        if validate_choice(expense_type, max_types):
            print("Valid input")
            break
    return expense_type


def exit_restart():
    """
    Request the user to choose between exiting
    the app or continuing with a new operation.
    Run a while loop to collect a valid string of data from the user
    via terminal, which must be a string with value y or n.
    The loop will repeatedly request data until it is valid
    """
    while True:
        print("Do you wish to continue with another operation?")
        last_input = input("Input y for yes or n for no\n").lower()
        choice_options = ("y", "n")
        if validate_last_choice(last_input, choice_options):
            print("Valid input")
            break
    return last_input


def validate_choice(choice, max_num):
    """
    Inside the try, state that the value must be in a specific range.
    Raise a value error if the string value is not convertible
    into an integer or if it is outside the range.
    """
    try:
        choice_number = int(choice)
        if choice_number < 1 or choice_number > max_num:
            raise ValueError(
                f"Only values between 1 and {max_num} are acceptable, \
you entered: {choice}"
                )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def validate_input_data(value):
    """
    Inside the try, convert the string value into an approximated integer.
    Raises ValueError if the string is not convertible into an integer.
    """
    try:
        math.ceil(float(value))
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return True


def validate_last_choice(value, possible_choice):
    """
    Inside the try, state that the value must be included
    in possible choice.
    Raise a value error if the value is not exactly 1
    or if it's not correct.
    """
    try:
        if value in possible_choice:
            if len(value) != 1:
                raise ValueError(
                    f"Only 1 value is required, you entered {len(value)} \
values.")
        else:
            raise ValueError(
                f"You have input {value}; your value must be either y or n"
                )
    except ValueError as e:
        print(f"invalid data: {e}. Please try again.\n")
        return False

    return True


def main():
    worksheet_num = choose_worksheet()
    if worksheet_num != "8":
        worksheet_to_update = find_worksheet(worksheet_num)
        month = choose_month()
        get_expense_data(worksheet_num, month, worksheet_to_update)
        totals_to_update(worksheet_num)
    else:
        view_total_data()
    last_choice = exit_restart()
    if last_choice == "y":
        main()
    else:
        print("Have a great day!\nSee you next time!")


main()
