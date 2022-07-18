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



def calculate_total_expenses():
    """
    Accesses values of monthly bills worksheet and adds up all the values by month,
    returning a list of total values.
    """
    total_expenses = []
    total_bills = []
    monthly_bills = SHEET.worksheet("monthly_bills")
    column_number = len(monthly_bills.row_values(1))
    for num in range(2, column_number + 1):
        column = monthly_bills.col_values(num)
        column.pop(0) 
        float_column = [float(value) for value in column]
        totals = sum(float_column)
        total_bills.append(totals)
    total_expenses.append(total_bills)
    """
    Accesses values of car and food expenses worksheets,
    and adds up the values for the same month 
    returning a list of lists of total values.
    """
    other_expenses_worksheets = (SHEET.worksheet("car"), SHEET.worksheet("food"))
   
    for worksheet in other_expenses_worksheets:
        other_expenses_list = []
        column_number = len(worksheet.row_values(1))
        for num in range(1, column_number + 1):
            column = worksheet.col_values(num)
            column.pop(0) 
            float_column = [float(value) for value in column]
            totals = sum(float_column)
            other_expenses_list.append(totals)
        total_expenses.append(other_expenses_list)
      
    print(total_expenses)
    return(total_expenses)


def update_total():
    total_expenses_results = calculate_total_expenses()
    total_worksheet = SHEET.worksheet("total")   

    total_worksheet.append_rows(total_expenses_results, table_range = "B2")

update_total()


