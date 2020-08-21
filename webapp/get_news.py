from bs4 import BeautifulSoup
from datetime import datetime
from webapp.model import db, News
import requests


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


def get_python_news(url="https://www.python.org/blogs/"):
    html = get_html(url)

    if html:
        soup = BeautifulSoup(html, "html.parser")
        news = soup.find("ul", class_="list-recent-posts menu").find_all("li")
        # можно еще вот так: news_list = soup.find_all("h3", class_="event-title")
        for i in news:
            url = i.find("a")["href"]
            title = i.find("a").text
            date = i.find("p").text.replace(".", "")
            try:
                date = datetime.strptime(date, "%B %d, %Y")
            except ValueError:
                date = datetime.now()
            save_news(title, url, date)


def save_news(title, url, date):
    news_exists = News.query.filter(News.url == url).count()
    if not news_exists:
        new_news = News(title=title, url=url, date=date)
        db.session.add(new_news)
        db.session.commit()


if __name__ == "__main__":
    get_python_news()
