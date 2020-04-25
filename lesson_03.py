import datetime
import json
import os
import random
import string
from faker import Faker
import pandas as pd
from flask import Flask
from pip._vendor import requests
from flask import request
from flask import abort
import sqlite3

print("hello")
app = Flask('app')

# Constants
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def hello():
    return 'Hello'

@app.route('/now')
def now():
    return str(datetime.datetime.now())

@app.route('/gen-password')
def gen_password():
    length = request.args['length']
    try:
        val = int(length)
        if (val > 0):
            if (8 <= val <= 24):
                return ''.join(
                    [
                        random.choice(string.ascii_lowercase)
                        for _ in range(val)
                    ]
                )
            else:
                return "Length should be in the range from 8 to 24."
        else:
            return "Length should be bigger than 0."
    except ValueError:
        return ("Length should be a number!")


@app.errorhandler(400)
def handle_bad_request(error):
    return("Please provide the required length of the password by adding ?length=N " \
          "parameter in the URL, where N is equal to the number of required length")

@app.route('/read-requirements')
def read_requirements():

    file_path = ROOT_DIR + '/requirements.txt'
    file = open(file_path, 'r')
    file_contents = file.read()
    result_string = ''.join(file_contents)
    file.close()
    return result_string;

@app.route('/100-random-users')
def random_users():
    fake = Faker()
    result_string = "\n".join([
        fake.name() + ' ' + fake.email()
        for _ in range(100)
    ])
    return str(result_string)

@app.route('/average-height-weight')
def average_height_weight():
    file_path = ROOT_DIR + '/hw.csv'
    data = pd.read_csv(file_path, header=0, names = ["index", "height", "weight"])
    height_mean_cm = round(data["height"].mean() * 2.54, 2)
    weight_mean_kg = round(data["weight"].mean() / 2.205, 2)

    # Height and weight in inches and pounds, respectively
    # height_mean = data["height"].mean()
    # weight_mean = data["weight"].mean()
    # print(str(height_mean) + " " + str(weight_mean))

    return 'Average height of students is = ' + str(height_mean_cm) + " cm;" \
           + '\n' + 'Average weight of students is = ' \
           + str(weight_mean_kg) + " kg;"

@app.route('/get-astronauts')
def get_astronauts():
    response = requests.get('http://api.open-notify.org/astros.json')
    if response.status_code == 200:
        resp = json.loads(response.content)
        return f"Astronauts number: {resp['number']}"
    else:
        return f"Error code is: {response.status_code}"

@app.route('/get-unique-firstnames')
def get_unique_firstnames():
    query = 'SELECT DISTINCT FirstName FROM customers'
    records = execute_query(query)
    return str(records)

@app.route('/filter-by-state-and-city')
def get_filtered_by_state_and_city():
    query = 'SELECT * FROM customers GROUP BY STATE, CITY'
    records = execute_query(query)
    return str(records)

@app.route('/get-revenue')
def get_revenue():
    query = 'SELECT SUM(UnitPrice * Quantity) FROM invoice_items'
    records = execute_query(query)
    return str(records)

def execute_query(query):
    db_path = os.path.join(ROOT_DIR, 'chinook.db')
    print(db_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    records = cur.fetchall()
    return records

app.run()
