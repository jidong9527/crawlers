# encoding: utf-8
# author: jidongdong

from lxml import etree
import requests
import re

BASE_URL = "http://www.dytt8.net"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400"
}


def get_detail_urls(url):
    response = requests.get(url, headers=HEADERS)
    # text = response.content.decode('gbk')
    text = response.text
    html = etree.HTML(text)
    detail_urls = html.xpath("//table[@class='tbspan']//a/@href")
    detail_urls = map(lambda url:BASE_URL+url, detail_urls)
    return detail_urls


def parse_detail_page(url):
    movie = {}
    response = requests.get(url, headers=HEADERS)
    text = response.content.decode("gbk")
    html = etree.HTML(text)
    title = html.xpath("//div[@class='title_all']/h1/font/text()")
    movie["title"] = title

    zoom_element = html.xpath("//div[@id='Zoom']")[0]
    imgs = zoom_element.xpath(".//img/@src")

    movie["cover"] = imgs[0]
    movie["screenshot"] = imgs[1]

    def parse_info(info, rule):
        return info.replace(rule, "").strip()

    infos = zoom_element.xpath(".//text()")
    for index, info in enumerate(infos):
        print(index, info)
        if info.startswith("◎年　　代"):
            info = parse_info(info, "◎年　　代")
            movie["year"] = info
        elif info.startswith("◎产　　地"):
            info = parse_info(info, "◎产　　地")
            movie["country"] = info
        elif info.startswith("◎类　　别"):
            info = parse_info(info,"◎类　　别")
            movie['category'] = info
        elif info.startswith("◎豆瓣评分"):
            info = parse_info(info,"◎豆瓣评分")
            movie['douban_rating'] = info
        elif info.startswith("◎片　　长"):
            info = parse_info(info,"◎片　　长")
            movie['duration'] = info
        elif info.startswith("◎导　　演"):
            info = parse_info(info,"◎导　　演")
            movie['director'] = info
        elif info.startswith("◎主　　演"):
            info = parse_info(info,"◎主　　演")
            actors = [info]
            for x in range(index+1,len(infos)):
                actor = infos[x].strip()
                if actor.startswith("◎"):
                    break
                actors.append(actor)
            movie['actors'] = actors
        elif info.startswith("◎简　　介"):
            info = parse_info(info,"◎简　　介")
            for x in range(index+1,len(infos)):
                profile = infos[x].strip()
                movie["profile"] = profile
    download_url = html.xpath("//td[@bgcolor='#fdfddf']/a/@href")[0]
    movie['download_url'] = download_url
    return movie

def spider():
    list_url = "http://www.dytt8.net/html/gndy/dyzz/list_23_{}.html"
    movies = []

    # 获取最新电影的总页数
    # //div[@class='co_content8']/div[@class='x']/text()
    index_url = list_url.format("1")
    response = requests.get(index_url, headers=HEADERS)
    text = response.content.decode("gbk")
    html = etree.HTML(text)
    page_info = html.xpath("//div[@class='co_content8']/div[@class='x']//text()")[1]
    # 共172页/4276条记录  首页1
    PATTERN = "(.*)共(.*)页/(.*)"
    pattern = re.compile(PATTERN)
    search = pattern.search(page_info)
    if search:
        page_num = int(search.group(2))
    else:
        page_num = 7
    print("The total page number is {}".format(page_num))

    for x in range(1,page_num + 1):
        # 第一个for循环用来控制总页数
        url = list_url.format(x)
        detail_urls = get_detail_urls(url)
        for detail_url in detail_urls:
            # 第二个for循环时用来遍历一页中所有电影的详情url
            movie = parse_detail_page(detail_url)
            movies.append(movie)
            print(movie)

if __name__ == '__main__':
    spider()