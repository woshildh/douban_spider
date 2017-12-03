# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 15:07:06 2017

@author: ldh
"""
# douban_movie.csv表结构
#movie_id,movie_name,movie_type,movie_director,movie_bianju,movie_actor,movie_country,movie_year,movie_time_length,movie_ave_score,movie_review_count

import csv
import json
import threading
#douban_movie.csv的路径
movie_path="douban_movie.csv"

#douban_review.csv的路径
review_path="douban_review.csv"

#movie_set.csv的路径
movie_set_path="movie_set.csv"

#review_set.csv
review_set_path="review_set.csv"

#定义锁，使得只有一个线程可以访问douban_review.csv
lock=threading.Lock()

#向douban_movie.csv中写数据
def write_movie(data):
    print("正在写入...")
    num=0
    with open(movie_path,'a',encoding="utf-8",newline="") as file1: #必须用'a'模式打开
        writer_movie=csv.writer(file1)  #创建写对象
        for row_data in data:
            #print("----")
            #print(row_data)
            writer_movie.writerow(row_data)
            #print(row_data)
            num=num+1
            movie_id=row_data[0]
            with open(movie_set_path,'a',encoding="utf-8",newline="") as file2:
                writer=csv.writer(file2)
                writer.writerow([movie_id])
    print("共有{}条数据处理完毕\n".format(num))
    return num

#向douban_review.csv中写数据
#douban_review.csv表结构  uid,movie_id,score,review,time  

def write_review(data):
    num=0
    if lock.acquire():
        with open(review_path,'a',newline="",encoding="utf-8") as file1: #必须用'a'模式打开
            writer_obj=csv.writer(file1)  #创建写对象
            for row_data in data:
                writer_obj.writerow(row_data)
                num=num+1
        lock.release()
    return num

if __name__=="__main__":
    data=['26926452', '虚拟革命', '科幻/犯罪', '盖-罗杰·杜维尔', '盖-罗杰·杜维尔', '麦克·多普德/简·巴德勒/JochenHägele/马克西米安·鲍林/KayaBlocksage/PetraSilander/NicolasVanBeveren/ElieHaddad/艾米里.德.法尔科/EricKailey/ZoeCorraface/MelissaMars', '美国/法国', '2016-05-11(戛纳电影节)/2016-10-12(法国)', '92分钟', '5.2', '336', '4.5%', '10.5%', '37.2%', '34.4%', '13.4%']
    row_data=[]
    row_data.append(data)
    write_movie(row_data)
 