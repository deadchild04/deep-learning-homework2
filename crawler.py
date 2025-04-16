import requests
from bs4 import BeautifulSoup

class NewsCrawler:
    def __init__(self,url):
        self.url=url
        
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
        
class Newsanalysis:
    def __init__(self, news_list):
        self.news_list = news_list
        self.count_category = {}

    def count_category_news(self):
        for news in self.news_list:
            category = news['category']
            if category in self.count_category:
                self.count_category[category] += 1
            else:
                self.count_category[category] = 1