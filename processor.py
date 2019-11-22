f = open("Bush Polls.csv", "r")
output = "Time, Net approval rating, No opinion\n"
start_year = 2001
while True:
    line = f.readline()
    if line:
        cells = line.split(",")
        time = cells[0].split(" ")  # Add a / for 538, change 0 to 4
        months = {"Jan": 0, "Feb": 31, "Mar": 59, "Apr": 89, "May": 120, "Jun": 150, "Jul": 181, "Aug": 212,
                  "Sep": 242,"Sept":242, "Oct": 273, "Nov": 303, "Dec": 334}
        elapsed_time = 0
        print(time)
        try:
            if int(time[2].split("-")[1]) > 31:
                elapsed_time = 365 * int(time[2].split("-")[1]) - start_year * 365
                elapsed_time += months[time[3]]
            else:
                elapsed_time = 365 * int(time[0]) - start_year * 365
                elapsed_time += months[time[1]]
        except ValueError:
            elapsed_time = 365 * int(time[0]) - start_year * 365
            elapsed_time += months[time[2].split("-")[1]]
        end_bit = time[len(time)-1].split("-")
        elapsed_time += int(end_bit[len(end_bit)-1]) - 20
        net_approval = (int(cells[1]) - int(cells[2]))
        no_opinion = int(cells[3])
        output += str(elapsed_time) + "," + str(net_approval) + "," + str(no_opinion) + "\n"
    else:
        break
f.close()
f = open("Bush.csv", "w")
f.write(output)
f.close()
