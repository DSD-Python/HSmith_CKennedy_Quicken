import csv
from datetime import date
import pickle
import calendar
import numpy as np
import matplotlib.pyplot as plt
import os.path
import Project_Functions as pf
import sym_encrypt as se
from pathlib import Path

def user_input():
    """Allows the user to input the name of a statement file and converts the data to a list"""
    while True:
        file_name = input("Please input the name of your bank statement file omitting the file extension: ")
        try:
            data = pf.extract_data_from_csv(file_name)
            return data
        except:
            print("File does not exist in directory. Please try again\n")


def user_welcome():
    """This UX function allows the user to enter past statements in an iterative fashion to make the past payments file
    If the user has a file already the function does not allow them to overwrite it to prevent a user from accidentaly ruining the existing file"""
    if os.path.isfile("./credit_payment_history.pkl") or os.path.isfile("./credit_payment_history.pkl.box") or os.path.isfile("./credit_payment_history.pkl.box"):
        print("It looks like you've used our app before! We see you already have a file containing your previous payments")
        print("If this is correct and you'd like to upload this months data, go to the existing users file instead")
        print("If you'd like to recreate the file, simply delete the file titled 'credit_payment_history.pkl' and run this function again!")
        return
    print("Hello New User! Welcome to our App!")
    print("This file allows you to upload past bank statements to create a long term file that stores the information")
    print("This will allow you to see how your current spending comapres to your past\n")
    print("First, we're going to attempt to create a key in order to encrypt the long term file")
    print("If you receive no message, it is successful. If the message say it is already created, it's already good")
    se.create_secret_and_save()
    print("\nPlease download your bank statements in .csv form and place them in the same directory (folder) as this software")
    print("Please upload the files in chronological order, with the oldest being uploaded first\n")
    long_term_payment = []
    first_data = user_input()
    print("File succesfully uploaded\n")
    print("Would you like to upload another file?")
    long_term_payment.append(first_data)
    while True:
        answer = input("Please type YES or NO (all caps): ")
        if answer == "YES":
            while True:
                new_data = user_input()
                if new_data not in long_term_payment:
                    long_term_payment.append(new_data)
                    print("File succesfully uploaded\n")
                else:
                    print("Data already uploaded\n")
                print("Would you like to upload another file?")
                while True:
                    answer = input("Please type YES or NO (all caps): ")
                    if answer == "YES":
                        break
                    if answer == "NO":
                        pf.create_new_long_term_file(long_term_payment)
                        return
                    else:
                        print("Please enter correct response\n")
        if answer == "NO":
            pf.create_new_long_term_file(long_term_payment)
            break
        else:
            print("Please enter correct response\n")
    print("File succesfully created!")


def returning_user_start():
    """Makes sure a user has a long term file already. If they do it returns that data and asks them to upload this months data
    If they dont have one it tells the user to go to the first time user file to create one"""
    try:
        long_term_file = pf.open_long_term_file()
        print("Long term file accessed successfully")
    except:
        print("You do not have a long term statement file in this directory")
        print("If you've made one before, make sure it's in the correct directory")
        print("If you haven't, go to the first time user file to create it first")
        print("Do not run the following function without doing either of these first")
        return "one", "two"
    new_data = user_input()
    if new_data in long_term_file:
        print("Warning! This data has already been added to the long term file")
        print("If you wish to continue, just be aware that this months data is already included in past months averages\n")
    print("Here is the data from this month\n")
    print(new_data)
    return long_term_file, new_data



def Returning_User(long_term_file, new_data):
    """The main UX of the returning user file, it asks the user what it would like to do and utilizes functions in the project functions file to carry out these requests
    The user can see graphs and data, create a budget, compare their budget to their current spending, and add the current months payments to the long term file"""
    while True:
        print("How can I help you?\n A) View my Spending\n B) Create a Budget\n C) Compare Spending to Budget\n D) Add Current Months Data to Long Term File\n Q) Quit Application")
        Choice = input("Select Here: ")
        if Choice.upper() == "A":
            pf.graphs_and_data(long_term_file, new_data)
        elif Choice.upper() == "B":
            pf.BudgetMaker(long_term_file)
        elif Choice.upper() == "C":
            pf.Compare(new_data,long_term_file)
        elif Choice.upper() == "D":
            if new_data in long_term_file:
                print("Data already in long term file\n")
            else:
                long_term_file.append(new_data)
                pf.update_long_term_file(long_term_file)
                print("\nUpdate Successful\n")
        elif Choice.upper() == "Q":
            print("\nThank you for using our service!")
            return
        else:
            print("Not a Valid Choice. Please Try Again\n")