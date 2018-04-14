from defines import *
from flask import Flask
from flask import request
from flask import render_template
from flask import abort, redirect, url_for
import time
import query_web
import update_records
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    update_time = 'Error: not '
    with open(os.path.join(save_path, 'update_time.text'), 'r', encoding='utf8') as f:
        get_time = float(f.read())
        update_time = time.asctime(time.localtime(get_time))
    return render_template('index.html', error_query=False, update_time=update_time)

@app.route('/retry', methods=['GET'])
def retry():
    update_time = '宇宙大爆炸后的第 7 天'
    with open(os.path.join(save_path, 'update_time.text'), 'r', encoding='utf8') as f:
        get_time = float(f.read())
        update_time = time.asctime(time.localtime(get_time))
    return render_template('index.html', error_query=True, update_time=update_time)

@app.route('/query', methods=['POST'])
def query():
    stuid = request.form['stuid']
    if stuid not in stu_info:
        return redirect('/retry')
    else:
        report = query_web.query_stuid(stuid)
    return render_template('query.html', report=report)

stu_info = {}
def app_init():
    update_records.update()
    with open(stu_info_file, 'r', encoding='utf8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stu_now = {'name': row['name'], 'grade': row['grade']}
            stu_info['id'] = stu_now

if __name__ == '__main__':
    app_init()
    app.run()