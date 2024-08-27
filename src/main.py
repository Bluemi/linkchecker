#!/usr/bin/env python3

import argparse
import sys
from typing import Deque, Dict, List, Tuple

import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque

from utils import dump_data, print_links, is_same_domain, UrlInfo


def parse_args():
    parser = argparse.ArgumentParser(description='Crawling a website')
    parser.add_argument('url', type=str, help='The start url')
    parser.add_argument('--username', '-u', type=str, help='The username')
    parser.add_argument('--password', '-p', type=str, help='The password')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    return parser.parse_args()


def main():
    args = parse_args()
    auth = None
    if args.username and args.password:
        auth = HTTPBasicAuth(args.username, args.password)
    intern_urls, failed_urls, external_urls = crawl_website(args.url, auth=auth, verbose=args.verbose)

    dump_data(external_urls, failed_urls, intern_urls)
    print_links(external_urls, failed_urls, intern_urls)


def crawl_website(start_url: str, auth=None, verbose=False) -> Tuple[List[UrlInfo], List[UrlInfo], List[UrlInfo]]:
    """Crawl all links on the same domain starting from start_url."""
    visited: Dict[str, UrlInfo] = {}
    to_visit: Deque[UrlInfo] = deque([UrlInfo(start_url, None)])

    external_urls: Dict[str, UrlInfo] = {}
    failed_urls: List[UrlInfo] = []

    while to_visit:
        current_url_info = to_visit.popleft()
        if current_url_info.url in visited:
            continue
        visited[current_url_info.url] = current_url_info

        try:
            if verbose:
                print(f'load {current_url_info.url}')
            response = requests.get(current_url_info.url, auth=auth)
            response.raise_for_status()  # Ensure the request was successful
        except requests.RequestException as e:
            if verbose:
                print(f"  Failed to retrieve {current_url_info.url}: {e}")
            failed_urls.append(current_url_info)
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        new_counter = 0
        external_counter = 0
        already_counter = 0
        for link in soup.find_all('a', href=True):
            href = urljoin(start_url, link['href'])
            title = link.get_text(strip=True)
            if is_same_domain(href, start_url):
                if href in visited:
                    already_visited = visited[href]
                    already_visited.from_urls.add((current_url_info.url, title))
                    already_counter += 1
                else:
                    to_visit.append(UrlInfo(href, {(current_url_info.url, title)}))
                new_counter += 1
            else:
                if href in external_urls:
                    external_urls[href].from_urls.add((current_url_info.url, title))
                else:
                    external_urls[href] = UrlInfo(href, {(current_url_info.url, title)})
                    external_counter += 1
        if verbose:
            print(f'  found {new_counter} new links, {already_counter} old links and {external_counter} external links')

    return list(visited.values()), failed_urls, list(external_urls.values())


if __name__ == "__main__":
    main()
