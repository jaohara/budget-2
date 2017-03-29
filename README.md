#Budget Script v 2.0
Written by John O'Hara

Modified March 28th, 2017
-------------------------

##About

A simple command-line application for figuring out your budget.

The initial need and idea from this arose from working in the food-service industry, where you're more commonly paid daily via tips than weekly via paycheck. The fact that you have a daily income and your money is more often than not split between your bank account, cash, and checks due to you by the restaurant made it difficult to use something such as Mint. I created this simple budget script that was more fitting for my purposes.


##How-To

Run the budget_2.py script to use the application. It will create a ./budget_data directory if one does not currently exist and use this to store any created budget files.

When a budget file is created, you give it a name to describe the period that you're trying to track - a given month, a given week, etc - and you add the profit from your day after all of your expenses to the budget file. The script will calculate the rate at which you need to continue saving to meet your goal for the period.


