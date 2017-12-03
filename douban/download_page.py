import requests
from bs4 import BeautifulSoup
import json
import csv
import getcookie
import random
import time
from selenium import webdriver
#这部分用于下载页面和请求json部分

def get_html(url,driver):
    #用driver访问页面
    time.sleep(0.5)
    driver.get(url)
    #print("一个页面获取成功...")
    return driver.page_source
    '''
    try:
        num=random.randint(0,100)
        if num%67==0:
            time.sleep(5)
        agents=["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
            ]
        headers={"User-Agent":agents[random.randint(0,100)%4], #随机选择一个agent        
                "Host": "movie.douban.com",
                "Accept-Language": "zh-Hans-CN, zh-Hans; q=0.8, en-US; q=0.5, en; q=0.3",
                "Accept-Encoding":'gzip, deflate, br',
                "Cookie":cookies,
                "Connection":"keep-alive"
        }
        r=requests.get(url,headers)
        r.raise_for_status()
        #print(r.text[100])
        return r.text
    except:
        return 
    '''
    
#每次返回20条电影的json列表
def get_json(request_root_url,page_start,cookies): #request_root_url指的是初始的url，page_start为每次请求的数据的起始位置
    agents=["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
            ]
    headers={"User-Agent":agents[random.randint(0,100)%4], #随机选择一个agent        
                "Host": "movie.douban.com",
                "Accept-Language": "zh-Hans-CN, zh-Hans; q=0.8, en-US; q=0.5, en; q=0.3",
                "Accept-Encoding":'gzip, deflate, br',
                "Cookie":cookies,
                "Connection":"keep-alive"
        }
    #下面的request_root_url需要根据电影的类型进行修改
    #request_root_url="https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%BB%8F%E5%85%B8&sort=recommend&page_limit=20&page_start=20"
    request_url=request_root_url+"&start="+str(page_start)
    data=requests.get(request_url,headers=headers)
    data.raise_for_status()
    #page_start=page_start+20
    return data.text     #必须是返回data.text，data是一个<response>对象

#此处的data是20部电影的json列表
def deal_json(data):
    if data=="":
        print("这是一个空的json...")
        return []
    data=str(data)
    data=json.loads(data)
    movie_info_list=data["subjects"]
    movie=[]  #这是将要返回的数据，包括 [电影名字,url]
    for item in movie_info_list:
        x=[]
        x.append(item["title"])
        x.append(item["url"])
        movie.append(x)
    return movie

#这部分是从全部电影的页面那里请求json
def get_json2(request_root_path,start,cookies):
	#request_root_path="https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1"
	headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",        
             "Host": "movie.douban.com",
             "Accept-Language": "zh-Hans-CN, zh-Hans; q=0.8, en-US; q=0.5, en; q=0.3",
             "Accept-Encoding":'gzip, deflate, br',
             "Cookie":cookies,
             "Connection":"keep-alive"
    }
	request_url=request_root_path+"&start="+str(start)
	data=requests.get(request_url,headers=headers)
	data.raise_for_status()
	return data.text
#处理json
def deal_json2(data):
    if data=="":
        print("这是一个空的json...")
        return []
    data=str(data)
    data=json.loads(data)
    movie_info_list=data["data"]
    movie=[]  #这是将要返回的数据，包括 [电影名字,url]
    for item in movie_info_list:
        x=[]
        x.append(item["title"])
        x.append(item["url"])
        movie.append(x)
    return movie

if __name__=="__main__":
    driver=getcookie.get_driver()
    print(driver.page_source)
    '''
   driver=getcookie.get_driver()
   cookies=getcookie.get_cookie(driver)
   json_text=get_json("https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%88%B1%E6%83%85&sort=recommend&page_limit=20",260,cookies)
	print(json_text)
   '''