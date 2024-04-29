import time
import datetime
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import re
import os
import threading
from queue import Queue
import eventlet
eventlet.monkey_patch()
now = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('[%m/%d %H:%M]Updated.')
urls = [
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iTWVpemhvdSI%3D",#梅州
    "https://fofa.info/result?qbase64=ImlwdHYiICYmIGNpdHk9IkppZXlhbmciICYmIHBvcnQ9IjgwODEi",#揭阳
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iU2hlbnpoZW4i",#深圳
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iR3Vhbmd6aG91Ig%3D%3D",#广州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iZ3Vhbmdkb25nIg%3D%3D" ,# Guangdong (广东)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iWmhhb3Fpbmci",#肇庆
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iWmhhbmppYW5nIg%3D%3D",#湛江
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iSHVpemhvdSI%3D",#惠州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iRm9zaGFuIg%3D%3D",#佛山
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iWmh1aGFpIg%3D%3D",#珠海
    "https://fofa.info/result?qbase64=ImlwdHYiICYmIGNpdHk9Ilpob25nc2hhbiI%3D",#中山
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY2l0eT0iRG9uZ2d1YW4i",#东莞
    "https://fofa.info/result?qbase64=ImlwdHYiICYmIGNpdHk9Ill1bGluIiAmJiBwb3J0PSI4MTgxIg%3D%3D"#广西玉林
]

def modify_urls(url):
    modified_urls = []
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find(":", ip_start_index)
    base_url = url[:ip_start_index]  # http:// or https://
    ip_address = url[ip_start_index:ip_end_index]
    port = url[ip_end_index:]
    ip_end = "/tsfile/live/1004_1.m3u8?key=txiptv&playlive=1&down=1"
    for i in range(1, 256):
        modified_ip = f"{ip_address[:-1]}{i}"
        modified_url = f"{base_url}{modified_ip}{port}{ip_end}"
        modified_urls.append(modified_url)

    return modified_urls

def is_url_accessible(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            print(f'{url} 【有效】')
            return url
    except requests.exceptions.RequestException:
        pass
    return None

results = []

for url in urls:
    # 创建一个Chrome WebDriver实例
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    # 使用WebDriver访问网页
    driver.get(url)  # 将网址替换为你要访问的网页地址
    time.sleep(10)
    # 获取网页内容
    page_content = driver.page_source
    # 关闭WebDriver
    driver.quit()
    # 查找所有符合指定格式的网址
    pattern = r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"  # 设置匹配的格式，如http://8.8.8.8:8888
    urls_all = re.findall(pattern, page_content)
    # urls = list(set(urls_all))  # 去重得到唯一的URL列表
    #urls = ['http://119.125.104.125:9901']  # 去重得到唯一的URL列表（测试）         ！！  仅测试119.125.104.XXX:9901  ！！
    urls = set(urls_all)                   # 去重得到唯一的URL列表（原句） 
    x_urls = []
    for url in urls:  # 对urls进行处理，ip第四位修改为1，并去重
        url = url.strip()
        ip_start_index = url.find("//") + 2
        ip_end_index = url.find(":", ip_start_index)
        ip_dot_start = url.find(".") + 1
        ip_dot_second = url.find(".", ip_dot_start) + 1
        ip_dot_three = url.find(".", ip_dot_second) + 1
        base_url = url[:ip_start_index]  # http:// or https://
        ip_address = url[ip_start_index:ip_dot_three]
        port = url[ip_end_index:]
        ip_end = "1"
        modified_ip = f"{ip_address}{ip_end}"
        x_url = f"{base_url}{modified_ip}{port}"
        x_urls.append(x_url)
    urls = set(x_urls)  # 去重得到唯一的URL列表

    valid_urls = []
    #   多线程获取可用url
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for url in urls:
            url = url.strip()
            modified_urls = modify_urls(url)
            for modified_url in modified_urls:
                futures.append(executor.submit(is_url_accessible, modified_url))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                valid_urls.append(result)

    for url in valid_urls:
        print(url)

with open("test.txt", 'w', encoding='utf-8') as file:
    file.write('TVB频道,#genre#\n')
    for url in valid_urls:
        file.write(f"翡翠台,{url}\n")
    file.write(f'{now},#genre#\n')
    file.write("Auto-update,http:// \n")
with open("test.m3u", 'w', encoding='utf-8') as file:
    file.write('#EXTM3U x-tvg-url="https://live.fanmingming.com/e.xml"\n')
    for url in valid_urls:
        file.write(f"#EXTINF:-1 tvg-name="翡翠台" tvg-logo=\"https://live.fanmingming.com/tv/翡翠台.png\" group-title=\"TVB频道\",翡翠台\n")
        file.write(f"{url}\n")
    file.write(f"#EXTINF:-1 tvg-name=\"\" tvg-logo=\"\" group-title=\"{now}\",Auto-update\n")
    file.write("http:// \n")
