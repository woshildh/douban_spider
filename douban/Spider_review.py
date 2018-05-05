import queue
import threading
import parse_html
import time
import getcookie
#声明锁，锁住未访问的集合
lock=threading.Lock()
#声明锁，锁住文件 review_set.csv
f_lock=threading.Lock()
#声明锁获取未访问的集合
lock_get_set=threading.Lock()

class Spider_review(threading.Thread):
	def __init__(self,thread_name,driver):
		threading.Thread.__init__(self)
		self.douban_review_path="douban_review.csv"
		self.review_set_path="review_set.csv"
		self.movie_set_path="movie_set.csv"
		self.thread_name=thread_name
		self.driver=driver
	def run(self):
		global no_visited
		global visited
		if lock_get_set.acquire():
			try:
				len(no_visited)
			except:
				#全局变量只能在这里进行初始化，否则会出错
				no_visited=set()
				visited=set()
				visited,no_visited=self.get_set()
				print("还有{}部电影评论待爬取".format(len(no_visited)))
			lock_get_set.release()

		try:
			while len(no_visited)>0:
				if lock.acquire():
					#print("申请锁成功了...")
					id=no_visited.pop()
					visited.add(id)
					#print("id分配成功了...")
					lock.release()
					#print("锁释放成功了...")
					#print("我是{}".format(self.thread_name))
					parse_html.process_review(id,self.driver,self.thread_name)
		except:
			print("爬取过程出错了...")
		else:
			print("全部OK...")

	#设置两个队列，已经访问的集合，未访问的集合
	def get_set(self):
		#file1、fiile2读取
		file1=open(self.movie_set_path,'r',encoding='utf-8')
		file2=open(self.review_set_path,'r',encoding='utf-8')
		data1=file1.read()
		data2=file2.read()
		
		#temp1、temp2分别表示所有电影的集合、已经访问的电影的集合
		temp1=set(data1.split("\n"))
		temp2=set(data2.split("\n"))
		
		s1=temp2
		s2=temp1-temp2
		file1.close()
		file2.close()
		return s1,s2

def start_main(threadnum,driver_list):
		for i in range(0,threadnum):
			t=Spider_review(i,driver_list[i])
			t.start()
			print("线程{}启动成功".format(i))

if __name__=="__main__":
	#用户名、密码列表，可以自己增加
	user_list=[]
	pw_list=[]
	driver_list=[]
	#构建driver_list列表
	for i in range(0,len(user_list)):
		driver_list.append(getcookie.get_driver(user_list[i],pw_list[i]))
	
	start_main(len(driver_list),driver_list)
