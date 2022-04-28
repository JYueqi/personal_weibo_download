'''
Author: JYQ
Description: 
Date: 2022-04-26 12:29:03
LastEditTime: 2022-04-28 16:46:37
FilePath: \weibo_data\config.py
'''
#22/4/28: 暂时不会自动获取cookies
#weibo.com是新版界面，不好爬取，应该用weibo.cn
#个人微博图片分为两类：1）静态普通图片jpeg；2）IOS livephoto: quicktime movie;3)动图 MP4 movie

url='https://weibo.com/u/2932972560'
uid='2932972560'

filter_type=1
'''
filter=0 全部微博（包含纯文本微博，转载微博）
filter=1 原创微博（包含纯文本微博）
filter=2 图片微博（必须含有图片，包含转载）
'''
cookies='_T_WM=9f7a2fcfa8360bc1acb8305755ed76e4; SCF=ArviQe0oBxCtBsjh3hb6eF9fOg6SvDn20XIFI5vaVT-e-RAPKm9d5jg74qAjp0gZ19Jqeb2_o49hkRXvF4jh76E.; SUB=_2A25PYwciDeRhGeRH6FAY9yzJzTyIHXVsr6lqrDV6PUJbktCOLUPYkW1NTcgX0DQvzK9y-EWmLCZtiHRmz4HV6FA5; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWGfCoX81c9R7fyaAhsky8Z5NHD95QE1KeE1KMESKq7Ws4Dqc_Ii--fiKy8i-iFi--Ri-isiKnNi--RiK.4iKy8i--ciK.ciK.pi--ci-z4i-i8i--NiKLWiKnXi--Ri-isi-zNi--Xi-iWi-iWi--fiKnNi-2Xi--NiKnRi-8W; SSOLoginState=1650947955'

download_root='E:/jyq/projects/weibo_data/download'

weibo_data_path='E:\\jyq\\projects\\weibo_data\\mrfz_weibo_data.csv'