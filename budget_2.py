"""
	budget_2.py

        Written by John O'Hara
        Last Updated March 28th, 2017

		A more revised version of that budget idea that I had a couple months back.
        This one will store months in their own files in a "./budget_data" directory.

        The data files will have the same structure as they did previously - first line
        is number of workdays for the given month, second line is the budget goal, 
        and the third line is a CSV line with the results of each shift so far.


            !!! - Should files have a given extension/indicator?

                Right now they're like this: "data"

                    25
                    800
                    150,100,50

                This would make them like this: "data.bud"

                    $BUDGETDATA
                    25
                    800
                    150,100,50

                Basically, the frist line would always be a specific 
                string to indicate the file is formatted in a certain
                way.

            !!! - Another idea - add more of these tags to add metadata to the 
            files - like a description of the month, etc.



            !!! - Add a way to classify expenses: necessary (rent, bills), savings (non-essential
            but desired financial growth), entertainment (non-essential and first to go), that 
            way when the number is crunched it will tell you how much you need to make 
            the bare necessities as well as how much you will need to make your goal.




            !!!!!!!!!!!!!!!!!!!!!!
            There's an issue saving files. Sometimes the directory disappears, most of the time
            the file will disappear. I need to examine this more.



            I found this issue - it uses the present working directory instead of an absolute 
            directory path. So this shit will work differently based on whichever directory
            you choose. I think I need to make a way to detect where the script itself is, and
            then base it all off of that. 
            !!!!!!!!!!!!!!!!!!!!!!
"""
import os
import re

div = "-" * 29
budget_dir = "{}/budget_data".format(os.path.dirname(os.path.abspath(__file__)))
money_pattern = r'^\d+\.?\d+$'
last_updated = "March 28th, 2017"


def scan_budget_files():
    # check if .budget_data exists

    if not os.path.isdir(budget_dir):
        print("Budget data directory doesn't exist, creating...")
        os.makedirs(budget_dir)

    budget_files = list()

    for item in os.listdir(budget_dir):
        if os.path.isfile("{}/{}".format(budget_dir, item)):
            budget_files.append(item)

    return budget_files

# waits for one of a specific input choices, defaults to y/n

# should I make this a dictionary? that way I could do something
# like this: {"y" : "yes"} so each could have a verbose 
# explanation. Maybe.
def input_choice(valid_choices=['y','n']):
    """
        Here's a future plan: I want to separate different input tokens, split 
        at a space character. This would allow you to do something like this:

            "o file_name"

        This would read the first token, o, as an open command, and the second 
        token, file_name, as an argument to be passed to the next input_choice. 
        This could be pretty easy to implement as every option that asks for a
        target will immediately ask for that target after the option is selected.
    """
    choice_string = "("

    for choice in valid_choices[:-1]:
        choice_string = "{}{}/".format(choice_string, choice)

    choice_string = "{}{})".format(choice_string, valid_choices[-1])

    while True:
        choice = input()

        if choice.lower() in valid_choices:
            return choice
        else:
            print("Please enter a valid input: {}".format(choice_string), end=" ")

def list_all_files(files, display_count=True):
    if display_count:
        print("{} file(s) in total.\n".format(len(files)))
    print("All files:")
    for file in files:
        print("    - {}".format(file))

def format_budget(days_in_period, budget_goal, shifts_logged):
    days_remaining = days_in_period - len(shifts_logged)
    shifts_worked = len(shifts_logged)
    profit = 0 
    for shift in shifts_logged:
        profit = profit + shift
    goal_remaining = budget_goal - profit

    print("Goal Progress:       ${:.2f} of ${:.2f}, {:.2f}%".format(profit, budget_goal, (profit/budget_goal)*100))
    print("Days Remaining:      {} of {} total".format(days_remaining, days_in_period))
    if profit < budget_goal:
        print("Profit Goal:         ${:.2f} per day\n".format(goal_remaining/days_remaining))
    else:
        print("Profit Goal:         Goal met! Now don't blow all that money on something stupid.") 

def current_report(shifts_logged):
    if len(shifts_logged) is not 0:
        print("\nDaily Profit to Date:\n")

        day = 1
        
        for shift in shifts_logged:
            print("    {} - {}".format(day, shift))

        print()
    else:
        print("\nNo shifts logged.\n")

def file_info(days_in_period, budget_goal, file_name):
    print("Current File:        {}".format(file_name))
    print("Days in Period:      {}".format(days_in_period))
    print("Target Budget:       ${:.2f}\n".format(budget_goal)) 

def print_title():
    print("\n{}".format(div))
    print("Budget Script v2.0")
    print("Written by John O'Hara")
    print("Last Updated {}".format(last_updated))
    # all test stuff
    print("Running from {}".format(os.path.dirname(os.path.abspath(__file__))))
    print("Looking for {}".format(budget_dir))
    print(os.path.isdir(budget_dir))
    print(div, end="\n\n")

def quit_program():
    print("\nGoodbye!\n")
    quit()

def main(args=None):
    print_title()

    files = scan_budget_files()

    if len(files) == 0:
        print("No budget files found :(")
    else:
        print("{} files found.".format(len(files)))

    while True:
        # main program loop
        print()
        print("(c)reate/(o)pen/(d)elete/(l)ist all/(q)uit? ", end="")

        file_option = input_choice(["c", "o", "d", "l", "q"])

        if file_option.lower() == "c":
            print("Name? (best to use some form of month-year) ", end="")
            file = None

            while True:
                name = input()
                if os.path.isfile("{}/{}".format(budget_dir, name)):
                    print("{} already exists. Please provide a different name: ".format(name), end="")
                else:
                    file = open("{}/{}".format(budget_dir, name), "w")
                    break

            print("Workdays in month (1-31)? ", end="")

            while True:
                days = input()

                try:
                    days = int(days)
                except:
                    print("Please enter an integer between 1-31: ", end="")
                else:
                    if days < 1 or days > 31:
                        print("Please enter an integer between 1-31: ", end="")
                    else:
                        file.write("{}\n".format(days))
                        break

            print("Budget goal? ", end="")

            while True:
                goal = input()

                try:
                    goal = float(goal)
                except:
                    print("Please enter a positive integer: ")
                else:
                    file.write("{}\n".format(goal))
                    break

            file.write("no_data")
            print("Budget file '{}' created successfully!".format(name))

            file.close()

            files = scan_budget_files()
        elif file_option.lower() == "o":
            if len(files) == 0:
                print("No files exist!")
            else:
                print("Open which file? ", end="")

                file_name = input()

                try:
                    file = open("{}/{}".format(budget_dir, file_name))
                except:
                    print("File doesn't exist. Please enter a valid file name.")
                    # make way to ask to create a file - maybe make file creation a method and
                    # call it here as well as after the "o" option?
                else:
                    print("File opened successfully!\n")
                    
                    days_in_period = int(file.readline())
                    budget_goal = float(file.readline())
                    shifts_string = file.readline()

                    file_info(days_in_period, budget_goal, file_name)


                    if re.search(r'no_data', shifts_string):
                        shifts_logged = list()
                    else:
                        shifts_logged = [float(i) for i in shifts_string.split(",") if i is not "\n"]

                    # =========================================
                    # Main File Loop
                    # =========================================

                    new_loop = True

                    while True:
                        if new_loop:
                            format_budget(days_in_period, budget_goal, shifts_logged)
                            new_loop = False

                        print("(a)dd shift/(c)lose file/(v)iew shifts/(q)uit?", end=" ")

                        action_choice = input_choice(["a", "c", "v", "q"])

                        if action_choice == "a":
                            while True:
                                print("Shift profit?", end=" ")
                                shift_value = input()

                                """
                                    ADD A WAY TO MATCH MORE THAN JUST INTS, ALLOWING FOR DECIMALS.
                                    This regex can't handle a decimal point currently.
                                """

                                if re.search(money_pattern, shift_value):
                                    shifts_logged.append(float(shift_value))
                                    print("Successfully logged ${}.\n".format(shift_value))
                                    new_loop = True
                                    break
                                else:
                                    print("Please enter only a number. ")

                        elif action_choice == "c":
                            print("Saving file...done.")
                            # write changes like so.... 
                            """
                                1. open the file in read-only mode
                                2. read all lines into an array of lines
                                3. close the file
                                4. modify the array of lines as the working file
                                5. reopen the file in write mode
                                6. overwrite the file with the array of lines
                            """

                            # This is like step 1.5 as we've already got the file open
                            file.seek(0) # rewind that tape baby
                            file_data = file.readlines()

                            if len(shifts_logged) is not 0:
                                shifts_string = ",".join([str(i) for i in shifts_logged])
                            else:
                                shifts_string = "no_data"

                            file_data[-1] = shifts_string

                            file.close()

                            file = open("{}/{}".format(budget_dir, file_name), "w")

                            for data_line in file_data:
                                file.write(data_line)

                            break

                        elif action_choice == "v":
                            current_report(shifts_logged)

                        elif action_choice == "q":
                            quit_program()

                    file.close()

        elif file_option.lower() == "d":
            if len(files) == 0:
                print("No files exist!")
            else:
                print("Delete which file? ", end="")

                target = input()

                try:
                    del_file = open("{}/{}".format(budget_dir, target))
                except:
                    print("File doesn't exist, no need to delete!")
                else:
                    del_file.close()
                    os.remove("{}/{}".format(budget_dir, target))
                    print("'{}' deleted successfully!".format(target))
                    files = scan_budget_files()
        elif file_option.lower() == "l":
            if len(files) == 0:
                print("No files exist!")
            else:
                list_all_files(files)
        elif file_option.lower() == "q":
            quit_program()

if __name__ == "__main__":
    main()
