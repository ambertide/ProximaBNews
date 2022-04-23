from datetime import datetime
from typing import Dict, Optional, Union
from requests import post, request
from requests_oauthlib import OAuth1
from os import getenv

APP_KEY = getenv('CONSUMER_KEY')
APP_SECRET = getenv('CONSUMER_SECRET')
OAUTH_TOKEN = getenv('OAUTH_TOKEN')
OAUTH_SECRET = getenv('OAUTH_SECRET')

auth = OAuth1(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_SECRET)


def _post_tweet(text: str, reply_to: Optional[str] = None) -> str:
    """
    Post a tweet and return its id.

    :param text: Text to tweet
    :param reply_to: Tweet being replied to.
    :return the id of the tweet.
    """
    request_body: Dict[str, Union[str, dict]] = {'text': text}
    if reply_to:
        request_body['reply'] = {'in_reply_to_tweet_id': reply_to}
    resp = post('https://api.twitter.com/2/tweets',
                auth=auth, json=request_body)
    return resp.json()['data']['id']


def _post_header(date: datetime) -> str:
    """
    Post the header with the sources. Return the post id.
    """
    header = f"Greatings from Proxima B News Network, here are the latest news from Earth, dated: {date.strftime('%B %d, %Y')}"
    return _post_tweet(header)


def _partition_new(new: str) -> list[str]:
    """
    Partition a new to strings of length at maximum 280.
    """
    # Split by spaces.
    new_naive_split = new.split(' ')
    new_naive_split.reverse()
    new_split = [new_naive_split.pop(), ]
    while new_naive_split:
        # Until we integrate all of these
        next_new = new_naive_split.pop()
        if len(new_split[-1] + ' ' + next_new) > 277:
            new_split[-1] += '...'
            new_split.append('...' + next_new)
        else:
            new_split[-1] += ' ' + next_new
    return new_split


def _post_new(new: str, last_id: str) -> str:
    """
    Post the new and return the latest id.
    """
    news = [new, ]
    if len(new) > 280:
        news = _partition_new(new)
    latest_id = last_id
    for new in news:
        latest_id = _post_tweet(new, latest_id)
    return latest_id


def _post_footer(source: str, last_id) -> str:
    """
    Post the source citation.
    """
    footer = f'This has been today\'s Proxima B News Network, news data courtesy of {source}.'
    return _post_tweet(footer, last_id)


def send_news(news: list[str], source: str, date: datetime) -> None:
    """
    Send to twitter.
    """
    header_id = _post_header(date)
    latest_id = header_id
    for new_index, new in enumerate(news):
        latest_id = _post_new(f'{new_index + 1}) {new}', latest_id)
    _post_footer(source, latest_id)
