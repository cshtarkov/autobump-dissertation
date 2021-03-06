#!/usr/bin/env python3
#
# Scrapes at least the first N projects that support
# Python 3 from pypi-ranking.info and pypi.org.
# The output is in the form (reponame, url, popularity).
#
import re
import sys
import requests
import lxml.html


def get_module_github(name):
    """Find the GitHub repository of a project with this 'name'.
    Returns None if it isn't found."""

    # First, get pypi-ranking module page to find out actual PyPI page
    content = requests.get("http://pypi-ranking.info/module/{}".format(name)).content
    tree = lxml.html.fromstring(content)
    url = tree.xpath('//h2[@id="item_title"]/a/@href')
    if len(url) == 0:
        return None
    url = url[0]

    # Fetch actual PyPI page and look for GitHub link
    content = requests.get(url).content
    tree = lxml.html.fromstring(content)
    links = tree.xpath('//a/@href')

    for link in reversed(links):
        if re.match(r"https?://github\.com/.*/" + name.lower() + r"$", link):
            return link


def get_modules_at_page(page):
    """Return a list of Python 3 compatible modules at a pypi-ranking.info page."""

    content = requests.get("http://pypi-ranking.info/alltime?page={}".format(page)).content
    tree = lxml.html.fromstring(content)

    def py3_compatible(module):
        _, attributes, _ = module
        return len(attributes.getchildren()) > 0

    def has_github_repo(module):
        _, repo, _ = module
        return repo is not None

    def subst_github_repo(module):
        name, _, count = module
        return name, get_module_github(name), count

    def popularity_to_int(module):
        name, repo, count = module
        return name, repo, int(count.replace(",", ""))

    return map(popularity_to_int,
               filter(has_github_repo,
                      map(subst_github_repo,
                          filter(py3_compatible,
                                 zip(tree.xpath('//span[@class="list_title"]/text()'),
                                     tree.xpath('//td[@class="attributes"]'),
                                     tree.xpath('//td[@class="count"]/span/text()'))))))


def get_modules_lower_bound(lower_bound):
    """Find the first at least 'lower_bound' Python 3 compatible modules at pypi-ranking.info"""

    page = 1
    count = 0
    while count < lower_bound:
        for module in get_modules_at_page(page):
            count = count + 1
            yield module
        page = page + 1


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Not enough arguments!"
    lower_bound = int(sys.argv[1])
    for name, repo, popularity in get_modules_lower_bound(lower_bound):
        print(name, repo, popularity)
