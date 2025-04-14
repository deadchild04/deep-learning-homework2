from flask import Flask, render_template
from crawler import NewsCrawler

app = Flask(__name__)

def get_all_news():
    crawler = NewsCrawler()
    news = crawler.get_news()
    return news

news_data = get_all_news()


@app.route('/')
def index():
    news_data = get_all_news()
    return render_template('index.html', news_data=news_data)

if __name__ == '__main__':
    app.run(debug=True)