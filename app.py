from flask import Flask, render_template
from crawler import NewsCrawler,Newsanalysis

app = Flask(__name__)

def category_data(count_category):
    lt=[]
    for category,num in count_category.items():
        lt.append({'value':num,'name':category})
    return lt

app.add_template_filter(category_data, 'category_data')

def get_all_news():
    crawler = NewsCrawler()
    news = crawler.get_news()
    return news

@app.route('/')
def index():
    news_data = get_all_news()
    analysis = Newsanalysis(news_data)
    analysis.count_category_news()
    return render_template('index.html',analysis=analysis)

if __name__ == '__main__':
    app.run(debug=True)
