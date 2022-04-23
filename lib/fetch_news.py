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
from requests import get
from os.path import isfile

from bs4 import BeautifulSoup, NavigableString, Tag

_filtered_out = [
    'Armed conflicts and attacks',
    'International relations',
    'Armed conflicts and attacks',
]


def fetch_news_page_url(date: datetime) -> str:
    """
    Fetch the url of the news page.

    :param date: Date of the news page.
    :return the page url.
    """
    return f'https://en.wikipedia.org/wiki/Portal:Current_events/{date.strftime("%B_%Y")}'


def _fetch_page(url: str, filename: str) -> None:
    """
    Fetch the news page from Wikipedia.
    """
    response = get(url)
    with open(f'page_cache/{filename}', 'w') as file:
        file.write(response.text)


def _is_filtered_out(tag: Tag) -> bool:
    """
    Some tags that may be controversial
    """
    parents = tag.find_parents('ul')
    for parent in parents:
        heading = parent.find_previous_sibling(
            'div', class_='current-events-content-heading')
        if heading is None:
            continue
        if heading.get_text() in _filtered_out:
            return True
    return False


def _is_leaf_event(tag: Tag) -> bool:
    """
    Check if the event is a leaf event, ie: does not have
        sub events.
    """
    return tag.name == 'li' and tag.find('li') == None and not _is_filtered_out(tag)


def fetch_news(url: str, date: datetime) -> list[str]:
    """
    Fetch the news from the wikipedia page and return the
        names.
    """
    filename = date.strftime('%B_%Y')
    if not isfile(f'page_cache/{filename}'):
        # If the page isn't cached, cache it.
        _fetch_page(url, filename)
    with open(f'page_cache/{filename}') as file:
        soup = BeautifulSoup(file, 'html.parser')
    days_events = soup.find(id=date.strftime('%Y_%B_%d'))
    if not days_events or isinstance(days_events, NavigableString):
        return []
    # Find all the simple events.
    events = days_events.find_all(_is_leaf_event)
    events = [event for event in events if event.get_text() not in [
        'edit', 'history', 'watch']]
    return [event.get_text().replace('\n', ' ') for event in events]
