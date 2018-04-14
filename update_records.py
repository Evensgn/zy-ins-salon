from defines import *
import requests
import time
import os
import csv
import re
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    in_page_body = False
    in_h2 = False
    in_p = False
    get_pre_h2 = False
    lines = []

    def myInit(self):
        self.in_page_body = False
        self.in_h2 = False
        self.in_p = False
        self.get_pre_h2 = False
        self.lines = []

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and attrs == [('class', 'page-body')]:
            self.in_page_body = True
        if not self.in_page_body:
            return
        if tag == 'h2':
            self.in_h2 = True
            self.get_pre_h2 = True
        elif tag == 'p':
            self.in_p = True 

    def handle_endtag(self, tag):
        if not self.in_page_body:
            return
        if tag == 'div':
            self.in_page_body = False
        elif tag == 'h2':
            self.in_h2 = False
        elif tag == 'p':
            self.in_p = False

    def handle_data(self, data):
        if not self.in_page_body:
            return
        if self.in_h2:
            if data == '注意':
                self.get_pre_h2 = False
            else:
                self.lines.append(data)
        elif self.get_pre_h2 and self.in_p:
            self.lines.append(data)
            self.get_pre_h2 = False

def process_html(name, html):
    parser = MyHTMLParser()
    parser.myInit()
    parser.feed(html)
    out_file = os.path.join(save_path, salon_record_file % (name))
    with open(out_file, 'w', encoding='utf8') as f:
        f.write('\n'.join(parser.lines))

def update_text():
    update_time = time.time()
    failed = False

    if not os.path.exists(save_path):
        os.makedirs(save_path) 

    for record in salon_records:
        try:
            html = requests.get(zy_article_url + record[1]).text
            process_html(record[0], html)
        except:
            failed = True

    if not failed:
        out_file = os.path.join(save_path, update_time_file)
        with open(out_file, 'w', encoding='utf8') as f: 
            f.write(str(update_time))

def get_map():
    sid_data = {}
    salons = {}
    sid_list_pattern = r'(\d+(\(\d+\))?、)*\d+(\(\d+\))?'
    sid_set = set()

    names = [x[0] for x in salon_records]
    for name in names:
        in_file = os.path.join(save_path, salon_record_file % (name))
        sid_data[name] = []
        salons[name] = []
        with open(in_file, 'r', encoding='utf8') as f:
            for line in f.readlines():
                s = line.replace(' ', '').replace('\n', '')

                if re.fullmatch(sid_list_pattern, s):
                    sid_list = s.split('、')
                    sid_data_now = []
                    for sid in sid_list:
                        sid_now = ''
                        count_now = 0
                        if '(' in sid:
                            sid_now = sid.split('(')[0]
                            count_now = int(sid.split('(')[1].replace(')', ''))
                        else:
                            sid_now = sid
                            count_now = 1
                        for i in range(count_now):
                            sid_data_now.append(sid_now)
                        if sid_now not in sid_set:
                            sid_set.add(sid_now)
                    sid_data[name].append(sid_data_now)

                elif line.strip('\n').strip(' ') != '':
                    title = line.strip('\n').strip(' ')
                    salons[name].append(title)

    stus = {}
    for sid in sid_set:            
        stu = UniObject()
        stu.count_zy = 0
        stu.count_other = 0
        stu.acts_zy = []
        stu.acts_other = []
        for name in names:
            for i in range(len(salons[name])):
                num = sid_data[name][i].count(sid)
                if num == 0:
                    continue
                if name not in other_set: 
                    stu.acts_zy.append((salons[name][i], num))
                    stu.count_zy += num
                else:
                    stu.acts_other.append((salons[name][i], num))
                    stu.count_other += num
        stus[sid] = stu
    return stus