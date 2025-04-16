from flask import Flask, render_template,request
from crawler import NewsCrawler,Newsanalysis

app = Flask(__name__)

time=''

def category_data(count_category):
    lt=[]
    for category,num in count_category.items():
        lt.append({'value':num,'name':category})
    return lt

app.add_template_filter(category_data, 'category_data')

def get_all_news(url='https://www.chinanews.com/scroll-news/news1.html'):
    crawler = NewsCrawler(url)
    news = crawler.get_news()
    return news

@app.route('/')
def index():
    news_data = get_all_news()
    analysis = Newsanalysis(news_data)
    analysis.count_category_news()
    return render_template('index.html',analysis=analysis)

@app.route('/', methods=['POST' ])
def get_time():
    time=request.form.get('time')
    news_data = get_all_news(url='https://www.chinanews.com/scroll-news/'+time[0:4]+'/'+time[4:8]+'/'+'news.shtml')
    analysis = Newsanalysis(news_data)
    analysis.count_category_news()
    return render_template('index.html',analysis=analysis)

if __name__ == '__main__':
    app.run(debug=True)
