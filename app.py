import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import sqlite3

import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
import pandas as pd
import numpy as np
import pickle
import sqlite3
import random

import smtplib 
from email.message import EmailMessage
from datetime import datetime

warnings.filterwarnings('ignore')



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/about1")
def about():
    return render_template("about.html")

@app.route("/about2")
def about1():
    return render_template("about1.html")

@app.route("/about3")
def about2():
    return render_template("about2.html")

@app.route("/about4")
def about3():
    return render_template("about3.html")

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')

@app.route("/signup")
def signup():
    global otp, username, name, email, number, password
    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    otp = random.randint(1000,5000)
    print(otp)
    msg = EmailMessage()
    msg.set_content("Your OTP is : "+str(otp))
    msg['Subject'] = 'OTP'
    msg['From'] = "manojtruprojects@gmail.com"
    msg['To'] = email
    
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("manojtruprojects@gmail.com", "qvhanvuuxyogomze")
    s.send_message(msg)
    s.quit()
    return render_template("val.html")

@app.route('/predict_lo', methods=['POST'])
def predict_lo():
    global otp, username, name, email, number, password
    if request.method == 'POST':
        message = request.form['message']
        print(message)
        if int(message) == otp:
            print("TRUE")
            con = sqlite3.connect('signup.db')
            cur = con.cursor()
            cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
            con.commit()
            con.close()
            return render_template("signin.html")
    return render_template("signup.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("home.html")
    else:
        return render_template("signin.html")



@app.route('/predict',methods=['POST'])
def predict():
    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]
    model = joblib.load('Model/model_Adolescent_norm.sav')
    predict = model.predict(final4)

    if predict==0:
        output='You have no ASD based on the input provide!'
    elif predict==1:
        output='You have ASD, based on the input provide!'

    return render_template('prediction.html', output=output)


@app.route('/predict1',methods=['POST'])
def predict1():
    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]
    model = joblib.load('Model/model_adults_mas.sav')
    predict = model.predict(final4)

    if predict==0:
        output='You have no ASD based on the input provide!'
    elif predict==1:
        output='You have ASD, based on the input provide!'

    return render_template('prediction1.html', output=output)


@app.route('/predict2',methods=['POST'])
def predict2():
    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]
    model = joblib.load('Model/model_child_mas.sav')
    predict = model.predict(final4)

    if predict==0:
        output='You have no ASD based on the input provide!'
    elif predict==1:
        output='You have ASD, based on the input provide!'

    return render_template('prediction2.html', output=output)


@app.route('/predict3',methods=['POST'])
def predict3():
    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]
    model = joblib.load('Model/model_toddler_mas.sav')
    predict = model.predict(final4)

    if predict==0:
        output='You have no ASD based on the input provide!'
    elif predict==1:
        output='You have ASD, based on the input provide!'

    return render_template('prediction3.html', output=output)


@app.route('/home1')
def home1():
	return render_template('home1.html')


@app.route('/home2')
def home2():
	return render_template('home2.html')


@app.route('/home3')
def home3():
	return render_template('home3.html')


@app.route('/home')
def home():
	return render_template('home.html')


@app.route('/notebook1')
def notebook1():
	return render_template('Adolescent.html')


@app.route('/notebook2')
def notebook2():
	return render_template('Adults-Screening.html')


@app.route('/notebook3')
def notebook3():
	return render_template('Childern.html')


@app.route('/notebook4')
def notebook4():
	return render_template('Toddler.html')


if __name__ == "__main__":
    app.run(debug=True)
