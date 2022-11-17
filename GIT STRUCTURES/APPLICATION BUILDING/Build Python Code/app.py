import flask_sqlalchemy
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, url_for
import joblib

app = Flask(__name__)

@app.route('/')

def home():
	return render_template('index.html')

@app.route('/predict/')

def predict():
	return render_template('Loan_Prediction.html')

@app.route('/prediction', methods = ['POST'])
def prediction():
	if request.method == 'POST':
		gender = request.form['gender']
		married = request.form['status']
		dependat =request.form['dependants']
		education = request.form['education']
		employ = request.form['employ']
		annual_income = request.form['aincome']
		co_income = request.form['coincome']
		Loan_amount = request.form['Lamount']
		Loan_amount_term = request.form['Lamount_term']
		credit = request.form['credit']
		proper = request.form['property_area']

	gender = gender.lower()
	married= married.lower()
	education = education.lower()
	employ = employ.lower()
	proper = proper.lower()
	error = 0
	if(employ=='yes'):
		employ = 1
	else:
		employ = 0
	if(gender=='male'):
		gender = 1
	else:
		gender = 0
	if (married=='married'):
		married=1
	else:
		married=0
	if (proper=='rural'):
		proper=0
	elif (proper=='semiurban'):
		proper=1
	else:
		proper=2
	if (education=='graduate'):
		education=0
	else:
		education=1
	try:
		dependat = int(dependat)
		annual_income = int(annual_income)
		co_income = int(co_income)
		Loan_amount = int(Loan_amount)
		Loan_amount_term = int(Loan_amount_term)
		credit = int(credit)
		x_app = np.array([[gender, married, dependat,education,employ,annual_income,co_income,Loan_amount,Loan_amount_term,credit,proper]])
		model = joblib.load('Forest.pkl')
		ans = model.predict(x_app)
		if (ans==0):
			print("We sad to inform that you are not eligible for this loan")
			return render_template('result2.html', prediction=ans)
		else:
			print("Congratulations you are eligble for this Loan")
			return render_template('result1.html')	
	except ValueError:
		return render_template('error.html')
	

if __name__ == '__main__':
	app.run(debug=True)