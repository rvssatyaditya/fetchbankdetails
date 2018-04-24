from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy  # imported SQLAlchemy for data storage and retrival
import psycopg2
import pandas as pd

app = Flask(__name__)
# Initializing Database String
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bankrestapi:123@localhost/bankrestapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db contains flask object
db = SQLAlchemy(app)
res = []


# created Banks Model to fetch Bank related data
class Banks(db.Model):
    # __tablename__ = 'books'
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))

    # Constructor of Books Model
    def __init__(self, id, name) -> object:
        self.id = id
        self.name = name


# created Branches Model to fetch Branch related data
class Branches(db.Model):
    # __tablename__ = 'author';
    ifsc = db.Column(db.String, primary_key=True)
    bank_id = db.Column(db.String)
    branch = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    district = db.Column(db.String)
    state = db.Column(db.String)

    # Constructor of Branch Model
    def __init__(self, ifsc, bank_id, branch, address, city, district, state):
        self.ifsc = ifsc
        self.bank_id = bank_id
        self.branch = branch
        self.address = address
        self.city = city
        self.district = district
        self.state = state

#Routing and handling the Response of the server to different pages.
@app.route('/', methods=['POST', 'GET'])
def init():
    if request.method == 'POST':
        if request.form['action'] == 'Check Details via IFSC CODE':
            return render_template('Query.html')
        elif request.form['action'] == 'Check Branches':
            return render_template('Query Branch.html')
        else:
            return render_template('Home.html')
    return render_template('Home.html')


@app.route('/Query', methods=['POST', 'GET'])
def home():
    pd.set_option('display.max_colwidth', -1)
    conn = psycopg2.connect('postgresql://lonewolf:123@localhost/bankrestapi')
    c = conn.cursor()
    if request.method == "POST":
        text = request.form['text']
        if text == "":
            msg = 'Invalid IFSC CODE'
            return render_template('Query.html', msg=msg)

        try:
            c.execute( "select name,id,branch,address,city,district,state from banks,branches where banks.id=branches.bank_id and branches.ifsc=(%s) LIMIT 1",(text,))
            data = c.fetchall()
            df = pd.DataFrame(data)
            print(df.to_string(index=False))
            return render_template('result.html', df=df)

        except:
            return render_template('layout.html')

    return render_template('Query.html')



@app.route('/redirect', methods=['POST', 'GET'])
def redirect():
    return render_template('Query.html')


@app.route('/Query_branch', methods=['POST', 'GET'])
def query_branch():
    if request.method == 'POST':
        conn = psycopg2.connect('postgresql://lonewolf:123@localhost/bankrestapi')
        c = conn.cursor()
        bank_name = request.form['bn']
        city = request.form['city']
        if (bank_name == "") or (city == ""):
            msg = 'Please Enter required Details'
            return render_template('Query branch.html', msg=msg)
        try:
            c.execute("select Distinct branch from branches,banks where branches.city=(%s) and banks.name=(%s) and Banks.id=branches.bank_id",
                      (city, bank_name))
            data1 = c.fetchall()
            df1 = pd.DataFrame(data1)
            cdf1=df1.to_string(index=False)
            print(cdf1)
            return render_template('result_branch.html', df1=df1)

        except:
            return render_template('layout.html')

    return render_template('Query_branch.html')

@app.route('/redirect_branch', methods=['POST', 'GET'])
def redirect_branch():
    return render_template('Query Branch.html')



if __name__ == '__main__':
    app.run()
