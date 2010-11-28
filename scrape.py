#!/usr/bin/env python

"""
TODO
"""

import re
import sys
import urllib2
import urllib

# re is fine for now
#from BeautifulSoup import BeautifulSoup


class Review(object):
    def __init__(self, url):
        self.url = url
        self._set_html()
        #self._set_soup()
        self._set_date()
        self._set_text()
        self._set_star_rating()
        self._set_title()
        self._set_helpfulness()

        self._set_reviewer()
        self._set_product_name()

    def _set_html(self):
        page = urllib.urlopen(self.url)
        self.html = page.read()

    def _set_soup(self):
        self.soup = BeautifulSoup(self.html)
        pass

    def _set_date(self):
        """Set self.date to the date found in the review's HTML."""
        pat = re.compile(r'<nobr>(.*?)</nobr>')
        match = pat.search(self.html)
        (date,) = match.groups()
        self.date = date

    def _set_text(self):
        pat = re.compile(r'<span class="description">\s*(.*?)\s*</span>')
        match = pat.search(self.html)
        (text,) = match.groups()
        self.text = text

    def _set_star_rating(self):
        pat = re.compile(r'(\d).\d out of 5 stars')
        match = pat.search(self.html)
        stars = match.groups()[0]
        self.star_rating = int(stars)

    def _set_title(self):
        pat = re.compile(r'<span class="summary">\s*(.*?)\s*</span>')
        match = pat.search(self.html)
        self.title = match.groups()[0]

    def _set_helpfulness(self):
        pat = re.compile(r'(\d+) of (\d+) people found the following '
                          'review helpful')
        match = pat.search(self.html)
        pair = match.groups()
        helpful = int(pair[0])
        total = int(pair[1])
        self.helpfulness = (helpful, total)

    def _set_reviewer(self):
        pat = re.compile(r'<title>Amazon.com: (.*?)\'s? review of')
        match = pat.search(self.html)
        gr = match.groups()
        self.reviewer = str(gr[0])

    def _set_product_name(self):
        pat = re.compile(r'This review is from: </span>(.*?)\(.*?\)</b>')
        match = pat.search(self.html)
        self.product_name = match.groups()[0]

    #
    # Output methods
    #
    def __str__(self):
        return ''

    def to_xml(self):
        pass

    def to_xml_file(self, fname):
        pass

    def to_json_file(self, fname):
        pass

    def to_sqlite(self, fname):
        pass

    # end output methods

class Product(object):
    def __init__(self, url):
        self.product_url = url
        self.scrape_reviews()

    @staticmethod
    def _fetch_html(url):
        return urllib2.urlopen(url).read()


    def scrape_reviews(self):
        'Scrape the reviews for product at `url` and return a list of Reviews.'
        reviews = []
        for url in self._get_review_urls():
            reviews.append(Review(url))
        return reviews

    @staticmethod
    def _scrape_permalinks(html):
        'Return all the permalinks to reviews on this page.'
        #TODO
        return [47]

    @staticmethod
    def _get_link_to_next(html):
        'Return url of link to the next page of reviews or None.'
        #TODO
        return None


    def _get_review_urls(self):
        main_page_html = self._fetch_html(self.product_url)
        pat = re.compile(r'<a href="(.*?)" >\d+ customer reviews</a>')
        url = pat.search(main_page_html).groups()[0]

        # Loop until akdsjf;ajdfl
        permalinks = []
        while url:
            html = self._fetch_html(url)
            new_permalinks = self._scrape_permalinks(html)
            permalinks += new_permalinks
            url = self._get_link_to_next(html)
        return permalinks 


def test_product():
    url = sys.argv[1]
    product = ProductReviews(url)



def test_review():
    url = sys.argv[1]
    review = Review(url)
    print review.text
    print review.date
    print review.star_rating
    print review.title
    print review.helpfulness
    print review.reviewer
    print review.product_name


def f():
    import urllib2
    from BeautifulSoup import BeautifulSoup
    url = sys.argv[1]
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    print soup.html.title
    print soup.html.title.nextSibling



if __name__ == '__main__':
    test_product()












