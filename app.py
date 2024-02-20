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
    def __init__(self, name, height, weight, dob, range):
        self.name = name
        self.dob = dob
        self.height = float(height)
        self.weight = float(weight)
        self.range  = str(range)
        self.datetime = datetime.now()
        self.entry = [{"datetime": self.datetime, "height": self.height, "weight": self.weight, "bmi": self.bmi()}]
        insert_data(self)
        self.info = """To increase BMI
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

To decrease BMI
Diet:
High protein and low calorie diet should be taken.
Drink plenty of fluids
Eat small portions of meals in short intervals.
Avoid red meat
Eat plenty of fruits and vegetables.

Exercise:
75mins jogging 2 times a week
Weight lifting
90mins cycling 1 time a week"""

    def bmi(self):
        return self.weight / (self.height * self.height)
        
    def bmi_range(self):
	if bmi(self) < 0:
		print("Invalid BMI")
		self.range("Invalid")
    	elif bmi(self) < 18.5:
		print("Underweight")
	    	self.range("Underweight")
    	elif bmi(self) >= 18.5 and bmi(self) < 25.0:
		print("Healthy Weight")
	    	self.range("Healthy Weight")
    	else:
		print("Overweight")
	    	self.range("Overweight")

    def suggestions(self):
	if self.range == "Healthy Weight":
		print("Good job! Keep it up and maintain your BMI.")
	elif self.age < 60 and self.range == "Underweight":
		print("a")
	elif self.age < 60 and self.range == "Overweight":
		print("b")
	elif self.age >= 60 and self.range == "Underweight":
		print("c")
	elif self.age >= 60 and self.range == "Overweight":
		print("d")
	elif self.range == "Invalid":
		print("Invalid BMI")

# _________________ API _________________-
app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def calculate():
    if request.method == 'POST':
        usr = User(request.form['name'], request.form['height'], request.form['weight'], request.form['DOB'])
        return vars(usr)
    else:
        return render_template('main.html')


@app.route('/user')
def show_user_profile():
    user = request.args.get('user')
    return retrieve_data(user)


app.run(debug=True)
