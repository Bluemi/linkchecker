import argparse
import json

import requests

from utils import iter_all_urls, UrlInfo


def parse_args():
    parser = argparse.ArgumentParser(description='Inspecting data')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    return parser.parse_args()


def main():
    args = parse_args()

    with open('data.json', 'r') as f:
        data = json.load(f)

    # show_titles(data, args.verbose)
    check_external_links(data, args.verbose)


def show_titles(data, show_from_urls=False):
    for url_info in iter_all_urls(data):
        print(url_info.url)

        title_to_from_links = {}
        for from_url, title in url_info.from_urls:
            if title in title_to_from_links:
                title_to_from_links[title].append(from_url)
            else:
                title_to_from_links[title] = [from_url]

        if show_from_urls:
            for title, from_urls in title_to_from_links.items():
                print(f'  {title} -> {'  '.join(from_urls)}')
        else:
            print(f'  titles: {list(title_to_from_links.keys())}')


def check_external_links(data, verbose):
    for url_info in data['external_urls']:
        url_info = UrlInfo.from_dict(url_info)
        if verbose:
            print(f'loading "{url_info.url}"')
        if url_info.url.endswith('.zip'):
            if verbose:
                print('  skipping zip file')
            continue
        try:
            r = requests.get(url_info.url)
            r.raise_for_status()
            if verbose:
                print('  success')
        except Exception as e:
            print(f'  failed to get {url_info.url}')
            print(f'  from: {url_info.from_urls}')
            print(' ', e)
            print('  -----------------')


if __name__ == '__main__':
    main()
