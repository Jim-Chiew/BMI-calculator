from flask import Flask, render_template, request, make_response
import pickle
from pandas import DataFrame
import os.path
from datetime import datetime
from dateutil.relativedelta import relativedelta


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
        database[user.name].entry.insert(0, {"datetime": user.datetime, "height": user.height, "weight": user.weight, "bmi": user.bmi, "status": user.status})
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
        self.age = self.get_age()
        self.bmi = self.bmi()
        self.status = self.bmi_range()
        self.entry = [{"datetime": self.datetime, "height": self.height, "weight": self.weight, "bmi": self.bmi, "status": self.status}]
        insert_data(self)
        self.info = self.suggestions()

    def bmi(self):
        return self.weight / (self.height * self.height)

    def get_age(self):
        if self.dob:
            return relativedelta(self.datetime.date(), datetime.strptime(self.dob, '%Y-%m-%d')).years
        
    def bmi_range(self):
        if self.bmi < 0:
            bmi_range = "Invalid"
        elif self.bmi < 18.5:
            bmi_range = "Underweight"
        elif 18.5 <= self.bmi < 25.0:
            bmi_range = "Healthy Weight"
        else:
            bmi_range = "Overweight"

        return bmi_range

    def suggestions(self):
        suggestion = ""

        if self.age:
            if self.status == "Healthy Weight":
                suggestion = "Good job! Keep it up and maintain your BMI."
            elif self.age < 60 and self.status == "Underweight":
                suggestion = """To increase BMI
Diet:
Eating more frequently. Slowly begin to eat 5 to 6 smaller meals during the day.
Choosing food with lots of nutrients. Set up a routine to eat and drink things you like and that have a lot of nutrients as well as calories. 
Add extras to your dishes for more calories, such as cheese in casseroles or nut butter on whole-grain toast. You also can add dry milk or liquid milk to foods for extra protein and calories. Some examples are mashed potatoes or soups.
Try smoothies and shakes. Avoid beverages with few nutrients or calories, such as diet soda.
Beverages can make you feel full. If that's the case for you, avoid drinking during a meal or before. But make sure you are drinking enough throughout the day.

Exercise:
45 minutes of running 3 times a week
Heavy weight lifting
Calisthenics
"""
            elif self.age < 60 and self.status == "Overweight":
                suggestion = """Diet:
High protein and low calorie diet should be taken.
Drink plenty of fluids
Eat small portions of meals in short intervals.
Avoid red meat
Eat plenty of fruits and vegetables.

Exercise:
75mins jogging 2 times a week
Weight lifting
90mins cycling 1 time a week
"""
            elif self.age >= 60 and self.status == "Underweight":
                suggestion = """Diet:
Eat small meals and snacks regularly throughout the day, rather than attempting to eat three large meals
Keeping a ready supply of healthy snacks (e.g. dried fruits and unsalted nuts) within easy reach around your home
Avoiding foods containing high levels of sugar or saturated fats, as these are full of empty calories
Increasing their intake of full-fat milk or cheese; try adding these ingredients to meals or drinks they already consume regularly
Take on more high-energy foods that are rich in calories, such as nuts, beans, pulses, porridge, olive oil and pasta

Exercise:
45 mins of light jogging, 3 times a week
"""
            elif self.age >= 60 and self.status == "Overweight":
                """Diet:
High protein and low calorie diet should be taken.
Drink plenty of fluids
Eat small portions of meals in short intervals.
Avoid red meat
Eat plenty of fruits and vegetables.

Exercises:
Walking up to 45 minutes a day
Light Yoga under supervision
Indoor cycling
Light weight training
Pilates

Exercises to be avoided include:

Bench-press
Pull ups
Squats
Long distance cycling
Anything else that requires great body effort or produces stress on joints.
"""
            elif self.status == "Invalid":
                print("Invalid BMI")

            return suggestion


# _________________ API _________________-
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route("/", methods=['POST', 'GET'])
def calculate():
    if request.method == 'POST':
        usr = User(request.form['name'], request.form['height'], request.form['weight'], request.form['DOB'])
        return vars(usr)
    else:
        return render_template('main.html')


@app.route("/database")
def database_page():
    return render_template('database.html')


@app.route('/user')
def show_user_profile():
    user = request.args.get('user')
    return retrieve_data(user)


app.run(debug=True)
