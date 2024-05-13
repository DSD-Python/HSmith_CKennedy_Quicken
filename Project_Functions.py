import csv
from datetime import date, datetime
import pickle
import calendar
import numpy as np
import matplotlib.pyplot as plt
import os.path
import os
import sym_encrypt as se
from pathlib import Path

def extract_data_from_csv(csv_name):
    """Takes the name of the file, opens the csv and creates a list with the data and returns that"""
    payment_list_header = []
    with open(f'{csv_name}.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            payment_list_header.append(row)
    return payment_list_header[1:]

def extract_day_of_week(my_date):
    """When given a date, it converts the value into the day of the week"""
    split_date = my_date.split("/")
    year = int(split_date[2])
    month = int(split_date[0])
    day = int(split_date[1])
    return calendar.day_name[date(year, month, day).weekday()]

def spending_by_day_full_info(payment_list):
    """Takes the current months payments and makes a dictionary with all of the transacations on each day of the week"""
    day_spend_dict = {}
    for payment in payment_list:
        day_of_week = extract_day_of_week(payment[0])
        #print(day_of_week)
        if day_of_week in day_spend_dict:
            day_spend_dict[day_of_week].append([payment[0],payment[2],payment[3],payment[5]])
        else:
            day_spend_dict[day_of_week] = [payment[0],payment[2],payment[3],payment[5]]
    return day_spend_dict


def spending_by_day(payment_list):
    """Takes the current months payments and makes a dictionary with the value of all of the transactions on each day of the week"""
    day_spend_dict = {}
    for payment in payment_list:
        if payment[4] == "Payment":
                continue
        day_of_week = extract_day_of_week(payment[0])
        if day_of_week in day_spend_dict:
                day_spend_dict[day_of_week]+=abs(float(payment[5]))
        else:
            day_spend_dict[day_of_week] = abs(float(payment[5]))
    return day_spend_dict

def avg_spending_by_day_long_term(long_term_payment):
    """Takes the previous 6 months payments and makes a dictionary with the value of all of the transactions on each day of the week"""
    day_spend_dict = {}
    if len(long_term_payment)<=6:
        length = len(long_term_payment)
    else:
        length = 6
    past_6_months_payment = long_term_payment[-6:]
    for month in past_6_months_payment:
        for payment in month:
            if payment[4] == "Payment":
                continue
            day_of_week = extract_day_of_week(payment[0])
            if day_of_week in day_spend_dict:
                day_spend_dict[day_of_week]+=float(payment[5])
            else:
                day_spend_dict[day_of_week] = float(payment[5])
    for day in day_spend_dict:
        day_spend_dict[day] = abs(day_spend_dict[day]/length)
    return day_spend_dict

def spending_by_category_full_info(payment_list):
    """Takes the current months payments and makes a dictionary with all of the transacations on each spending category"""
    category_spend_dict = {}
    for payment in payment_list:
        category = payment[3]
        if category in category_spend_dict:
            category_spend_dict[category].append([payment[0],payment[2],payment[5]])
        else:
            category_spend_dict[category] = [payment[0],payment[2],payment[5]]
    return day_spend_dict

def spending_by_category(payment_list):
    """Takes the current months payments and makes a dictionary with the value of all of the transactions on each spending category"""
    category_spend_dict = {}
    for payment in payment_list:
        category = payment[3]
        if category == '':
            continue
        if category in category_spend_dict:
            category_spend_dict[category]+= abs(float(payment[5]))
        else:
            category_spend_dict[category] = abs(float(payment[5]))
    return category_spend_dict

def avg_spending_by_category_long_term(long_term_payment):
    """Takes the previous 6 months payments and makes a dictionary with the value of all of the transactions on each spending category"""
    category_spend_dict = {}
    if len(long_term_payment)<=6:
        length = len(long_term_payment)
    else:
        length = 6
    past_6_months_payment = long_term_payment[-6:]
    for month in past_6_months_payment:
        for payment in month:
            category = payment[3]
            if category == '':
                continue
            if category in category_spend_dict:
                category_spend_dict[category]+= abs(float(payment[5]))
            else:
                category_spend_dict[category] = abs(float(payment[5]))
    for cat in category_spend_dict:
        category_spend_dict[cat] = abs(category_spend_dict[cat]/length)
    return category_spend_dict

def spending_by_location_full_info(payment_list):
    """Takes the current months payments and makes a dictionary with all of the transacations on each location"""
    location_spend_dict = {}
    for payment in payment_list:
        location = payment[2]
        if location in location_spend_dict:
            location_spend_dict[location].append([payment[0],payment[5]])
        else:
            location_spend_dict[location] = [payment[0],payment[5]]
    return location_spend_dict

def spending_by_location(payment_list):
    """Takes the current months payments and makes a dictionary with the value of all of the transactions on each location"""
    location_spend_dict = {}
    for payment in payment_list:
        location = payment[2]
        if payment[4] == "Payment":
                continue
        if location in location_spend_dict:
            location_spend_dict[location]+= abs(float(payment[5]))
        else:
            location_spend_dict[location] = abs(float(payment[5]))
    return location_spend_dict


def avg_spending_by_location_long_term(long_term_payment):
    """Takes the previous 6 months payments and makes a dictionary with the value of all of the transactions on each location"""
    location_spend_dict = {}
    if len(long_term_payment)<=6:
        length = len(long_term_payment)
    else:
        length = 6
    past_6_months_payment = long_term_payment[-6:]
    for month in past_6_months_payment:
        for payment in month:
            location = payment[2]
            if payment[4] == "Payment":
                continue
            if location in location_spend_dict:
                location_spend_dict[location]+= abs(float(payment[5]))
            else:
                location_spend_dict[location] = abs(float(payment[5]))
    for loc in location_spend_dict:
        location_spend_dict[loc] = abs(location_spend_dict[loc]/length)
    return location_spend_dict


def location_fixing(loc_short_data, loc_long_data):
    """Takes the current location data and transforms it. Includes all the locations from each dictionary in both now, and orders both by the average spending in the past 6 months in order to make the graph function work more smoothly"""
    combined_loc = {}
    short_dict = {}
    long_dict = {}
    locations = list(set(loc_short_data.keys()) | set(loc_long_data.keys()))
    for location in locations:
        loc_list = []
        if location in loc_short_data:
            loc_list.append(loc_short_data[location])
        else:
            loc_list.append(0)
        if location in loc_long_data:
            loc_list.append(loc_long_data[location])
        else:
            loc_list.append(0) 
        combined_loc[location] = loc_list
    combined_loc =  dict(sorted(combined_loc.items(), key = lambda x:x[1][1], reverse = True))
    for location in combined_loc:
        short_dict[location] = combined_loc[location][0]
        long_dict[location] = combined_loc[location][1]
    return short_dict, long_dict

def create_new_long_term_file(payment_list):
    """Creates the long term file"""
    storage_file = payment_list
    with open('credit_payment_history.pkl','wb') as f:
        pickle.dump(storage_file, f)
    f.close()
    P = Path('.') / 'credit_payment_history.pkl'
    se.encrypt(P)
    os.remove('credit_payment_history.pkl')
        


def open_long_term_file():
    """Opens the long term file"""
    P = Path('.') / 'credit_payment_history.pkl.box'
    se.decrypt(P)
    with open('credit_payment_history.pkl.secret', 'rb') as f:
        long_term_payment = pickle.load(f)
    f.close()
    os.remove('credit_payment_history.pkl.box')
    return long_term_payment

def open_long_term_file_first_time():
    """Opens the long term file"""
    P = Path('.') / 'credit_payment_history.pkl.box'
    se.decrypt(P)
    with open('credit_payment_history.pkl.secret', 'rb') as f:
        long_term_payment = pickle.load(f)
    f.close()
    os.remove('credit_payment_history.pkl.secret')
    return long_term_payment


def update_long_term_file(long_term_payment):
    """Updates the long term file. Sorts the file to ensure the payments are in order in the file"""
    date_format = '%m/%d/%Y'
    long_term_payment.sort(key = lambda x: datetime.strptime(x[0][0], date_format))
    with open('credit_payment_history.pkl','wb') as f:
        pickle.dump(long_term_payment, f)
    f.close()
    P = Path('.') / 'credit_payment_history.pkl'
    se.encrypt(P)
    os.remove('credit_payment_history.pkl.secret')
    os.remove('credit_payment_history.pkl')




def make_dow_bar(dow_dict,long_dow_dict,length):
    """Makes a bar chart showing spending on each day of the week for this month compared to last 6 months"""
    short_days = []
    long_days = []
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    for day in days:
        if day in long_dow_dict:
            long_days.append(long_dow_dict[day])
        else:
            long_days.append(0)
        if day in dow_dict:
            short_days.append(dow_dict[day])
        else:
            short_days.append(0)
    width = 0.3
    X = np.arange(len(days)) 
    plt.figure(figsize=(10,6))
    plt.bar(X, short_days, width = width,label = "Last Month")
    plt.bar(X+width,long_days, width = width,label = f"Previous {length} Months Average")
    plt.xticks(X+width/2,days)
    plt.title("Spending By Day of the Week")
    plt.xlabel("Day of the Week")
    plt.ylabel("Amount Spent ($)")
    plt.legend()
    plt.show()
    return days, short_days,long_days


def make_cat_bar(cat_dict,long_cat_dict,length):
    """Makes a bar chart showing spending on category for this month compared to last 6 months"""
    short_cat = []
    long_cat = []
    categories = list(set(cat_dict.keys()) | set(long_cat_dict.keys()))
    for category in categories:
        if category in long_cat_dict:
            long_cat.append(long_cat_dict[category])
        else:
            long_cat.append(0)
        if category in cat_dict:
            short_cat.append(cat_dict[category])
        else:
            short_cat.append(0)
    width = 0.4
    X = np.arange(len(categories)) 
    plt.figure(figsize=(6,10))
    plt.barh(X, short_cat, width, label = "Last Month")
    plt.barh(X+width,long_cat,width,label = f"Previous {length} Months Average")
    plt.yticks(X+width/2,categories)
    plt.title("Spending By Category")
    plt.ylabel("Categories")
    plt.xlabel("Amount Spent ($)")
    plt.legend()
    plt.show()
    return categories,short_cat,long_cat



def make_loc_bar_short(loc_dict):
    """Makes a bar chart showing how much was spent at each location this month"""
    locations = loc_dict.keys()
    width = 0.25
    X = np.arange(len(locations)) 
    plt.figure(figsize=(6,10))
    plt.barh(X, loc_dict.values(), width)
    plt.yticks(X,locations)
    plt.title("Spending By Location This Month")
    plt.ylabel("Locations")
    plt.xlabel("Amount Spent ($)")
    plt.show()
    return locations

def make_loc_bar_long(long_loc_dict,length):
    """Makes a bar chart showing how much was spent per month on average at each location in past 6 months"""
    locations = long_loc_dict.keys()
    width = 0.25
    X = np.arange(len(locations)) 
    plt.figure(figsize=(6,12))
    plt.barh(X, long_loc_dict.values(),width)
    plt.yticks(X,locations)
    plt.title(f"Spending By Location Past {length} Months")
    plt.ylabel("Locations")
    plt.xlabel("Amount Spent ($)")
    plt.show()
    return locations

def spent_by_month_dict(long_term_file,short_term_file):
    """Creates the dictionaries that show how much money was spent each month of the year"""
    long_term_file = long_term_file[-12:]
    by_month_dict = {}
    for dump in long_term_file:
        for transaction in dump:
            date = transaction[0]
            value = float(transaction[5])
            date_list = date.split("/")
            month = int(date_list[0])
            if transaction[4] != "Payment":
                if month in by_month_dict.keys():
                    new_total = by_month_dict[month] + abs(value)
                    by_month_dict[month] = new_total
                else:
                    by_month_dict[month] = value
    for transaction in short_term_file:
        date = transaction[0]
        value = float(transaction[5])
        date_list = date.split("/")            
        month = int(date_list[0])
        if transaction[4] != "Payment":
            if month in by_month_dict.keys():
                new_total = by_month_dict[month] + abs(value)
                by_month_dict[month] = new_total
            else:
                by_month_dict[month] = value
    return by_month_dict


def earn_by_month_dict(long_term_file,short_term_file):
    """Creates the dictionaries that show how much money was paid each month of the year"""
    long_term_file = long_term_file[-12:]
    by_month_dict = {}
    for dump in long_term_file:
        for transaction in dump:
            date = transaction[0]
            value = float(transaction[5])
            date_list = date.split("/")
            month = int(date_list[0])
            if transaction[4] == "Payment":
                if month in by_month_dict.keys():
                    new_total = by_month_dict[month] + abs(value)
                    by_month_dict[month] = new_total
                else:
                    by_month_dict[month] = value
    for transaction in short_term_file:
        date = transaction[0]
        value = float(transaction[5])
        date_list = date.split("/")            
        month = int(date_list[0])
        if transaction[4] == "Payment":
            if month in by_month_dict.keys():
                new_total = by_month_dict[month] + abs(value)
                by_month_dict[month] = new_total
            else:
                by_month_dict[month] = value
    return by_month_dict 
        

def make_spend_by_month_bar(title, total_by_month_dict):
    """This function will take dictionaries created by either of the above functions to make a spend/earn by month bar chart"""
    total_by_month = dict(sorted(total_by_month_dict.items(), key = lambda x:x[0]))
    month = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    months = [month[x] for x in total_by_month.keys()]
    width = 0.25
    X = np.arange(len(months)) 
    plt.figure(figsize=(6,12))
    plt.barh(X, total_by_month.values(),width)
    plt.yticks(X,months)
    plt.title(f"{title} By Month")
    plt.xlabel("Amount Spent ($)")
    plt.ylabel("Months")
    plt.show()
    return months, list(total_by_month.values())


def BudgetMaker(long_term_payment):
    """Allows the user to create their desired budget, with last 6 months spending used to compare"""
    if os.path.isfile("./budget.txt"):
        print("Budget already created. Would you like to adjust it?")
        while True:
            answer = input("Type YES to adjust, or NO to use the current one")
            if answer.upper() == "YES":
                break
            elif answer.upper() == "NO":
                return
            else:
                print("Answer invalid. Please try again\n")
    cat_dict = avg_spending_by_category_long_term(long_term_payment)
    cat_list = ['Food & Drink', 'Health & Wellness', 'Shopping', 'Gas', 'Groceries', 'Bills & Utilities', 'Entertainment', 'Travel', 'Education', 'Fees & Adjustments', 'Gifts & Donations', 'Personal']
    budget = open("budget.txt", "w")
    #Is this used for anything
    print("How much would you like to spend on average per day in total")
    while True:
        total_spending = input("Enter dollar amount here: $")
        try:
            float(total_spending)
            break
        except:
            print("Did not enter a number. Please try again \n")
    dict1 = {}
    for cat in cat_list:
        if cat in cat_dict: 
            print(f"\nOn average, you spend {cat_dict[cat]} on {cat} per month")
        else:
            print(f"\nOn average, you spend 0 on {cat} per month")
        goal = input(f"How much would you like to spend in the category of {cat}: $")
        dict1[cat] = goal
    print("Your budget is complete")
    budget.write(f"Average Spending Per Day Goal_{total_spending}_\n")
    for cat in cat_list:
        budget.write(f"{cat}_{dict1[cat]}_\n")


def CreateBudgetDict():
    """Creates a dictionary for the budget from the txt file"""
    with open("budget.txt", "r") as file:
        budget1 = file.readlines()
        dict1 = {}
        for line in budget1:
            list1 = line.split("_")
            key = list1[0]
            value = list1[1]
            dict1[key] = value
    return dict1
        
def Compare(payment_list,long_term_payment):
    """Makes a graph comparing spending this month to a users desired budget"""
    cat_spending = spending_by_category(payment_list)
    if not os.path.isfile("./budget.txt"):
        print("You have not made a budget yet. Would you like to?")
        while True:
            answer = input("Type YES to create a budget, or NO to return to the menu")
            if answer.upper() == "YES":
                BudgetMaker(long_term_payment)
                break
            elif answer.upper() == "NO":
                return
            else:
                print("Answer invalid. Please try again\n")
    budget = CreateBudgetDict() 
    del budget["Average Spending Per Day Goal"]
    new_cat_spending = {}
    for cat in budget:
        if cat in cat_spending:
            new_cat_spending[cat] = cat_spending[cat]
        else:
            new_cat_spending[cat] = 0
    short_cat = list(new_cat_spending.values())
    short_cat = [int(value) for value in short_cat]
    budget_cat = list(budget.values())
    budget_cat = [int(value) for value in budget_cat]
    categories = list(budget.keys())
    width = 0.4
    X = np.arange(len(categories)) 
    plt.figure(figsize=(6,10))
    plt.barh(X, short_cat, width, label = "Last Month")
    plt.barh(X+width,budget_cat,width,label = "Budget")
    plt.yticks(X+width/2,categories)
    plt.title("Spending By Category Compared to Budget")
    plt.ylabel("Categories")
    plt.xlabel("Amount Spent ($)")
    plt.legend()
    plt.show()
    



def data_processor(long_term_file, new_data):
    """Runs all of the functions creating the dictionaries in one function and returns all the values"""
    if len(long_term_file)>=6:
        length = 6
    else:
        length = len(long_term_file)
    day_short_data = spending_by_day(new_data)
    day_long_data = avg_spending_by_day_long_term(long_term_file)
    cat_short_data = spending_by_category(new_data)
    cat_long_data = avg_spending_by_category_long_term(long_term_file)
    loc_short_data = spending_by_location(new_data)
    loc_long_data = avg_spending_by_location_long_term(long_term_file)
    monthly_spending = spent_by_month_dict(long_term_file,new_data)
    monthly_payments = earn_by_month_dict(long_term_file,new_data)
    loc_short_data_sorted, loc_long_data_sorted = location_fixing(loc_short_data, loc_long_data)
    return length,day_short_data,day_long_data,cat_short_data,cat_long_data,loc_short_data,loc_long_data, monthly_spending, monthly_payments, loc_short_data_sorted, loc_long_data_sorted


def data_table(title,length, categorical, short_num, long_num):
    """Prints a formatted data table with this months spending, past 6 months spending and the difference"""
    print(f"{title:20}This Month  Last {length} Months  Change This Month")
    for i in range(len(categorical)):
        print(f"{categorical[i][0:18]:20}{short_num[i]:<12.2f}{long_num[i]:<15.2f}{short_num[i]-long_num[i]:<10.2f}")

def data_table_for_months(title,categorical, data):
    """Prints a formatted data table just for the spending/paying by month. Just has month and the amount"""
    print(f"Month      Amount {title}")
    for i in range(len(categorical)):
        print(f"{categorical[i]:10} {data[i]:<.2f}")

def graphs_and_data(long_term_file, new_data):
    """Creates all the graphs and data tables and formats things nicely"""
    length, day_short_data,day_long_data,cat_short_data,cat_long_data,loc_short_data,loc_long_data,monthly_spending, monthly_payments,loc_short_data_sorted, loc_long_data_sorted = data_processor(long_term_file, new_data)
    days, short_days, long_days = make_dow_bar(day_short_data, day_long_data,length)
    data_table("Days of The Week", length, days, short_days, long_days)
    print("\n")
    categories, short_cat, long_cat = make_cat_bar(cat_short_data, cat_long_data,length)
    data_table("Spending Categories",length, categories, short_cat, long_cat)
    print("\n")
    short_loc = make_loc_bar_short(loc_short_data)
    long_loc = make_loc_bar_long(loc_long_data,length)
    data_table("Spending Locations",length, list(loc_short_data_sorted.keys()), list(loc_short_data_sorted.values()), list(loc_long_data_sorted.values()))
    print("\n")
    months, spending_data = make_spend_by_month_bar("Spending",monthly_spending)
    data_table_for_months("Spent",months, spending_data)
    print("\n")
    months, payment_data = make_spend_by_month_bar("Payments",monthly_payments)
    data_table_for_months("Paid",months, payment_data)
    print("\n")
            