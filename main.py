'''
Author: JYQ
Description: 微博数据 爬取
Date: 2022-04-21 14:52:46
LastEditTime: 2022-04-27 14:46:41
FilePath: \weibo_data\main.py
'''

from json.tool import main
import config
import os
import urllib
import urllib.request
import re
from bs4 import BeautifulSoup


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
        print("get %s failed" % url)
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

def _capture_images(uid,headers, path):
    filter_mode = 1      # 0-all 1-original 2-pictures
    num_pages = 1
    num_blogs = 0
    num_imgs = 0

    # regular expression of imgList and img
    imglist_reg = r'href="(https://weibo.cn/mblog/picAll/.{9}\?rl=2)"'
    imglist_pattern = re.compile(imglist_reg)
    img_reg = r'src="(http://w.{2}\.sinaimg.cn/(.{6,8})/.{32,33}.(jpg|gif))"'
    img_pattern = re.compile(img_reg)
    
    print('start capture picture of weibo_id:' + item_id)
    while True:
        url = 'https://weibo.cn/%s/profile?filter=%s&page=%d' % (uid, filter_mode, num_pages)

        # 1. get html of each page url
        html = _get_html(url, headers)
        
        # 2. parse the html and find all the imgList Url of each page
        soup = BeautifulSoup(html, "html.parser")
        # <div class="c" id="M_G4gb5pY8t"><div>
        blogs = soup.body.find_all(attrs={'id':re.compile(r'^M_')}, recursive=False)
        num_blogs += len(blogs)

        imgurls = []        
        for blog in blogs:
            blog = str(blog)
            imglist_url = imglist_pattern.findall(blog)
            if not imglist_url:
                # 2.1 get img-url from blog that have only one pic
                imgurls += img_pattern.findall(blog)
            else:
                # 2.2 get img-urls from blog that have group pics
                html = _get_html(imglist_url[0], headers)
                imgurls += img_pattern.findall(html)

        if not imgurls:
            print('capture complete!')
            print('captured pages:%d, blogs:%d, imgs:%d' % (num_pages, num_blogs, num_imgs))
            print('directory:' + path)
            break

        # 3. download all the imgs from each imgList
        print('PAGE %d with %d images' % (num_pages, len(imgurls)))
        for img in imgurls:
            imgurl = img[0].replace(img[1], 'large')
            num_imgs += 1
            try:
                urllib.request.urlretrieve(imgurl, '{}/{}.{}'.format(path, num_imgs, img[2]))
                # display the raw url of images
                print('\t%d\t%s' % (num_imgs, imgurl))
            except Exception as e:
                print(str(e))
                print('\t%d\t%s failed' % (num_imgs, imgurl))
        num_pages += 1
        print('')

def _get_one_images(weibo_id,headers,blog,path):
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
    print('start capture picture of weibo id:' + weibo_id)
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
                urllib.request.urlretrieve(imgurl, '{}/{}.{}'.format(path, num_imgs, img[2]))
                # display the raw url of images
                print('\t%d\t%s' % (num_imgs, imgurl))
            except Exception as e:
                print(str(e))
                print('\t%d\t%s failed' % (num_imgs, imgurl))

def _get_one_weibo(weibo_id,headers,blog,path):
    '''
    description: 获取某一条微博的文本内容
    event: 
    param {*}
    return {*}
    '''        
    print('start capture content of weibo id:' + weibo_id)
    weibo_info=blog.next_element.contents[16].contents
    content=blog.next_element.contents[0].contents[0]
    day=weibo_info[0].split(' ')[0]
    time=weibo_info[0].split(' ')[1][:5]
    if '月' in day:
        day="2022-"+day[:2]+"-"+day[3:5]
    print("day:"+day)
    print("time:"+time)
    print("content:"+content)


def _get_blogs(uid,headers,path):
    '''
    description: 获取所有原创微博
    event: 
    param {*}
    return {*}
    '''
    filter_mode=config.filter_type
    num_pages=1
    num_blogs=0
    
    print('start capture all original weibo of uid:' + uid)
    while True:
        url = 'https://weibo.cn/%s/profile?filter=%s&page=%d' % (uid, filter_mode, num_pages)
        html=_get_html(url,headers)

        soup=BeautifulSoup(html,'html.parser')
        blogs = soup.body.find_all(attrs={'id':re.compile(r'^M_')}, recursive=False)
        num_blogs += len(blogs)
           
        for blog in blogs:
            _get_one_weibo(blog.attrs.get('id'),headers,blog,path)
            _get_one_images(blog.attrs.get('id'),headers,blog,path)

if __name__=='__main__':
    uid=config.uid
    path=_get_path(uid)
    cookies=config.cookies
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Cookie': cookies}
    _get_blogs(uid,headers,path)