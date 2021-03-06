import json
import os
import time

from common import douban, email_, pianyuan

def extra_new_resources():
    try:
        movie_list = douban.get_movie_list()


        #检查json文件是否存在，如果不存在则创建新文件
        if not os.path.exists(os.path.join(os.getcwd(), 'tmp')):
            os.mkdir(os.path.join(os.getcwd(), 'tmp'))
        if not os.path.exists(os.path.join(os.getcwd(), 'tmp', 'movie.json')):
            f = open(os.path.join(os.getcwd(), 'tmp', 'movie.json'), 'w')
            f.close()
        #检查日志文件
        if not os.path.exists(os.path.join(os.getcwd(), 'tmp', 'log.log')):
            f = open(os.path.join(os.getcwd(), 'tmp', 'log.log'), 'w')
            f.close()
        f = open(os.path.join(os.getcwd(), 'tmp', 'movie.json'), 'r+')

        all_resources = list()
        new_resources = list()
        for movie in movie_list:
            imdb = movie['imdb']
            resources = pianyuan.get_resources(imdb, movie['name'])
            if not resources:
                continue
            all_resources.extend(resources)
        try:
            file = json.load(f)
        except:
            new_resources = all_resources
        else:
            for i in all_resources:
                if i not in file:
                    new_resources.append(i)
        f.seek(0)
        f.truncate()
        json.dump(all_resources, f)
        f.close()
        return new_resources
    except:
        pass

while True:
    try:
        structTime = time.localtime(time.time())
        currentTime = str(structTime.tm_year) + '/' + str(structTime.tm_mon) + '/' + str(structTime.tm_mday)  + '\0' + str(structTime.tm_hour) + ':' + str(structTime.tm_min)
        new_s = extra_new_resources()
        if len(new_s) > 0:
            with open(os.path.join(os.getcwd(), 'tmp', 'log.log'), 'a+') as f:
                f.seek(0)
                f.write('\n[' + currentTime + ']' + '找到 ' + str(len(new_s)) + ' 个新资源！')
            print('找到 ' + str(len(new_s)) + ' 个新资源！')
            html_ = ''
            for i in new_s:
                html_ += '<h3>' + i['name'] + '</h3>' + '\n'
                html_ += '<p>' + i['title'] + '</p>' + '\n'
                html_ += '<p>清晰度 : ' + i['definition'] + '大小 :'  + i['size'] + '</p>' + '\n'
                html_ += '<p>链接 : <a href = "' + i['link'] + '">' + i['link'] + '</a></p>' + '</br>' + '\n' 
            subject_ = '你想看的电影有资源更新了😋'
            email_.send_email(html_,subject_)
        else:
            with open(os.path.join(os.getcwd(), 'tmp', 'log.log'), 'a+') as f:
                f.seek(0)
                f.write('\n[' + currentTime + ']' + '没有资源更新')
            print('没有资源更新')
        print('等待中 ... ')
        time.sleep(3600)
    except:
        pass
