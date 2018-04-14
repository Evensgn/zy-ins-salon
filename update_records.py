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
		with open(os.path.join(save_path, salon_record_file % (record[1])), 'w', encoding='utf8') as f:
			try:
				page_text = requests.get(zy_article_url + record[1]).text
				f.write(page_text)
			except:
				failed = True

	if not failed:
		with open(os.path.join(save_path, update_time_file), 'w', encoding='utf8') as f: 
			f.write(str(update_time))