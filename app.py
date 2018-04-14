from defines import *
from flask import Flask
from flask import request
from flask import render_template
from flask import abort, redirect, url_for
import time
import update_records
import os
import csv

app = Flask(__name__)

def app_init():
    update_records.update_text()
    app.stus = update_records.get_map()

def check_update_time():
    update_time = 0.0
    with open(os.path.join(save_path, 'update_time.text'), 'r', encoding='utf8') as f:
        update_time = float(f.read())
    u_time = time.localtime(update_time)
    now_time = time.time()
    n_time = time.localtime(now_time)
    failed = False
    if (u_time.tm_year, u_time.tm_mon, u_time.tm_mday, u_time.tm_hour) != (n_time.tm_year, n_time.tm_mon, n_time.tm_mday, u_time.tm_hour):
        try:
            update_records.update_text()
            app.stus = update_records.get_map()
            u_time = n_time
        except:
            failed = True
    if not failed:
        ret = time_str % (u_time.tm_year, u_time.tm_mon, u_time.tm_mday, u_time.tm_hour, u_time.tm_min, u_time.tm_sec)
    else:
        ret = '一件不太寻常的事情发生了，更新没有正常进行'
    return ret

@app.route('/', methods=['GET'])
def home():
    update_time = check_update_time()
    return render_template('index.html', error_query=False, update_time=update_time)

@app.route('/retry', methods=['GET'])
def retry():
    update_time = check_update_time()
    return render_template('index.html', error_query=True, update_time=update_time)

@app.route('/query', methods=['POST'])
def query():
    stuid = request.form['stuid']
    if stuid not in app.stus:
        return redirect('/retry')
    else:
        report = app.stus[stuid]
        report.stuid = stuid
        report.count_all = report.count_zy + report.count_other
        report.all_ok = report.count_all >= 16
        report.zy_ok = report.count_zy >= 12
        report.has_acts_zy = len(report.acts_zy) > 0
        report.has_acts_other = len(report.acts_other) > 0
        return render_template('query.html', report=report)

if __name__ == '__main__':
    app_init()
    app.run()