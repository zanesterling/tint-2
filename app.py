from flask import Flask, render_template, redirect, url_for, flash
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
	return github.authorize()

@app.route('/github-callback')
@github.authorized_handler
def gh_callback(oauth_token):
	flash('You were logged in')
	return redirect(url_for('home'))

if __name__=='__main__':
	app.run('0.0.0.0', 9000, debug=True)
