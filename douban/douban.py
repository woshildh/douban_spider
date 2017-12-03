# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 13:18:52 2017

@author: ldh
"""

from bs4 import BeautifulSoup
import requests
import csv
import re
import download_page
import parse_html
import save_info
import getcookie
import time
import random
import threading
#这个主函数用于下载电影的相关信息
#爱情类(完)、热门（）、最新()、豆瓣高分(完)、喜剧类(完)、科幻(完)、悬疑（完）、恐怖(完)、动画(完)、冷门佳片(完)、华语(完)、欧美(完)
#韩国（完）、日本（完）、动作(完)、治愈()、可播放()、经典类()、
#quanbu(12000截至)
#count_movie=0
#count_review_movie=0 #用来标记已经爬取的电影评论的总数

def main_movie(cishu): #次数表示下载多少次，每次可以下载20条
    #分别表示剧情、传记、悬疑、音乐、励志、文艺
    quanbu=["https://movie.douban.com/j/new_search_subjects?sort=R&range=0,10&tags=%E7%94%B5%E5%BD%B1,%E5%89%A7%E6%83%85",
    "https://movie.douban.com/j/new_search_subjects?sort=R&range=0,10&tags=%E7%94%B5%E5%BD%B1,%E4%BC%A0%E8%AE%B0",
    "https://movie.douban.com/j/new_search_subjects?sort=R&range=0,10&tags=%E7%94%B5%E5%BD%B1,%E6%82%AC%E7%96%91",
    "https://movie.douban.com/j/new_search_subjects?sort=R&range=0,10&tags=%E7%94%B5%E5%BD%B1,%E9%9F%B3%E4%B9%90",
    "https://movie.douban.com/j/new_search_subjects?sort=R&range=0,10&tags=%E7%94%B5%E5%BD%B1,%E5%8A%B1%E5%BF%97",
    "https://movie.douban.com/j/new_search_subjects?sort=R&range=0,10&tags=%E7%94%B5%E5%BD%B1,%E6%96%87%E8%89%BA"]
    biglist=quanbu
    driver=getcookie.get_driver()
    cookies=getcookie.get_cookie(driver)
    if cookies=="":
        print("cookie解析失败")
        return -1
    else:
        print("cookie解析成功")
        time.sleep(5)
    count_movie=20 #这里是定义已经爬取的电影的总数目
    for request_root_url in biglist:
        x=0  #用来标记已经爬取的电影的次数
        #request_root_url="https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%81%90%E6%80%96&sort=rank&page_limit=20"
        text=download_page.get_json2(request_root_url,0,cookies)
        print(text[:20])
        print("---------------------------")
        text=download_page.get_json2(request_root_url,20,cookies)
        print(text[:20])
        print("---------------------------")
        try:
            while x<cishu:
            	if x%10==0:  #随机间隔一段时间
            		time.sleep(random.random()*20)
            	elif x%51==0:
            		time.sleep(30)
            		print("已经成功爬取了51次")
            	page_start=count_movie
                #json_text=download_page.get_json(request_root_url,page_start,cookies)  #这部分是获取json列表
                #print(json_text)
            	json_text=download_page.get_json2(request_root_url,page_start,cookies)
            	json_text=str(json_text)
                #print(json_text)
            	movie_data=download_page.deal_json2(json_text)
            	if movie_data!=[]:
                    print(len(movie_data),"条json数据获得了url和name")
            	else:
            		print("没有获得json数据")
            		break
                #print(movie_data)
                #return 
            	num=parse_html.process_movie_info(movie_data,driver)
            	count_movie=count_movie+20
            	x=x+1
            	print(x)
        except:
            return count_movie  
    return count_movie

def main_review():
    douban_review_path="douban_review.csv"
    
    review_set_path="review_set.csv"
    movie_set_path="movie_set.csv"

    #获取需要爬取评论的电影id列表
    file1=open(movie_set_path,'r',encoding='utf-8')
    file2=open(review_set_path,'r',encoding='utf-8')
    set1=set((file1.read()).split("\n"))
    set2=set((file2.read()).split("\n"))
    id_list=set1-set2

    #模拟登陆,获取cookie
    driver=getcookie.get_driver()
    cookie=getcookie.get_cookie(driver)
    #根据id_list去解析评论
    count=0
    for id in id_list:
    	count+=1
    	if count%20==0:
    		time.sleep(30)
    	parse_html.process_review(id,driver,-1)
    	#id_list.remove(id)
    print("{}部电影评论下载完毕".format(count))



if __name__=="__main__":
    
    #爬取电影评论
    num=main_review()
    print(num)
    #爬取电影信息
    #count_movie=main_movie(500)
    #print(count_movie)

    #进行测试
    #json_text=download_page.get_json("https://movie.douban.com/j/search_subjects?type=movie&tag=%E8%B1%86%E7%93%A3%E9%AB%98%E5%88%86&sort=time&page_limit=20",0)
    #data=download_page.deal_json(json_text)
    #parse_html.process_movie_info(data)
    #print(data)
