from datetime import datetime, timedelta
import sys

# MILE_TO_KM = 1.609


class Week:
    def __init__(self, week_num, days):
        self.week_num = week_num
        print(f"original days: {days}")
        self.days = days[1:]  # days[0] = Monday # TODO get rid of the total column in the km sheet
        print(f"after: {self.days}")
        self.training_days = []

    def __str__(self):
        print(self.days)
        return f"week num: {self.week_num}"


def read_file(filename):
    weeks = []
    with open(filename) as file_in:
        header = file_in.readline()
        print(f"header: {header}")
        # if header != "Week,Mon,Tues,Wed,Thur,Fri,Sat,Sun,Total":
        #     print("header expected to be: Week,Mon,Tues,Wed,Thur,Fri,Sat,Sun,Total")
        #     sys.exit()

        week_num = 1
        for raw_line in file_in:
            days = raw_line.split(",")
            w = Week(week_num, days)
            weeks.append(w)
            # for d in days:
            #     print(d, end="")
            week_num += 1
            # print(raw_line, end="")

    return weeks


def format_date(d):
    print(datetime.strftime(d, "%a %B %d, %Y"))


def print_usage_and_exit():
    print("usage: python marathon_scheduler.py <schedule.csv> <race_date_in_YYYY-MM-DD> <distance|time>")
    sys.exit()


def main():
    print(f"Welcome to the marathon scheduler!")
    if len(sys.argv) != 4:
        print("Not enough arguments")
        print_usage_and_exit()

    filename = sys.argv[1]
    race_date_raw = sys.argv[2]
    unit = sys.argv[3]
    if unit != "distance" and unit != "time":
        print_usage_and_exit()

    is_time_based = unit == "time"

    print(f"filename: {filename}")
    weeks = read_file(filename)
    race_day = datetime.strptime(race_date_raw, "%Y-%m-%d")
    print(f"race_date: {race_date_raw}")
    print(f"race day: {race_day}")
    current_date = race_day
    today = datetime.today()
    for w in reversed(weeks):
        print(w)
        print(f"week_num: {w.week_num}, num days = {len(w.days)}")
        # print(f"week_num: {w.week_num}, mon = {w.days[0]}, sun = {w.days[6]}")
        for d in reversed(w.days):
            if d != "Rest":
                if is_time_based:
                    w.training_days.insert(0, (d, current_date))
                else:
                    w.training_days.insert(0, (float(d), current_date))
            current_date = current_date - timedelta(days=1)

    print("*** final schedule ***")
    found_today = False
    for w in weeks:
        print(f"\nweek num: {w.week_num}")
        for i, d in enumerate(w.training_days):
            if is_time_based:
                print(datetime.strftime(d[1], "%a, %B %d, %Y") + ": " + d[0])
            else:
                print(datetime.strftime(d[1], "%a, %B %d, %Y") + ": " + "{:2.1f}".format(d[0]) + " km")

            if not found_today and d[1] >= today:
                found_today = True
                print("****** WE ARE AROUND HERE ******")


if __name__ == "__main__":
    main()