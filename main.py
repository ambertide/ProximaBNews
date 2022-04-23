from datetime import datetime
from pprint import pprint
from dateutil.relativedelta import relativedelta
from lib import fetch_news_page_url
from lib.fetch_news import fetch_news
from lib.send_tweets import send_news


def get_date() -> datetime:
    """
    Get the date on earth as it would be seen from Proxima Centauri B
    """
    return datetime.now() - relativedelta(days=1533)


if __name__ == '__main__':
    date = get_date()
    url = fetch_news_page_url(get_date())
    news = fetch_news(url, date)
    send_news(news, url, date)
