# Home Expense Tracker
[View the live project here]()

Home Expense Tracker is a command-line application that allows to set budgets and input basic home expenses such as bills, food, and car expenses throughout the year.
The application calculates the totals and compares them to budgets when set by the user or calculable.
The program's goal is to provide the user with an immediate understanding of essentials spendings and eventually to help better manage one's finances.
Home Expense Tracker's target is young adults who just moved out from their parent's house and need to plan and manage their finances.
It also targets families with low incomes, who need to pay attention to any expense to stay within their budgets.

## LINK TO GOOGLE SPREADSHEET:

-[Google Spreadsheet Link]()
-To run the program without values, the user  can delete the numbers in "car", "food" and "budget" worksheets.
Instead, the numbers in "monthly_bills" and "total" worksheets, must be replaced with the value 0.

## FEATURES:

### Welcome Section
 <img src ="readme-images/welcome.png">

- This first section greets the user with a welcome message and requests to enter a number to choose the operation to perform from the presented list.
- If the input choice is not in the number range or not a number at all, the program displays a customized message error.

### Months Section
<img src="readme-images/months.png">

- This section requests the user to enter a number to choose the month relative to the previously selected operation.
- This section is displayed if:
  - The first choice is to update an expense;
  - The first choice is to set a monthly budget;
  - The first choice is to view a total and the choice of Total Type Section is 1.
- If the input choice is not in the number range or not a number at all, the program displays a customized message error.


### Input Section
<img src="readme-images/input.png">

- This section requests the user to enter the expense value to be registered or the budget's value to be set.
- If the input choice is not a positive number, the program displays a customized message error.


### Feedback Section
<img src="readme-images/feedback.png">

- In this section, the program sends feedback to the user explaining how it handles the input data by printing the worksheet updated, the month, and the new value. Updating a value also triggers an update of monthly and yearly totals; messages of the main steps of the operations are displayed here too.

### Budget Section
<img src="readme-images/budget.png">

- This section shows messages about the comparison between
monthly and yearly expenses and their respective budgets.
- If the comparison is not possible, another sentence explains the reason on the terminal.
- This section is displayed if:
  - The first choice is to update an expense;
  - The first choice is to set a monthly budget.

### Restart/Leave Section

<img src="readme-images/restart.png">
- In this section, the program requests the user to choose between exiting the app or restarting the program.
- If the input choice is: a letter but not y or n, not a letter at all, or more than one letter, the program displays a customized message error.


### Expense Type Section

<img src="readme-images/expense-type.png">
- In this section, the program requests to enter a number to choose the expense type.
- This section is displayed if:
  - The first choice is to set a monthly budget;
  - The first choice is to view a total and the choice of Total Type Section is 2.
- If the input choice is not in the number range or not a number at all, the program displays a customized message error.


### View Total Section

<img src="readme-images/total.png">
- In this section, the program requests to choose which total to display: the total of expenses by month or the total of a specific expense type by year.
- If the input choice is not in the number range or not a number at all, the program displays a customized message error.

### 

## Data Model:
## Testing: