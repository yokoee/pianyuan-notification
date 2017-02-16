#douban.py

import json
import requests
from bs4 import BeautifulSoup

def get_movie_list():
    with open('config.json', 'r') as f:
        douban = json.load(f)['douban']
    #获取豆瓣'我想看的电影'页面
    payload = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    print('get douban page ...')
    res = requests.get(douban, params=payload)
    print(str(res.status_code) + ' OK!')
    #解析页面得到电影列表
    print('parsing douban page ...')
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.find_all('div', class_='item')
    movie_list = list()
    for i in items:
        tmp = dict()
        href = i.find('div', class_='info').find('a')['href']
        soup_1 = BeautifulSoup(requests.get(href, params=payload).text, 'html.parser')
        tmp['imdb'] = soup_1.find('span', text='IMDb链接:').find_next('a').text
        tmp['name'] = i.find('div', class_='info').find('a').find('em').text
        movie_list.append(tmp)
    print('done!')
    print(movie_list)
    return movie_list

if __name__ == '__main__':
    get_movie_list()
