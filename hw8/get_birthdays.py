from collections import defaultdict
from datetime import datetime


def get_birthdays_per_week(users):

    birthdays_this_week = defaultdict(list)
    date_now = datetime.now()
    day_now = date_now.day

    for item in users:

        birthdays = item.get('birthday')
        birth_day = birthdays.day
        difference_day = birth_day - day_now

        if 0 <= difference_day <= 7:
            if birthdays.weekday() >= 5:
                birthdays_this_week['Monday'].append(item.get('name'))
            else:
                birthdays_this_week[birthdays.strftime(
                    '%A')].append(item.get('name'))

    for weekday in birthdays_this_week:
        print(f"{weekday}: {', '.join(birthdays_this_week.get(weekday))}")

# For tsting list users


users = [{'name': 'Olia', 'birthday': datetime(year=1997, month=4, day=17)},  # Thursday
         {'name': 'Sasha', 'birthday': datetime(
             year=1987, month=3, day=5)},  # Thursday
         {'name': 'Dima', 'birthday': datetime(
             year=1997, month=4, day=20)},  # Sunday
         {'name': 'Sveta', 'birthday': datetime(
             year=2000, month=4, day=15)},  # Saturday
         {'name': 'Katia', 'birthday': datetime(year=1988, month=4, day=20)}]  # Wednesday


get_birthdays_per_week(users)
