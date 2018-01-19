from defines import *
import requests
import time

local_time = time.asctime(time.localtime(time.time()))

print(local_time)

for record in salon_records:
	with open('./saves/' + record[0] + '.text', 'w', encoding = 'utf8') as f:
		page_text = requests.get(zy_article_url + str(record[1])).text
		f.write(page_text)

