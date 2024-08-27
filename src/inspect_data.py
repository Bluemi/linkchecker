import argparse
import json
import os
from urllib.parse import urlparse, quote

import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
from spellchecker import SpellChecker

from ignore_words import ignore_word
from utils import iter_all_urls, UrlInfo, normalize_string


GERMAN_PAGES = [
    'https://dev.visual-computing.com/publications/perceived-color-difference-ein-spielerisches-experiment-zur-'
    'erfassung-empfundener-farbunterschiede',
    'https://dev.visual-computing.com/policy',
    'https://dev.visual-computing.com/imprint',
]


def parse_args():
    parser = argparse.ArgumentParser(description='Inspecting data')
    parser.add_argument('--username', '-u', type=str, help='The username')
    parser.add_argument('--password', '-p', type=str, help='The password')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    return parser.parse_args()


def main():
    args = parse_args()
    auth = None
    if args.username and args.password:
        auth = HTTPBasicAuth(args.username, args.password)

    with open('data.json', 'r') as f:
        data = json.load(f)

    # show_titles(data, args.verbose)
    # check_external_links(data, args.verbose)
    # load_page_and_execute(data, check_page, auth, verbose=args.verbose)
    load_page_and_execute(data, check_lorem_ipsum, auth, verbose=args.verbose)


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


def load_page_and_execute(data, func, auth=None, verbose=False):
    paths = []
    # load pages
    for url_info in data['intern_urls']:
        url_info = UrlInfo.from_dict(url_info)
        if verbose:
            print(f'loading {url_info.url}')
        filepath = save_page(url_info.url, auth=auth, verbose=verbose)
        if filepath is not None:
            paths.append((filepath, url_info))

    for filepath, url_info in paths:
        func(filepath, url_info)


def check_page(filepath, url_info):
    print(f'checking {url_info.url}')
    if url_info.url in GERMAN_PAGES:
        print('  skip german')
        return
    html_content = load_html_from_disk(filepath)
    text = extract_text_from_html(html_content)
    typos = check_for_typos(text)

    if typos:
        print(f"  found {len(typos)} typos:")
        for typo in typos:
            print(f" - '{typo}'")
    else:
        print("No typos found.")


def save_page(url, auth=None, directory="pages", verbose=False):
    # Parse the URL to create a valid filename
    parsed_url = urlparse(url)
    filename = f"{parsed_url.netloc}{parsed_url.path}"

    # Replace any unsafe characters with safe ones for file names
    filename = quote(filename, safe="")

    # Ensure the filename ends with .html
    if not filename.endswith(".html"):
        filename += ".html"

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Full path to save the file
    filepath = os.path.join(directory, filename)

    # Check if the file already exists
    if os.path.exists(filepath):
        if verbose:
            print(f"  skip '{filename}'. already exists")
        return filepath

    try:
        # Fetch the page content
        response = requests.get(url, auth=auth)
        response.raise_for_status()  # Check for HTTP errors

        # Save the content to the file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(response.text)

        if verbose:
            print(f"  saved '{url}' to '{filepath}'.")
    except requests.RequestException as e:
        if verbose:
            print(f"  failed to fetch '{url}': {e}")
        return None

    return filepath


def load_html_from_disk(filepath):
    """Load the HTML content from a file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file '{filepath}' does not exist.")

    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


def extract_text_from_html(html_content):
    """Extract the text content from HTML using BeautifulSoup."""
    soup = BeautifulSoup(html_content, 'html.parser')
    for div in soup.find_all("div", class_="background-code"):
        div.decompose()  # This removes the element from the tree
    return soup.get_text()


def check_for_typos(text):
    """Check the text for typos using the SpellChecker."""
    spell = SpellChecker()
    words = []
    for s in text.split():
        words.extend(normalize_string(s))
    typos = spell.unknown(words)
    typos = [t for t in typos if not ignore_word(t)]
    return typos


def check_lorem_ipsum(filepath, url_info):
    html_content = load_html_from_disk(filepath)
    text = extract_text_from_html(html_content)
    if check_for_lorem_ipsum(text):
        print(f'found lorem ipsum in {url_info.url}')


def check_for_lorem_ipsum(text):
    """Check the text for typos using the SpellChecker."""
    words = []
    for s in text.split():
        words.extend(normalize_string(s))
    words = [w.lower() for w in words]
    return 'lorem' in words


if __name__ == '__main__':
    main()
