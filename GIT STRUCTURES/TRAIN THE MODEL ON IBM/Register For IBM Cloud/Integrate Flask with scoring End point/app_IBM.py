from flask import Flask, render_template,url_for, request
import joblib
import numpy as np
import requests

API_KEY = "oXmPtryJbc9JVlM06u3yjFW8vNjxcTot4wbwLNZZUfi7"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

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
		features = [[gender,married,dependat,education,employ,annual_income,co_income,Loan_amount,Loan_amount_term,credit,proper]]
		con_features = [np.array(features)]
		payload_scoring = {"input_data": [{"fields": ['gender','married','depend','education','self_emp','applicant_income','co_income','loan_amount','loan_term','credit_history','property_area'], "values":features}]}
		response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/37be7c5e-9cef-4a81-bf34-cf607fbbc9a9/predictions?version=2022-11-18', json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
		print("response_scoring")
		prediction = response_scoring.json()
		predict = prediction['prediction'][0]['values'][0][0]

		if (predict==1):
			print("Congratulations your eligble for this Loan")
		else:
			print("We sad to inform that your request has not been accepted")
		return render_template('submit.html', prediction=predict)
	except ValueError:
		return render_template('error.html', prediction=1)
	

if __name__ == '__main__':
	app.run(debug=True)