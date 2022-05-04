'''
Author: JYQ
Description: 微博数据 爬取
Date: 2022-04-21 14:52:46
LastEditTime: 2022-05-04 13:48:08
FilePath: \weibo_data\main.py
'''

from json.tool import main
from tokenize import String
import config
import os
import urllib
import urllib.request
import re
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date
import logging

#log
logger=logging.getLogger(config.log_path)


def _get_html(url, headers):
    '''
    description: 
    event:下载html 
    param {*}
    return {*}
    '''    
    try:
        req = urllib.request.Request(url, headers = headers)
        page = urllib.request.urlopen(req)
        html = page.read().decode('UTF-8')
    except Exception as e:
        logger.error("get %s failed" % url)
        return None
    return html

def _get_path(item_id):
    '''
    description: 
    event: 获取图片存储路径
    param {*}
    return {*}
    '''    
    path=os.path.join(config.download_root,item_id)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path

def _get_img_path(item_id,year,month):
    path=os.path.join(config.download_root,year,month,item_id)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def _get_one_images(weibo_id,headers,blog,year,month):
    '''
    description: 爬取某一条微博的图片
    event: 
    param {*}
    return {*}
    '''
    
    num_imgs=0
    imgurls = []     
    # regular expression of imgList and img
    imglist_reg = r'href="(https://weibo.cn/mblog/picAll/.{9}\?rl=2)"'
    imglist_pattern = re.compile(imglist_reg)
    img_reg = r'src="(http://w.{2}\.sinaimg.cn/(.{6,8})/.{32,33}.(jpg|gif))"'
    img_pattern = re.compile(img_reg)
    #print('start capture picture of weibo id:' + weibo_id)
    blog=str(blog)
    imglist_url = imglist_pattern.findall(blog)
    if not imglist_url:
        # 2.1 get img-url from blog that have only one pic
        imgurls += img_pattern.findall(blog)
    else:
        # 2.2 get img-urls from blog that have group pics
        html = _get_html(imglist_url[0], headers)
        imgurls += img_pattern.findall(html)
    for img in imgurls:
            imgurl = img[0].replace(img[1], 'large')
            num_imgs += 1
            try:
                path=_get_img_path(weibo_id,year,month)
                urllib.request.urlretrieve(imgurl, '{}/{}.{}'.format(path, num_imgs, img[2]))
                # display the raw url of images
                #print('\t%d\t%s' % (num_imgs, imgurl))
            except Exception as e:
                logger.error('\t%d\t%s failed' % (num_imgs, imgurl))
                #print('\t%d\t%s failed' % (num_imgs, imgurl))

def _get_one_weibo(weibo_id,headers,blog,path):
    '''
    description: 获取某一条微博的文本内容
    event: 
    param {*}
    return {*}
    '''        
    #print('start capture content of weibo id:' + weibo_id)
    try:
        weibo_list=blog.text.split(' ')
        if "来自" not in weibo_list[-1] :
            weibo_list=weibo_list[:-1]
        content=weibo_list[0]
        if weibo_list[-2][-1] == '日':
            day=weibo_list[-2][-6:]
            day="2022-"+day[:2]+"-"+day[3:5]
        elif weibo_list[-2][-2:] == "今天":
            today=date.today()
            day = today.strftime("%Y-%m-%d")
        

        else:
            day=weibo_list[-2][-10:]
        time=weibo_list[-1][:5]
    except Exception as e:
        logger.warning('failed to get correct weibo which weibo_id:'+ weibo_id)
    
    year=day[:4]
    month=day[5:7]
    #print("day:"+day)
    #print("time:"+time)
    try:
        #print("content:"+content)
        if "转发了" in content:
            content="deleted" #转发微博不存储
    except Exception as e:
        logger.warning('this weibo had been deleted already :'+weibo_id)
        content='deleted'
    return year,month,day,time,content

def _weibo_writer(weibo_df):
    '''
    description: 将内容写进csv
    event: 
    param {*}
    return {*}
    '''    
    weibo_df.to_csv(config.weibo_data_path,index=0)
    print("weibo data writing : done")


def _get_blogs(uid,headers,path):
    '''
    description: 获取当前页面所有原创微博
    event: 
    param {*}
    return {*}
    '''
    weibo_data_list=[]
    filter_mode=config.filter_type
    num_pages=1
    num_blogs=0
    
    print('start capture all original weibo of uid:' + uid)
    while num_pages < 932:
        url = 'https://weibo.cn/%s/profile?page=%d' % (uid, num_pages)
        html=_get_html(url,headers)

        soup=BeautifulSoup(html,'html.parser')
        blogs = soup.body.find_all(attrs={'id':re.compile(r'^M_')}, recursive=False)
        num_blogs += len(blogs)
           
        for blog in blogs:
            id=blog.attrs.get('id')
            year,month,day,time,content=_get_one_weibo(id,headers,blog,path)
            if content == 'deleted':
                continue
            print(day+"-"+time)
            weibo_data_list.append([year,month,day,time,content,id])
            
            _get_one_images(id,headers,blog,year,month)
            
        
        num_pages=num_pages+1
    
    weibo_df=pd.DataFrame(weibo_data_list)
    _weibo_writer(weibo_df)


if __name__=='__main__':
    uid=config.uid
    path=_get_path(uid)
    cookies=config.cookies
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Cookie': cookies}
    _get_blogs(uid,headers,path)