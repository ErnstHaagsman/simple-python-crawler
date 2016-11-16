import argparse


def _crawl(url, depth):
    print(str.format('Parsing {} for {} level(s)', url, depth))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', metavar='URL', help='The URL to crawl')
    parser.add_argument('--depth', dest='depth', type=int, default=1,
                        help='How many levels of links should be followed')
    arguments = parser.parse_args()
    _crawl(arguments.url, arguments.depth)


if __name__ == '__main__':
    main()