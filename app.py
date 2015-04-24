from flask import Flask, render_template

import db

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

if __name__=='__main__':
	app.run('0.0.0.0', 9000, debug=True)
