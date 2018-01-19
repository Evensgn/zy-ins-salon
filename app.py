from flask import Flask
from flask import request
import query_web

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    #return '<h1>Home</h1>'
    return home_str

@app.route('/query', methods=['POST'])
def signin():
    stuid = request.form['stuid']
    if not stuid.isdigit():
        return '<h3>Oh it is not stuid</h3>'
    return query.query_stuid(stuid)

if __name__ == '__main__':
    with open('index.html', 'r', encoding = 'utf8') as f:
        home_str = f.read()
    app.run()