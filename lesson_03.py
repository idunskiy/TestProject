import datetime
import random
import string
from faker import Faker
import pandas as pd


from flask import Flask

print("hello")
app = Flask('app')

@app.route('/')
def hello():
    return 'Hello'

@app.route('/now')
def now():
    return str(datetime.datetime.now())

@app.route('/gen_password')
def gen_password():
    return ''.join(
    [
        random.choice(string.ascii_lowercase)
        for _ in range(10)
    ]
    )

@app.route('/read-requirements')
def read_requirements():
    file_path = '/Users/ivan/PythonProjects/TestProject/requirements.txt'
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
    file_path = '/Users/ivan/PythonProjects/TestProject/hw.csv'
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

app.run()