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
		page = Page()
		page.title = record[0]	
		page.count = 0
		page.blocks = []
		with open('.//' + save_path + '//' + record[0] + '.text', 'r', encoding = 'utf8') as f:
			page_text = f.read()
			blocks = re.findall(block_pattern, page_text)
			for block in blocks:
				block = Block()
				block.title = block[0]
				block.count = 0
				items = re.findall(stuid_pattern, block[1])
				if len(items) > 0:
					for item in items:
						multinums = re.findall(multinum_pattern, item)
						if len(multinums) > 0:
							block.count += int(multinums[0])
						else:
							block.count += 1
				if block.count > 0:
					block.multiple = block.count > 1
					page.blocks.append(block)
				page.count += block.count
		if page.count > 0:
			ret.pages.append(page)
		ret.count += page.count
	return ret