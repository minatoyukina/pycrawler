from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import time
import pymysql

chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(
    executable_path=(r'C:\Users\chenchuanqi\AppData\Local\Google\Chrome\Application'
                     r'\chromedriver.exe'), chrome_options=chrome_options)
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password="123456",
                       db='blog')
cur = conn.cursor()


def get_data(_browser, _type):
    ul = _browser.find_element_by_css_selector("ul")
    lists = ul.find_elements_by_tag_name("li")
    for li in lists:
        temp = li.find_element_by_class_name('opt').find_element_by_class_name('icn-share')
        title = temp.get_attribute('data-res-name')
        author = temp.get_attribute('data-res-author')
        width = li.find_element_by_class_name('bg').get_attribute('style')
        href = li.find_element_by_class_name('txt').find_element_by_tag_name('a').get_attribute('href')
        date_now = time.strftime("%Y-%m-%d", time.localtime())
        print(_type, title, author, width, href, date_now)

        sql_insert = """insert into wy_music(`type`,title, author, width, link,`date`) values("%s","%s","%s",
                "%s","%s","%s")""" % (_type, title, author, width, href, date_now)
        cur.execute(sql_insert)
        conn.commit()


def main():
    sql_check = "drop table if exists wy_music"
    sql_table = """
                create table wy_music(
                `type` enum("WEEK", "ALL") default 'WEEK',
                title varchar(256),
                author varchar(256),
                width varchar(200),
                link varchar(200),
                `date` varchar(20)
                )"""
    cur.execute(sql_check)
    cur.execute(sql_table)
    conn.commit()

    browser.get('https://music.163.com/#/user/songs/rank?id=60750004')
    browser.switch_to.frame('contentFrame')
    sleep(3)
    get_data(browser, 'WEEK')
    btn = browser.find_element_by_class_name('f-cb').find_element_by_id('songsall')
    sleep(3)
    btn.click()
    sleep(3)
    get_data(browser, 'ALL')
    browser.close()


if __name__ == '__main__':
    main()
