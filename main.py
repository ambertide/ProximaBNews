"""
ProximaBNews A news bot for twitter
Copyright (C) 2022 Ege Emir Özkan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

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


def tweet_news(event, context) -> None:
    date = get_date()
    url = fetch_news_page_url(get_date())
    news = fetch_news(url, date)
    send_news(news, url, date)

if __name__ == '__main__':
    tweet_news(None, None)
