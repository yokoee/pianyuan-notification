#pianyuan.py

import time

import requests
from bs4 import BeautifulSoup


def get_resources(imdb,name):
    search_url = 'http://pianyuan.net/search?q='
    soup = BeautifulSoup(requests.get(search_url+ imdb).text, 'html.parser')
    print('开始查找 '+ name + '(' + imdb+ ') ...')

    if soup.get_text().find('找不到相关资源') != -1:
        print('找不到资源')
        return False

    movie_page = 'http://pianyuan.net' + soup.find('div', class_='litpic').a['href']
    soup = BeautifulSoup(requests.get(movie_page).text, 'html.parser')
    tables = soup.find('span', text='全部资源').find_all_next('table')
    movie_resources = list()
    for table in tables:
        tmp = dict()
        resource_pages = list()
        for i in table.find_all('td', class_='nobr'):
            if i.a:
                resource_pages.append(i.a['href'])
        for i in resource_pages:
            soup_r = BeautifulSoup(requests.get('http://pianyuan.net' + i).text, 'html.parser')
            #资源下载链接
            tmp['link'] = soup_r.find('div', class_='tdown').a.find_next('a')['href']
            #资源名称
            tmp['title'] = soup_r.h1.text
            #资源大小
            tmp['size'] = soup_r.find('ul', class_='base clearfix').find_all('li')[1].text
            #资源添加时间
            #tmp['time'] = soup_r.find('ul', class_='base clearfix').find_all('li')[2].text
            #清晰度
            tmp['definition'] = soup_r.find('ul', class_='base clearfix').find_all('li')[0].text
            tmp['name'] = name
            tmp['imdb'] = imdb
            movie_resources.append(tmp)
            time.sleep(0.5)
    print('找到 ' + str(len(movie_resources)) + ' 个资源！')
    return movie_resources
