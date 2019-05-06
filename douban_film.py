import requests
from lxml import etree
import pymysql

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 '
                  'Safari/537.36'}
cookies = {
    'cookie': 'bid=1ODC2TeoITo; douban-fav-remind=1; viewed="3530375"; '
              '_vwo_uuid_v2=DE4A253964C77BAACAE5AE5DB885AC159|125945e47c85df2d2988af8d55cc3dd3; ll="118254"; '
              '__utmz=223695111.1556643599.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); push_noty_num=0; '
              'push_doumail_num=0; __utmv=30149280.17837; __utmz=30149280.1556897053.7.4.utmcsr=baidu|utmccn=('
              'organic)|utmcmd=organic; _pk_ses.100001.4cf6=*; '
              '__utma=30149280.1737882674.1540127590.1556897053.1557101083.8; __utmc=30149280; '
              '__utma=223695111.1720841501.1556643599.1556807415.1557101083.4; __utmb=223695111.0.10.1557101083; '
              '__utmc=223695111; ap_v=0,6.0; douban-profile-remind=1; __utmt=1; __utmb=30149280.14.10.1557101083; '
              'dbcl2="178375857:4+R8ojgz7tM"; ck=Ut6g; '
              '_pk_id.100001.4cf6=94ae3a7841d370ad.1556643599.4.1557102385.1556808526.'}

url = ['https://movie.douban.com/people/178375857/collect?start={}&sort=time&rating=all&filter=all&mode=grid'.format(
    str(i)) for i in range(0, 556, 15)]

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password="123456",
                       db='blog')
cur = conn.cursor()


def get_titles(parse_url):
    html = requests.get(parse_url, cookies=cookies, headers=headers)
    selector = etree.HTML(html.text)
    result = selector.xpath('//*[@class="item"]')
    for li in result:
        subject = li.xpath('div[1]/a/@href')[0]
        pic = li.xpath('div[1]/a/img/@src')[0]
        title = li.xpath('div[2]/ul/li[1]/a/em/text()')[0]
        desc = li.xpath('div[2]/ul/li[2]/text()')[0]
        time = li.xpath('div[2]/ul/li[3]/span/text()')[0]

        title = pymysql.escape_string(title)
        desc = pymysql.escape_string(desc)

        # sql_insert = """insert into movie(subject, pic, title, `desc`, `time`) values("%s","%s","%s","%s","%s")""" % (
        #     subject, pic, title, desc, time)
        # cur.execute(sql_insert)
        # conn.commit()
        # print(sql_insert)
        print(subject, pic, title, desc, time)


for titles in url:
    get_titles(titles)
