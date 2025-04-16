from flask import Flask, render_template,request,redirect,url_for
from crawler import NewsCrawler,Newsanalysis

app = Flask(__name__)

analysis=None

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
    global analysis
    analysis= Newsanalysis(news_data)
    analysis.count_category_news()
    return render_template('index.html',analysis=analysis)

@app.route('/', methods=['POST' ])
def get_time():
    time=request.form.get('time')
    news_data = get_all_news(url='https://www.chinanews.com/scroll-news/'+time[0:4]+'/'+time[4:8]+'/'+'news.shtml')
    global analysis
    analysis = Newsanalysis(news_data)
    analysis.count_category_news()
    return render_template('index.html',analysis=analysis)

@app.route('/process',methods=['POST'])
def process():
    category=request.form.get('category')
    return redirect(url_for('news_category',category=category))

@app.route('/news_category/<category>')
def news_category(category):
    data=[analysis.news_list[i] for i in range(len(analysis.news_list)) if analysis.news_list[i]['category']==category]
    return render_template('news_category.html',data=data,category=category)
    
if __name__ == '__main__':
    app.run(debug=True)
