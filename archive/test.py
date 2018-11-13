from flask import Flask
from flask import render_template

app = Flask(__name__)

d = { 'a' : 'b', 'c' : 'd'}
a = [ 'e', 'f', 'g', 'h']
@app.route('/')
def hello_world():
	return render_template('show_data.html', geocode=a)
