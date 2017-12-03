#这部分用于解析页面

import requests
from bs4 import BeautifulSoup
import download_page
import save_info
import re
import getcookie
import time
import csv
import random
import threading
# douban_movie.csv表结构
#movie_id,movie_name,movie_type,movie_director,movie_bianju,movie_actor,
#movie_country,movie_time,movie_time_length,movie_ave_score,movie_review_count
#,rate5,rate4,rate3,rate2,rate1

#movie_set.csv的路径
movie_set_path="movie_set.csv"

#review_set.csv
review_set_path="review_set.csv"

#定义锁，使得只有一个锁可以访问review_set.py
lock=threading.Lock()

#解析评论页面
def parse_review_html(html_text,movie_id):  #用来解析评论部分的html文本,获取uid,score,review,time
	#print("一个页面开始解析...")
	if html_text=="":
		return 
	dom=BeautifulSoup(html_text,"lxml")

    #获取电影名称
    #movie_name=dom.find_all("title")[0].text.split("。")[0]
	info=[]
	next_url=""
	try:
    	#获取下一个页面的url
		next_url=dom.find("a",{"class":'next'}).get("href")
		#获取所有用户评论的块
		user_span=dom.find_all("div",{"class":"comment-item"})
		for user in user_span:
			son_info=[]
			imgnode=user.find("img") #根据图片提取用户id
			user_id=imgnode.get('src').split("/")[-1].split("-")[0] #提取用户id
			if ".jpg" in user_id:
				continue
			comment=user.find("p").text.strip().replace(",","，").replace("\n","") #提取用户的评论

			try:
				score=user.find("span",{"class":"rating"}).get("title")
				if score=="力荐":
					score="5"
				elif score=="推荐":
					score="4"
				elif score=="还行":
					score="3"
				elif score=="较差":
					score="2"
				else:
					score="1"
			except:
				score="None"

			review_time=user.find("span",{"class":"comment-time"}).get("title") #获取评论的时间
			son_info=[user_id,movie_id,comment,score,review_time]
			info.append(son_info)
	except:
		pass
	#print("一个页面解析成功...")
	return info,next_url

def process_review(movie_id,driver,thread_name):
    count=0
    flag=True
    #获取初始的评论url
    start_url="https://movie.douban.com/subject/"+str(movie_id)+"/comments?status=P"
    #获取初始页面
    html_text=download_page.get_html(start_url,driver)
    review_info,next_url=parse_review_html(html_text,movie_id)
    count=len(review_info)+count
    if len(review_info)==0:
    	flag=False  
    num=save_info.write_review(review_info)
    while flag==True:
    	if count%200==0:
    		time.sleep(random.randint(4,10))
    	elif count>=400:
            break
    	url="https://movie.douban.com/subject/"+str(movie_id)+'/comments'+next_url
    	html_text=download_page.get_html(url,driver)
    	if "还没有人写过短评" in html_text:
    		flag=False
    		break
    	review_info,next_url=parse_review_html(html_text,movie_id)
    	count=len(review_info)+count
    	#if len(review_info)==0:
    	#	print(movie_id,'已经爬完了,共有{}条评论'.format(count))
    	#	flag=False
    	num=save_info.write_review(review_info)
    if lock.acquire():
        with open("review_set.csv",'a',encoding='utf-8',newline="") as file1:
        	writer_obj=csv.writer(file1)
        	writer_obj.writerow([movie_id])
        lock.release()
    print(movie_id,'已经爬完了,共有{}条评论,来自线程{}'.format(count,thread_name))

#这个函数需要返回的是除movie_id,movie_name之外的所有信息
def parse_movie_html(html_text):
    """#这部分是利用dom来进行的解析
    if html_text=="":
        print("这是一个空文本")
        return []
    dom=BeautifulSoup(html_text,"lxml")
    
    info_node=dom.find_all("div",{"id":"info"}) #注意Info_node是一个列表
    #这里nodes包括三个部分：director bianju actors
    nodes=info_node[0].find_all("span",{"class":"attrs"})
    try:
        director=nodes[0].text.replace(" ","")
        bianju=nodes[1].text.replace(" ","")
        actors=nodes[2].text.replace(" ","")
    except:
        print("解析出错...")
        return []
    
    #这里的nodes指的是获取类型部分
    movie_type=[]
    nodes=info_node[0].find_all("span",{"property":"v:genre"})
    for node in nodes:
        movie_type.append(node.text)
    movie_type="/".join(movie_type)
    
    #print(movie_type,director,bianju,actors)
    movie_country=info_node[0].text
    print(len(movie_country))
    """
    #以下是利用正则表达式进行寻找
    if html_text=="":
        print("这是一个空文本...")
        time.sleep(2)
        return []
    try:
        dom=BeautifulSoup(html_text,"lxml")
        info_node=dom.find_all("div",{"id":"info"}) #注意Info_node是一个列表
        info_text=info_node[0].text #信息节点部分的文本
        
        #利用正则表达式获取信息
        director=re.findall(r"导演: (.+?)\n",info_text)[0].replace(" ","")
        bianju=re.findall(r"编剧: (.+?)\n",info_text)[0].replace(" ","")
        actors=re.findall(r"主演: (.+?)\n",info_text)[0].replace(" ","")
        movie_type=re.findall(r"类型: (.+?)\n",info_text)[0].replace(" ","")
        country=re.findall(r"国家/地区: (.+?)\n",info_text)[0].replace(" ","")
        date=re.findall(r"上映日期: (.+?)\n",info_text)[0].replace(" ","")
        time_length=re.findall("片长: (.+?)\n",info_text)[0].replace(" ","")
        
        #获取评分相关信息
        ave_score=dom.find_all("strong",{"class":"ll rating_num","property":"v:average"})[0].text
        vote_num=dom.find_all("span",{"property":"v:votes"})[0].text
        
        #获取从0-5星的比例
        nodes=dom.find_all("span",{"class":"rating_per"})
        rate5=nodes[0].text
        rate4=nodes[1].text
        rate3=nodes[2].text
        rate2=nodes[3].text
        rate1=nodes[4].text
        #将上面的项逐个添加到item中
        item=[movie_type,director,bianju,actors,country,date,time_length,ave_score,vote_num,rate5,rate4,rate3,rate2,rate1]
        return item
    except:
        return []
    
    
#解析电影的页面详细信息  data是20个页面的信息

#data是多个列表的列表,列表项包含['title',url]]
def process_movie_info(data,driver):
    all_movie=[]  #所有电影的信息
    id_set=set()
    chongfu=0
    with open(movie_set_path,'r') as file:
        content=file.read()
        id_set=set(content.split("\n")) #电影的id集合用于去重
        #print(id_set)
        for item in data:
            son_movie=[]  #每部电影的信息
            movie_id=item[1].split("/")[-2]  #电影的id，用于去重
            #print(movie_id)    
            if movie_id in id_set:  #如果这部电影详细已经爬取的话,去重
                chongfu=chongfu+1
            else:
                movie_name=item[0]    #电影的名字
                #把电影的id name加入到son_movie中
                son_movie.append(movie_id)
                son_movie.append(movie_name)    
                html_text=download_page.get_html(item[1],driver) #下载对应的电影页面
                son_movie=son_movie+parse_movie_html(html_text)
                all_movie.append(son_movie)
        print(len(all_movie),"条电影数据非重复...")
        #print(chongfu)
        #print(all_movie)
        #print(len(all_movie))
        #print("正在写入...")
        num=save_info.write_movie(all_movie)
        if num==0:
            time.sleep(1)
        return num
    #print(len(data),"条电影数据存储完毕...\n")
    
if __name__=="__main__":
	driver=getcookie.get_driver()
	process_review(21324900,driver)