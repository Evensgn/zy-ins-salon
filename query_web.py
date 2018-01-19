from defines import *
import re

class Report(object):
	pass

class Page(object):
	pass

class Block(object):
	pass

def query_stuid(stuid):
	ret = Report()
	ret.stuid = stuid
	stuid_pattern = re.compile(stuid + '\(\d+\)|' + stuid, re.S)
	multinum_pattern = re.compile('\((\d+)\)', re.S)
	block_pattern = re.compile('<h2.*?>(.*?)</h2>\n\n<p>(.*?)</p>', re.S)
	ret.count = 0
	ret.pages = []
	for record in salon_records:
		page_ = Page()
		page_.title = record[0]	
		page_.count = 0
		page_.blocks = []
		with open('.//' + save_path + '//' + record[0] + '.text', 'r', encoding = 'utf8') as f:
			page_text = f.read()
			blocks = re.findall(block_pattern, page_text)
			for block in blocks:
				block_ = Block()
				block_.title = block[0]
				block_.count = 0
				items = re.findall(stuid_pattern, block[1])
				if len(items) > 0:
					for item in items:
						multinums = re.findall(multinum_pattern, item)
						if len(multinums) > 0:
							block_.count += int(multinums[0])
						else:
							block_.count += 1
				if block_.count > 0:
					block_.multiple = block_.count > 1
					page_.blocks.append(block_)
				page_.count += block_.count
		if page_.count > 0:
			ret.pages.append(page_)
		ret.count += page_.count
	return ret