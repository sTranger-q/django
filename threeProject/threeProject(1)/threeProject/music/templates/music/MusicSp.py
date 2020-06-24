from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time
from lxml import etree


def get_html(url):
    # 设置无界面打开
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # 发送请求
    driver.get(url)
    names = driver.find_elements_by_tag_name('iframe')[0]
    driver.switch_to.frame(names)
    soup = BeautifulSoup(driver.page_source, 'lxml').prettify()
    driver.close()
    driver.quit()
    return soup


def music_html(number):
    url = 'https://music.163.com/#/search/m/?type=1&s=%s' % number
    html = get_html(url)
    dom_tree = etree.HTML(html)  # 转换为python 的 html对象
    data_url = dom_tree.xpath(
        '//div[contains(@class,"item f-cb h-flag")]/div[contains(@class,"td w0")]/div/div/a[not(contains(@class,"mv"))]/@href'
    )  # /@href
    data_name = dom_tree.xpath(
        '//div[contains(@class,"item f-cb h-flag")]/div[contains(@class,"td w0")]/div/div/a/b/@title'
    )
    singer_name = dom_tree.xpath(
        '//div[contains(@class,"item f-cb h-flag")]/div[contains(@class,"td w1")]/div/a'
    )
    return zip([str.strip(i.text) for i in singer_name], data_name, data_url)
    # for i in data:
    #     print('`' + i.text + '```')
