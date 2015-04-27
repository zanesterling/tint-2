from flask import Flask, render_template, redirect, url_for, flash, \
	session
from flask.ext.github import GitHub

import db
import secrets

app = Flask(__name__)
app.config['GITHUB_CLIENT_ID'] = secrets.CLIENT_ID
app.config['GITHUB_CLIENT_SECRET'] = secrets.CLIENT_SECRET
app.secret_key = secrets.FLASK_SECRET

github = GitHub(app)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/login')
def login():
	# if the user is already logged in, send them away
	if 'username' in session:
		return redirect(url_for('home'))

	# forward to github's oauth system
	return github.authorize()

@app.route('/github-callback')
@github.authorized_handler
def gh_callback(oauth_token):
	# ensure we got the token
	if oauth_token is None:
		flash('There was an issue logging in')
		log('err: login error')
		return redirect(url_for('home'))

	# if the user is new register them with the db
	usern = db.hasUser(oauth_token)
	if not usern:
		usern = db.addUser(oauth_token)

	# give them a cookie (or refresh theirs) that says logged-in
	session['username'] = usern

	# send them to the dashboard
	flash('You were logged in')
	return redirect(url_for('home'))

# TODO add proper error logging
def log(logstr):
	print logstr

if __name__=='__main__':
	app.run('0.0.0.0', 9000, debug=True)
