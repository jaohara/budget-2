# little budget app idea.

# data is stored in the following format:

# line 1: shifts/work days per month
# line 2: savings goal
# line 3: CSV of income for days worked so far

def main(args=None):
    data_file = open('data', 'r')
    data_lines = data_file.readlines()

    """
        Gonna rework some stuff here
    """
    data_list = list()

    # this should strip newline chars
    for line in data_lines:
        data_list.append(line[:len(line)-1])

    data_file.close()

    total_days = int(data_list[0])
    total_goal = int(data_list[1])
    worked_shift_list = data_list[2].split(",")

    remaining_days = total_days - len(worked_shift_list)
    remaining_goal = total_goal

    for shift in worked_shift_list:
        remaining_goal -= int(shift)

    rate = remaining_goal/remaining_days

    print ("\n\n\n------------")
    print("Budget projections:\n")
    print("Remaining Goal: ${}".format(remaining_goal))
    print("Shifts remaining: {}\n".format(remaining_days))
    print("Savings goal: ${:.2f} per day".format(rate))
    print ("------------\n\n\n")

if __name__ == "__main__":
    main()