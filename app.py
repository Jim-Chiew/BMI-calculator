from flask import Flask, render_template, request
import pickle


# ______________ Database_________________
database = {}


def insert_data(user):
    database[user.name] = user
    pickle.dump(database, open('database.pkl', 'wb'))


def retrieve_data(name):
    global database
    database = pickle.load(open('database.pkl', 'rb'))

    if name in database:
        user = database[name]
        return "User " + user.name + " " + str(user.bmi())
    else:
        return "User don't exist"


# ________________ Calculate _______________
class User:
    def __init__(self, name, height, weight):
        self.name = name
        self.height = float(height)
        self.weight = float(weight)
        insert_data(self)

    def bmi(self):
        return self.weight / (self.height * self.height)


# _________________ Web people _________________-
app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        usr = User(request.form['name'], request.form['height'], request.form['weight'])
        ans = 'Welcome ' + usr.name + " " + str(usr.bmi())
        return ans
    else:
        return render_template('main.html')


@app.route('/user')
def show_user_profile():
    user = request.args.get('user')
    return retrieve_data(user)


app.run()
