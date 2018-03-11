#encoding: utf-8
#author: jidongdong
# 爬取豆瓣上正在上映的电影
import requests
from lxml import etree

# 1. 将目标网站上的页面抓取下来
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400",
    "Referer": "https://movie.douban.com/explore"
}
url = "https://movie.douban.com/cinema/nowplaying/beijing/"

response = requests.get(url, headers=headers)
text = response.text
# response.text 返回的是一个经过解码后的字符串，是str(unicode)类型
# response.content 返回的是一个原生字符串，就是从网页上抓取的，没有经过
# 处理的字符串，是bytes类型

# 2. 将抓取的数据根据一定的规则提取
html = etree.HTML(text)
ul = html.xpath("//ul[@class='lists']")[0]
# print(etree.tostring(ul, encoding="utf-8").decode("utf-8"))
lis = ul.xpath("./li")
movies = []
for li in lis:
    title = li.xpath("@data-title")[0]
    score = li.xpath("@data-score")[0]
    duration = li.xpath("@data-duration")[0]
    region = li.xpath("@data-region")[0]
    director = li.xpath("@data-director")[0]
    actors = li.xpath("@data-actors")[0]
    thumbnail = li.xpath(".//img/@src")[0]

    movie = {
        "title": title,
        "score": score,
        "duration": duration,
        "region": region,
        "director": director,
        "actors": actors,
        "thumbnail": thumbnail
    }
    movies.append(movie)

print(movies)
