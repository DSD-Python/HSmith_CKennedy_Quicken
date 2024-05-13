<h1>Holly Smith and Chris Kennedy Quicken Credit Info</h1>

**Goal and Intended User**

The goal for this project is to provide users with the ability to analyze the financial data of their bank statements for the purposes of budgeting and financial planning. The target user is anyone who would like to make informed financial decisions by analyzing their spending and earning patterns. 

**Functionality**

As of now, the software allows users to upload their bank statements. It then pulls out certain data from these statements including the users' categories of spending and earning, the specific places where they have spent or earned money, and the dates of these transactions. It then produces several graphs which the user may find helpful for analysis of their spending. Users also have the option of creating a budget. After creating a budget, users may compare their actual spending to their budgeted spending.

**How To**

To use our software is simple:

- Step 1: Download all of the following files and place them in the same directory: Project_Functions.py, User_Functions.py, sym_encrypt.py, First_Time_User.ipynb, and Returning_User.ipynb.
  
- Step 2: Run the code in First_Time_User.ipynb, following the printed instructions in order to upload your bank statements.
  
- Step 3: Run the code in Returning_User.ipynb,following the printed instructions in order to upload your current bank statement. Select the option that best meets your need. Select D to terminate the program. 
  
**Main Elements:**

- Project_Functions.py: Contains functions that upload and congregate user data, create graphs, and create the Budget.txt budget, where the budget information is stored.
  
- User_Functions.py: Contains user experience functions. These provide instructions to users and allow them to input the name of the bank statements in their directory.

- sym_encrypt.py: Contains functions that allow for encryption of the user's long-term transaction file. 
  
- First_Time_User.ipynb: This file welcomes the first-time user, instructs them to download their bank statements in .csv form and place them in the same directory (folder) as this software and to input the names of these .csv files in chronolical order to create a long-term file. It also imports Project_Functions.py, sym_encrypt.py, and User_Functions in order to function. 

- Returning_User.ipynb: This file welcomes the returning user and instructs them to upload their most recent bank statement. It them offers the user a choice between viewing graphs that summarize their spending, create a budget, or compare their actual spending with their budgeted spending. It also imports Project_Functions.py, sym_encrypt.py, and User_Functions in order to function. 




We encrypt the file that is created by our software. However, our software requires the user to download their bank statements onto their computer. While we do not possess any of the user's data, security risks are present whenever one downloads sensitive data to their computer. For example, someone with malicious intent could gain remote access of the users computer and gain access to their files. To mitigate this risk, it is important to use computers with advanced malware protection systems, such as Apple computers.

Additional work that could improve this project is making it more user-friendly and visually appealing. In addition, this software only works with Chase bank statements. Additional work could make the software compatible with a wider range of bank statements. 


