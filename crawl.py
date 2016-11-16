import argparse
import asyncio
from urllib.parse import urljoin, urlsplit

import aiohttp
from bs4 import BeautifulSoup

_crawled_pages = []


def _checkLink(from_url, to_url):
    # don't follow links out from the domain
    parts = urlsplit(to_url)
    if parts.hostname and parts.hostname != urlsplit(from_url).hostname:
        return False

    # strip query string
    url = urljoin(from_url, parts.path)

    # ensure we don't crawl the same page twice
    if url in _crawled_pages:
        return False
    else:
        _crawled_pages.append(url)

    return True


async def _handlePage(loop, session, url, depth_remaining):
    print(str.format('Getting {}', url))
    # get page
    async with session.get(url) as response:
        # get the page
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')

        # recurse if we have depth left
        if depth_remaining > 1:
            links = [link.get('href') for link in soup.find_all('a')]
            for link in links:
                new_url = urljoin(url, link)

                # check whether we want to follow the link
                if _checkLink(url, new_url):
                    await _handlePage(loop, session, new_url, depth_remaining - 1)

        # print image links
        images = [img.get('src') for img in soup.find_all('img', src=True)]
        for image in images:
            print(urljoin(url, image))


async def _crawl(loop, url, depth):
    print(str.format('Parsing {} for {} level(s)', url, depth))

    # run checklink to add initial page to the crawled pages list
    _checkLink(url, url)

    async with aiohttp.ClientSession(loop=loop) as session:
        await _handlePage(loop, session, url, depth)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', metavar='URL', help='The URL to crawl')
    parser.add_argument('--depth', dest='depth', type=int, default=1,
                        help='How many levels of links should be followed')
    arguments = parser.parse_args()

    # start crawling async
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_crawl(loop, arguments.url, arguments.depth))


if __name__ == '__main__':
    main()
