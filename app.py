from flask import Flask
from flask import request
from flask import render_template
import query_web

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def signin():
    stuid = request.form['stuid']
    if not stuid.isdigit():
        return '<h3>Oh it is not stuid</h3>'
    return query_web.query_stuid(stuid)

if __name__ == '__main__':
    app.run()