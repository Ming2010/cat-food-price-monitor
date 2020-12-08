import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# 设置filter
filter_in = '车'
filter_out = '团购'

# 设置起始和结束页面
def set_url(n):
    """设置需要爬取的页面数量"""
    url = 'https://www.douban.com/group/656297/discussion?start='
    urls = []
    for i in tqdm(range(n), ascii=True, desc='Processing '):
        current_url = url + str(25*i)
        urls.append(current_url)
    return urls

def get_response(urls):
    """获得页面内容"""
    responses = []
    for url in urls:
        response = requests.get(url=url, headers={'User-Agent': "Resistance is futile"}).  # we don't have to give the exact header
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
    urls = set_url(1)
    responses = get_response(urls)
    records = get_records(responses)

    for record in records:
        print(record)
