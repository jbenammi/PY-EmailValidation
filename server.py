from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
EMAILREGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
app = Flask(__name__)
app.secret_key = "I<3SEcretKeys"
mysql = MySQLConnector(app, 'pyemailvalid')
@app.route('/')
def index():
	return render_template('main.html')

@app.route('/process', methods=['POST'])
def create():
	if not EMAILREGEX.match(request.form['email']):
		notvalid = "notvalid"
		return render_template('main.html', notvalid = notvalid)
	else:
		query = "INSERT INTO emails (email, created_on, updated_on)  VALUES (:email, NOW(), NOW())"
		data = {
				'email': request.form['email'],
				}
		mysql.query_db(query, data)
	session['email'] = request.form['email']
	return redirect('/show_success')

@app.route('/show_success')
def show():
	query = "SELECT * FROM emails"
	emails = mysql.query_db(query)
	print emails
	return render_template('success.html', email_list = emails)

@app.route('/remove/<id>')
def delete_email(id):
	if 'email' in session:
		del session['email']
	query = "DELETE FROM emails WHERE id = :id"
	data = {
			'id': id
			}
	mysql.query_db(query, data)
	return redirect('/show_success')
app.run(debug=True)