from datetime import datetime, timedelta
import sys


class Week:
    def __init__(self, week_num, days):
        self.week_num = week_num
        self.days = days[1:]  # don't keep the week
        self.training_days = []

    def __str__(self):
        print(self.days)
        return f"week num: {self.week_num}"


class Input:
    def __init__(self, filename, race_date, is_time_based, create_entries):
        self.filename = filename
        self.race_date = race_date
        self.is_time_based = is_time_based
        self.create_entries = create_entries


def read_file(filename):
    weeks = []
    with open(filename) as file_in:
        header = file_in.readline()
        expected_header_fields = ["Week", "Mon", "Tues", "Wed", "Thur", "Fri", "Sat", "Sun"]
        actual_header_fields = header.split(",")

        # removes the pesky carriage return at the end of the line
        actual_header_fields[-1] = actual_header_fields[-1].strip()
        if actual_header_fields != expected_header_fields:
            print(f"actual_header_fields: {actual_header_fields}")
            print(f"Error: header fields expected to be: {','.join(expected_header_fields)}")
            print_usage_and_exit()

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
    return datetime.strftime(d, "%a %B %d, %Y")


def print_usage_and_exit():
    print("usage: python race_scheduler.py <schedule.csv> <race_date_in_YYYY-MM-DD> <distance|time> [--create-entries]")
    sys.exit()


def validate_args(args):
    if len(args) < 4:
        print("Not enough arguments")
        print_usage_and_exit()

    filename = args[1]
    race_date_raw = args[2]
    unit = args[3]
    create_entries = False
    if len(args) == 5:
        if args[4] == "--create-entries":
            create_entries = True
        else:
            print("Error: unrecognized argument")
            print_usage_and_exit()
    elif len(args) > 5:
        print("Too many arguments")
        print_usage_and_exit()

    if unit != "distance" and unit != "time":
        print_usage_and_exit()

    is_time_based = unit == "time"
    race_day = datetime.strptime(race_date_raw, "%Y-%m-%d")

    return Input(filename, race_day, is_time_based, create_entries)


def main():
    print(f"Welcome to the race scheduler!")
    input_args = validate_args(sys.argv)

    weeks = read_file(input_args.filename)
    current_date = input_args.race_date
    today = datetime.today().date()
    for w in reversed(weeks):
        for d in reversed(w.days):
            if d.lower() != "rest":
                if input_args.is_time_based:
                    w.training_days.insert(0, (d, current_date))
                else:
                    w.training_days.insert(0, (float(d), current_date))
            current_date = current_date - timedelta(days=1)

    print("*** final schedule ***")
    found_today = False

    for w in weeks:
        print(f"\nweek num: {w.week_num}")
        for i, d in enumerate(w.training_days):
            day = d[1]
            activity = d[0]

            here = ""
            if not found_today:
                if today < day.date():
                    print("****** WE ARE HERE ******")
                    found_today = True
                elif today == day.date():
                    here = " ****** IT IS TODAY ******"
                    found_today = True

            if input_args.is_time_based:
                print(format_date(day) + ": " + activity + here)
            else:
                print(format_date(day) + ": " + "{:2.1f}".format(activity) + " km" + here)


if __name__ == "__main__":
    main()