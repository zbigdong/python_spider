'''
设置变量 <  imgoutpath  > 为文件保存路径
控制 初始化函数 成员变量  <  i  > 完成每次爬取的步长
<    timeout   > 设置超时时间为 5s  如果5s 请求超时 则跳过本请求继续请求
每次请求回来的连接为600 但是实际得到的图片大概在200 这样，够我目前的需求
'''
__author__ = 'Administrator'

import requests
import os
import re
import time
class image_get(object):


    def __init__(self,word):#初始化
        self.word = word
        #self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'}#添反爬加请求头防止
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}#添反爬加请求头防止
        self.start_url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%s&pn={}&gsm=3c&ct=&ic=0&lm=-1&width=0&height=0'%word#网页初始页
        self.start_url_list = []#创建一个网页的列表
        #for i in range(10):#循环遍历
        i = 0;
        while i < 10:
            url = self.start_url.format(i*20)#使上面的url进行字符串格式化
            self.start_url_list.append(url)#把获取到的url添加到列表里面
            i = i+1
        #print(self.start_url_list)#打印列表

    def get_content(self,url):
        #print(url)
        html = requests.get(url,headers=self.headers)#进行网络请求
        #print(html.text)#打印网页源代码
        img_list = re.findall('"objURL":"(.*?)",',html.text)#使用正则匹配图片
        return img_list#返回图片列表

    def save(self,start_url_list):#保存函数
        num = 0
        for pic_url in start_url_list:#进行循环
            num += 1
            print('已保存'+str(num)+'张')#打印循环后的结果
            end = re.search('(.jpg|.jpeg|.png)$',pic_url)#添加一个名为end的变量名，搜索picurl里的东西
            if end == None:#进行if判断，如果等于无
                pic_url = pic_url + '.jpg'#则添加后缀.jpg
            try:#进行错误测试
               #with open('./' + self.word + '/{}'.format(pic_url[-10:]), 'ab') as f:#使用with方法保存，+ 输入的文字 + 格式化picurl里面的图片名字防止重名
                with open(imgoutpath + self.word + '/{}'.format(pic_url[-10:]), 'ab') as f:#使用with方法保存，+ 输入的文字 + 格式化picurl里面的图片名字防止重名
                    try:
                        pic = requests.get(pic_url,headers=self.headers,timeout=5)#进行网络请求，添加请求头，超过一秒则切换下一个
                        f.write(pic.content)#写入图片
                    except Exception:
                        pass
            except Exception:
                pass



    def run(self):
        for url in self.start_url_list:
            start_url_list = self.get_content(url)
            self.save(start_url_list)

if __name__ == '__main__':
    imgoutpath = r'C:\Users\30278\Desktop\Py_img'
    word = input('请输入需要的图片：')
    os.mkdir(imgoutpath + word)
    tupian = image_get(word)
    tupian.run()

