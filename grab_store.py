import time
import requests
from bs4 import BeautifulSoup

# 设置filter
filter_in = '车'
filter_out = '团购'

# 设置起始和结束页面
def set_url(n):
    """设置需要爬取的页面数量"""
    url = 'https://www.douban.com/group/656297/discussion?start='
    urls = []
    for i in range(n):
        current_url = url + str(25*i)
        urls.append(current_url)
        time.sleep(2)
    return urls

def get_response(urls):
    """获得页面内容"""
    responses = []
    # 设置请求头
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    for url in urls:
        response = requests.get(url=url, headers=headers)
        responses.append(response)
    return responses

def get_records(responses):
    """解析页面内容，并对记录进行初步筛选"""
    records = []
    # get records from each page
    for response in responses:
        soup = BeautifulSoup(response.text, "html.parser")

        # 获取帖子列表，将帖子链接和帖子名存储到列表中
        table = soup.find("table")
        td_list = table.find_all(class_="title")
        for td in td_list:
            soup_a = td.find_all('a')[0]
            href = soup_a.get('href')
            title = soup_a.get('title')
            # 对帖子进行筛选
            if filter_out not in title and filter_in in title:
                record = dict()
                record['href'] = href
                record['title'] = title
                records.append(record)

    return records

if __name__ == '__main__':
    urls = set_url(10)
    responses = get_response(urls)
    records = get_records(responses)

    for record in records:
        print(record)
