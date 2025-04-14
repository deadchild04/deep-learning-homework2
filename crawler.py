import requests
from bs4 import BeautifulSoup

class NewsCrawler:
    def __init__(self):
        self.url='https://www.chinanews.com/scroll-news/news1.html'

    def parse_news(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        news_items = []
        ul=soup.select('div.content-left div.content_list ul li')

        for item in ul:
            if item.select_one('div.dd_lm a') is None:
                continue
            category=item.select_one('div.dd_lm a').text.strip()
            title=item.select_one('div.dd_bt a').text.strip()
            link='https://www.chinanews.com/'+item.select_one('div.dd_bt a')['href']
            time=item.select_one('div.dd_time').text.strip()
            news_items.append({'category':category,'title':title,'link':link,'time':time}) 

        return news_items

    def get_news(self):
        url = self.url

        try:
            response = requests.get(url, timeout=10)
            response.encoding = 'utf-8'
            return self.parse_news(response.text)
        
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return []