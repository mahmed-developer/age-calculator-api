from flask import Flask, request, jsonify
import time
from calendar import isleap

app = Flask(__name__)

def judge_leap_year(year):
    return isleap(year)

def month_days(month, leap_year):
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    elif month == 2 and leap_year:
        return 29
    elif month == 2 and not leap_year:
        return 28

@app.route('/')
def home():
    return "Welcome to the Age Calculator API!"

@app.route('/calculate', methods=['GET'])
def calculate_age():
    name = request.args.get('name')
    age = int(request.args.get('age', 0))
    localtime = time.localtime(time.time())

    year = int(age)
    month = year * 12 + localtime.tm_mon
    day = 0

    begin_year = int(localtime.tm_year) - year
    end_year = begin_year + year

    for y in range(begin_year, end_year):
        day += 366 if judge_leap_year(y) else 365

    leap_year = judge_leap_year(localtime.tm_year)
    for m in range(1, localtime.tm_mon):
        day += month_days(m, leap_year)

    day += localtime.tm_mday

    return jsonify({
        "name": name,
        "years": year,
        "months": month,
        "days": day
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
