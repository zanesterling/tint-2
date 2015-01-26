from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
	return 'hello home'

if __name__=='__main__':
	app.run('0.0.0.0', 9000, debug=True)
