from defines import *
import re

stuid = 'wow'
input_once = False
while not stuid.isdigit():
	if input_once:
		stuid = input('输入有误，请重新输入学号: ')
	else:
		stuid = input('请输入查询的学号: ')
	input_once = True

stuid_pattern = re.compile(stuid + '\(\d+\)|' + stuid, re.S)
multinum_pattern = re.compile('\((\d+)\)', re.S)
block_pattern = re.compile('<h2.*?>(.*?)</h2>\n\n<p>(.*?)</p>', re.S)

count = 0
for record in salon_records:
	page_count = 0
	blocks_info = []
	with open('./saves/' + record[0] + '.text', 'r', encoding = 'utf8') as f:
		page_text = f.read()
		blocks = re.findall(block_pattern, page_text)
		for block in blocks:
			items = re.findall(stuid_pattern, block[1])
			block_count = 0
			if len(items) > 0:
				for item in items:
					multinums = re.findall(multinum_pattern, item)
					if len(multinums) > 0:
						block_count += int(multinums[0])
					else:
						block_count += 1
			if block_count > 0:
				block_info = '- ' + block[0]
				if block_count > 1:
					block_info += ' \033[31m(%d次)\033[0m' % block_count
				blocks_info.append(block_info)
			page_count += block_count
	if page_count > 0:
		print('\033[32m' + record[0] + ':\033[0m')
		for block_info in blocks_info:
			print(block_info)
	count += page_count

print('>>> \033[33m%s\033[0m 同学参加ZY-INS沙龙共计 \033[33m%d次\033[0m' % (stuid, count))
