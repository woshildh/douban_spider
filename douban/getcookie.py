# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 13:47:24 2017

@author: ldh
"""

import time
from selenium import webdriver
import requests

#设置phantomjs.exe的路径
chromedriver_path="C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"

def get_driver(u_name,pw):
    douban_url="https://www.douban.com/"
    password=pw
    user_name=u_name
    
    driver=webdriver.Chrome(executable_path=chromedriver_path)
    
    #获取网页
    driver.get(douban_url)
    print("豆瓣网页获取成功...")
    time.sleep(2)
    cookie1=driver.get_cookies()
    
    #获取用户名框并输入用户名
    try:
        elem_user=driver.find_element_by_xpath('//*[@id="form_email"]')
        elem_user.send_keys(user_name)
        #获取密码框并且输入密码
        elem_pwd=driver.find_element_by_xpath('//*[@id="form_password"]')
        elem_pwd.send_keys(password)

        #勾选记住我
        elem_rem=driver.find_element_by_xpath('//*[@id="form_remember"]')
        elem_rem.click()
        print("*******")
        #考虑验证码图片
        try:
            #获取登录框并且点击提交
            elem_sub=driver.find_element_by_xpath('//*[@id="lzform"]/fieldset/div[3]/input')
            elem_sub.click()
        except:
            #进行验证码识别
            pic=driver.find_element_by_xpath('//*[@id="captcha_image"]')
            img_url=pic.get_attribute("src")
            print(img_url)
            pic_val=input("请输入验证码:")
            print("-----")
            elem_pic=driver.find_element_by_xpath('//*[@id="captcha_field"]')
            elem_pic.send_keys(pic_val)
            print("+++++++")
            #获取登录框并且点击提交
            elem_sub=driver.find_element_by_xpath('//*[@id="lzform"]/fieldset/div[4]/input')
            elem_sub.click()
    except:
        print("寻找登陆信息失败...")
        return []
    cookie2=driver.get_cookies()
    if cookie1==cookie2:
        print("登陆失败，请重新登陆...")
        return ""
    else:
        print("登陆成功...")
    driver.get("https://movie.douban.com/explore#!type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0")
    return driver

#用于把driver解析成cookie
def get_cookie(driver):
    if driver=="":
        return ""
    else:
        cookies=driver.get_cookies() #这是所有cookie的一个列表
        
        #这两行代码很重要,用于构造cookie
        ck=[item['name']+'='+item['value'] for item in cookies]
        ckstr=';'.join(ck)
        return ckstr
    
if __name__=="__main__":
    driver=get_driver()
    cookies=get_cookie(driver)
    headers={
    "User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
     cookies:cookies
    }
    r = requests.get("https://movie.douban.com/subject/26747274/?from=showing",headers=headers)
    print(a.text)
