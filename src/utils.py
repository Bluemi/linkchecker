import json
from itertools import chain
from typing import List, Set, Tuple
from urllib.parse import urlparse


def is_same_domain(url1, url2):
    """Check if two URLs belong to the same domain."""
    return urlparse(url1).netloc == urlparse(url2).netloc


class UrlInfo:
    def __init__(self, url: str, from_urls: Set[Tuple[str, str]] | None = None):
        self.url = url
        if from_urls is None:
            from_urls = set()
        # from urls is a set of tuples (from, title), where from is an url from where this url has been linked and title
        # is the title of the href element pointing to this url
        self.from_urls: Set[Tuple[str, str]] = from_urls

    def to_dict(self):
        return {
            'url': self.url,
            'from': list(self.from_urls)
        }

    @staticmethod
    def from_dict(data):
        from_urls = set(tuple(f) for f in data['from'])
        return UrlInfo(data['url'], from_urls)

    def __eq__(self, other):
        if isinstance(other, UrlInfo):
            return self.url == other.url
        return False

    def __hash__(self):
        return hash(self.url)

    def __repr__(self):
        return f"UrlInfo(url={self.url}, from={list(self.from_urls)})"


def dump_data(external_urls: List[UrlInfo], failed_urls: List[UrlInfo], intern_urls: List[UrlInfo]):
    data = {
        'intern_urls': [url.to_dict() for url in intern_urls],
        'failed_urls': [url.to_dict() for url in failed_urls],
        'external_urls': [url.to_dict() for url in external_urls]
    }
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)


def print_links(external_urls: List[UrlInfo], failed_urls: List[UrlInfo], intern_urls: List[UrlInfo]):
    print("Crawled Links:")
    for link in intern_urls:
        print(' ', link)
    print("Failed Links:")
    for link in failed_urls:
        print(' ', link)
    print("External Links:")
    for link in external_urls:
        print(' ', link)


def iter_all_urls(data):
    return [UrlInfo.from_dict(ui) for ui in chain(data['intern_urls'], data['failed_urls'], data['external_urls'])]
