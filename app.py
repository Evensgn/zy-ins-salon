from flask import Flask
from flask import request
from flask import render_template
from flask import abort, redirect, url_for
from defines import *
import time
import query_web
import update_records

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    update_time = '宇宙大爆炸后的第 7 天'
    with open(os.path.join(save_path, 'update_time.text'), 'r', encoding='utf8') as f:
        get_time = float(f.read())
        update_time = time.asctime(time.localtime(get_time))
    return render_template('index.html', wrong_input=False, update_time=update_time)

@app.route('/retry', methods=['GET'])
def retry():
    update_time = '宇宙大爆炸后的第 7 天'
    with open(os.path.join(save_path, 'update_time.text'), 'r', encoding='utf8') as f:
        get_time = float(f.read())
        update_time = time.asctime(time.localtime(get_time))
    return render_template('index.html', wrong_input=True, update_time=update_time)


@app.route('/query', methods=['POST'])
def query():
    stuid = request.form['stuid']
    if not stuid.isdigit():
        return redirect('/retry')
    else:
        report = query_web.query_stuid(stuid)
    return render_template('query.html', report=report)

if __name__ == '__main__':
    update_records.update()
    app.run()