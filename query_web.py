from defines import *
import re

def query_stuid(stuid):
	stuid_pattern = re.compile(stuid + '\(\d+\)|' + stuid, re.S)
	multinum_pattern = re.compile('\((\d+)\)', re.S)
	block_pattern = re.compile('<h2.*?>(.*?)</h2>\n\n<p>(.*?)</p>', re.S)
	count = 0
	ret_str = ''
	for record in salon_records:
		page_count = 0
		blocks_info = []
		with open('.//' + save_path + '//' + record[0] + '.text', 'r', encoding = 'utf8') as f:
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
					block_info = '<li>' + block[0]
					if block_count > 1:
						block_info += ' (%d次)' % block_count
					block_info += '<li/>'
					blocks_info.append(block_info)
				page_count += block_count
		if page_count > 0:
			ret_str += record[0] + ':<br/><ul>'
			for block_info in blocks_info:
				ret_str += block_info
			ret_str += '<ul/>'
		count += page_count
	ret_str += '>>> %s 同学参加ZY-INS沙龙共计 %d次<br/>' % (stuid, count)
	return ret_str