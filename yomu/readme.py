import argparse
import logging
from typing import Optional

import feedparser
import requests
from bs4 import BeautifulSoup
from snakemd import Document, Inline, Table

logger = logging.getLogger(__name__)


def main() -> None:
    """
    The main drop in function for README generation.

    :return: nothing
    """
    loglevel = _get_log_level()
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {loglevel}')
    logging.basicConfig(level=numeric_level)
    how_to = HowTo()
    how_to.page.dump("README")


def _get_log_level() -> str:
    """
    A helper function which gets the log level from 
    the command line. Set as warning from default. 

    :return: the log level provided by the user
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-log",
        "--log",
        default="warning",
        help=(
            "Provide logging level. "
            "Example --log debug', default='warning'"
        ),
    )
    options = parser.parse_args()
    return options.log


def _get_intro_text() -> str:
    return """
    Welcome to a collection of Jupyter Notebooks from the How to Python series on The Renegade Coder. For 
    convenience, you can access all of the articles, videos, challenges, and source code below. Alternatively, I keep 
    an enormous article up to date with all these snippets as well.
    """


def get_series_posts() -> list:
    """
    Collects all posts from the series into a feed. 

    :return: a list of posts from the How to Python series
    """
    index = 1
    base = "https://therenegadecoder.com/series/how-to-python/feed/?paged="
    feed = []
    while (rss := feedparser.parse(f"{base}{index}")).entries:
        feed.extend(rss.entries)
        index += 1
    logger.debug(f"Collected {len(feed)} posts")
    return feed


def get_youtube_video(entry) -> Inline:
    """
    Generates an InlineText item corresponding to the YouTube
    video link if it exists. Otherwise, it returns an empty
    InlineText element.

    :param entry: a feedparser entry
    :return: the YouTube video as an InlineText element
    """
    content = entry.content[0].value
    soup = BeautifulSoup(content, "html.parser")
    target = soup.find("h2", string="Video Summary")
    if target:
        url = target.find_next_sibling().find_all("a")[-1]["href"]
        return Inline("Video", link=url)
    return Inline("")


def get_slug(title: str, sep: str) -> str:
    """
    Converts a title to a slug.

    :param title: title of item
    :param sep: the separator to use in place of whitespace
    :return: a slug from a title
    """
    return title.split(":")[0][:-10].lower().replace(" ", sep)


def verify_url(url: str) -> bool:
    """
    Checks that a URL exists. 

    :param url: the URL to verify
    :return: True if the URL exists; False otherwise
    """
    try:
        r = requests.get(url)
        if r.status_code == 404:
            logger.debug(f"URL does not exist: {url}")
            return False
    except:
        logger.warning(f"Issue loading URL: {url}")
        return False
    return True


def get_challenge(title: str) -> Inline:
    """
    Retrieves the link to the challenge code samples.

    :param title: the title of the article
    :return: the link to the challenge folder, if it exists
    """
    slug = get_slug(title, "-")
    base = "https://github.com/TheRenegadeCoder/how-to-python-code/tree/main/challenges/"
    challenge = Inline("Challenge", link=f"{base}{slug}")
    if not verify_url(challenge._link):
        return Inline("")
    return challenge


def get_notebook(title: str) -> Inline:
    """
    Retrieves the link to the Jupyter Notebook for the article.

    :param title: the title of the article
    :return: the link to the notebook, if it exists
    """
    slug = get_slug(title, "_")
    base = "https://github.com/TheRenegadeCoder/how-to-python-code/tree/main/notebooks/"
    notebook = Inline("Notebook", link=f"{base}{slug}.ipynb")
    if not verify_url(notebook._link):
        return Inline("")
    return notebook


def get_test(title: str) -> Inline:
    """
    Retrieves the test file for the article.

    :param title: the title of the article
    :return: the link to the test, if it exists
    """
    slug = get_slug(title, "_")
    base = "https://github.com/TheRenegadeCoder/how-to-python-code/tree/main/testing/"
    test = Inline("Test", link=f"{base}{slug}.py")
    if not verify_url(test._link):
        return Inline("")
    return test


class HowTo:
    def __init__(self):
        self.page: Optional[Document] = None
        self.feed: Optional[list] = None
        self._load_data()
        self._build_readme()

    def _load_data(self):
        self.feed = get_series_posts()

    def _build_readme(self):
        self.page = Document()

        # Introduction
        self.page.add_heading("How to Python - Source Code")
        self.page.add_paragraph(_get_intro_text()) \
            .insert_link("How to Python", "https://therenegadecoder.com/series/how-to-python/") \
            .insert_link(
                "an enormous article",
                "https://therenegadecoder.com/code/python-code-snippets-for-everyday-problems/"
        )

        # Table
        headers = [
            "Index",
            "Title",
            "Publish Date",
            "Article",
            "Video",
            "Challenge",
            "Notebook",
            "Testing"
        ]
        table = Table(
            [Inline(header) for header in headers],
            self.build_table()
        )
        self.page.add_block(table)

    def build_table(self) -> list[list[Inline]]:
        index = 1
        body = []
        for entry in self.feed:
            if "Code Snippets" not in entry.title:
                article = Inline("Article", link=entry.link)
                youtube = get_youtube_video(entry)
                challenge = get_challenge(entry.title)
                notebook = get_notebook(entry.title)
                test = get_test(entry.title)
                body.append([
                    Inline(str(index)),
                    Inline(entry.title),
                    Inline(entry.published),
                    article,
                    youtube,
                    challenge,
                    notebook,
                    test
                ])
                index += 1
        return body


if __name__ == '__main__':
    main()
