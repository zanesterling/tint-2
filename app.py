#!/usr/local/bin/python
from flask import Flask, render_template, redirect, url_for, flash, \
	session, request
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
	if 'usern' not in session:
		return render_template('home.html')
	user = db.getUser(usern=session['usern'])
	if not user:
		session.pop('usern', None)
		return render_template('home.html')

	d = {}
	d['usern'] = session['usern']
	d['repos'] = github.get('user/repos')
	return render_template('dashboard.html', d=d)

@app.route('/login')
def login():
	# if the user is already logged in, send them away
	if 'usern' in session:
		return redirect(url_for('home'))

	# forward to github's oauth system
	return github.authorize()

@app.route('/logout')
def logout():
	session.pop('usern', None)
	flash('You were logged out')
	return redirect(url_for('home'))

@app.route('/github-callback')
@github.authorized_handler
def gh_callback(oauth_token):
	# ensure we got the token
	if oauth_token is None:
		flash('There was an issue logging in')
		log('err: login error')
		return redirect(url_for('home'))

	# if the user is new register them with the db
	if not db.hasUser(oauth_token):
		db.addUser(oauth_token)
	usern = db.getUser(oauth_token)['usern']

	# give them a cookie (or refresh theirs) that says logged-in
	session['usern'] = usern

	# send them to the dashboard
	flash('You were logged in')
	return redirect(url_for('home'))

@app.route('/action', methods=['POST'])
def action():
	if 'usern' not in session:
		return 'err: you aren\'t authorized'

	data = request.form
	if not data:
		return 'err: bad data'
	if 'action' not in data:
		return 'err: action not recognized'

	if data['action'] == 'toggle-repo':
		user = db.getUser(usern=session['usern'])
		if data['repo'] in user['tinted-repos']:
			user['tinted-repos'].remove(data['repo'])
		else:
			user['tinted-repos'].append(data['repo'])
		db.overwriteUser(user)
		return 'success'

	return 'err: action not recognized'

# TODO add proper error logging
def log(logstr):
	print logstr

@github.access_token_getter
def token_getter():
	if 'usern' in session:
		return db.getUser(usern=session['usern'])['token']

if __name__=='__main__':
	app.run('0.0.0.0', 9000, debug=True)
