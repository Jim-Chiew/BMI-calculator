from flask import Flask, render_template, request, make_response
import pickle
from pandas import DataFrame
import os.path
from datetime import datetime


# ______________ Database_________________
database = {}


def exporting():
    dict_for_csv = {}
    for users in database:
        dict_for_csv[database[users].name] = vars(database[users])

    df = DataFrame(dict_for_csv)
    df.to_csv("users.csv")
    df.to_json("users.json")


def insert_data(user):
    global database

    if os.path.isfile("database.pkl"):
        database = pickle.load(open('database.pkl', 'rb'))

    if user.name in database:
        database[user.name].entry.insert(0, {"datetime": user.datetime, "height": user.height, "weight": user.weight, "bmi": user.bmi()})
    else:
        database[user.name] = user

    pickle.dump(database, open('database.pkl', 'wb'))
    exporting()


def retrieve_data(name):
    global database
    database = pickle.load(open('database.pkl', 'rb'))

    if name in database:
        user = database[name]
        return vars(user)
    else:
        return make_response("User not found", 400)


# ________________ Calculate _______________
class User(object):
    def __init__(self, name, height, weight, dob):
        self.name = name
        self.dob = dob
        self.height = float(height)
        self.weight = float(weight)
        self.datetime = datetime.now()
        self.entry = [{"datetime": self.datetime, "height": self.height, "weight": self.weight, "bmi": self.bmi()}]
        insert_data(self)

    def bmi(self):
        return self.weight / (self.height * self.height)


# _________________ API _________________-
app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def calculate():
    if request.method == 'POST':
        usr = User(request.form['name'], request.form['height'], request.form['weight'], request.form['dob'])
        return vars(usr)
    else:
        return render_template('main.html')


@app.route('/user')
def show_user_profile():
    user = request.args.get('user')
    return retrieve_data(user)


app.run(debug=True)
