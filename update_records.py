from defines import *
import requests
import time
import os

def update():
	update_time = time.time()
	failed = False

	if not os.path.exists(save_path):
		os.makedirs(save_path) 

	for record in salon_records:
		with open('.//' + save_path + '//' + record[0] + '.text', 'w', encoding = 'utf8') as f:
			try:
				page_text = requests.get(zy_article_url + str(record[1])).text
				f.write(page_text)
			except:
				failed = True

	if not failed:
		with open('.//' + save_path + '//' + 'update_time.text', 'w', encoding = 'utf8') as f: 
			f.write(str(update_time))