from flask import Flask, render_template
from webapp.get_news import get_python_news
from webapp.model import db, News
from webapp.weather import weather_by_city


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)

    @app.route("/")
    def index():
        title = "Новости Python"
        weather = weather_by_city(app.config["WEATHER_DEFAULT_CITY"])
        news_list = News.query.order_by(News.date.desc()).all()
        return render_template("index.html",
                                page_title=title,
                                weather=weather,
                                news_list=news_list)
    return app
