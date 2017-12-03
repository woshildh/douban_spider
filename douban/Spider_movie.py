# -*- encoding:utf-8 -*-
'''
defined a class Spider_movie,this class can crawl a type or all types movies' info,including movie_id,movie_name,
actor,director,writer,average_score,country,time_length,show_date and so on.
'''

import download_page
import parse_html
import save_info
import getcookie
import time
import random
import threading

#这个是类别url_dict 以后想要爬取更多种类，可以在里面添加类别
url_dict={"all":[],"romatic":[],"kongbu":[],"xiju":[],"wenyi":[],"oumei":[],"hanguo":[],"jingdian":[]}

#定义锁住url_list初始化的lock1
lock1=threading.Lock()
#定义锁住url_list分配url的lock2
lock2=threading.Lock()

class Spider_movie(threading.Thread):
	'''
	爬取电影信息的类,
	'''
	def __init__(self,thread_name,driver,type):
		self.type=type
		self.thread_name=thread_name
		self.driver=driver
	def create_url_list(self):
		url_list=[]
		try:
			for x in self.type:
				url_list=url_list+url_dict[x]
			print("url_list构造完成...")
		except:
			print("您提供了不存在的类别...")
		else:
			return url_list
	def run(self):
		global url_list
		if lock1.acquire():
			try:
				len(url_list)
			except:
				url_list=self.create_url_list()
			lcok1.release()

		while len(url_lsit)>0:
			if lock2.acquire():
				url=url_list.pop()
