#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
class tproc():
	def __init__(self):
		self.kwmap=[{'key':["吉高平"],'retext':["吉高平最帅",
										"吉高平最聪明",
										"吉高平最牛逼",
										"吉高平比你们不知道高明到哪里去了",
										"咱们说说别的人吧",
										"砸你家玻璃",
										"呵！呵！呵！呵！呵！"]},
				{"key":["傻逼"],'retext':["骂人不是好孩子！",
										"我不想和你说话啦",
										"你是个没有素质的人",
										"还是吉高平牛逼一些",
										"略略略"]},
				{"key":["草","艹"],'retext':["卧槽？？",
										"草",
										"你个辣鸡",
										"你读过书么",
										"出口成脏啊"]},
				{"key":["谭新培","新培","txp","TXP"],'retext':["不要和提这个傻逼",
										"哈哈哈哈，真是太好笑了",
										"啧啧啧，没想到你居然骂脏话",
										"还是吉高平牛逼一些",
										"这货还不如熊若阳！！！",
										"谭啥？老坛酸菜？？",
										"我知道他没有女朋友"]}]
	def proc(self,str):
		for key in self.kwmap:
			for kw in key['key']:
				if str.find(kw)>-1:
					l=len(key['retext'])
					print l
					pos=random.randint(0,l-1)
					return key['retext'][pos]
		return str
if __name__ == '__main__':
	tp=tproc()
	print tp.proc('吉高平尼玛')
		