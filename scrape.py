#!/usr/bin/env python

"""
Script to scrape Amazon product reviews.

Colin Pollock, pollockcolin@gmail.com

Example Usage
Creating a Review using the URL of an individual Amazon review.
>>> url = 'http://www.amazon.com/review/R219IF7JSF8OVB/'
>>> review = Review(url)
>>> print review.title, review.product_name, review.text, review.star_rating
>>> print review.date, review.reviewer, review.helpfulness

Creating a list of Reviews using the URL of the main page of a product.
>>> url = 'http://www.amazon.com/Cryptonomicon-Neal-Stephenson/dp/0060512806/'
>>> product = Product(url)
>>> for review in product.reviews:
>>>     print(review.text)
"""


try:
    import simplejson as json
except ImportError:
    import json
from optparse import OptionParser
import re
import sys
import textwrap
from urllib import urlopen


class Review(object):

    """Container for attributes and text of an Amazon product review.

    Attributes:
        title        -- the reviewer's title of the review
        product_name -- full name of product according to Amazon
        text         -- the actual review of the product
        star_rating  -- 0, 1, 2, 3, 4, or 5
        date         -- date the review was left
        reviewer     -- Amazon user name of reviewer
        helpfulness  -- pair (number of people who found the review helpful,
                        total number of people who responded)
    """

    def __init__(self, url):
        """Initialize fields of Amazon review by scraping site at `url`."""
        self.url = url
        self.html = self._get_html()

        self.title = self._get_title()
        self.product_name = self._get_product_name()
        self.text = self._get_text()
        self.date = self._get_date()
        self.star_rating = self._get_star_rating()
        self.helpfulness = self._get_helpfulness()
        self.reviewer = self._get_reviewer()

    def _get_html(self):
        """Return html found at self.url."""
        page = urlopen(self.url)
        return page.read().decode('iso-8859-1')


    #
    # HTML scraping methods.
    #
    def _get_date(self):
        """Return the date the review was left."""
        pat = re.compile(r"""<nobr>(.*?)</nobr>""")
        match = pat.search(self.html)
        if not match:
            raise ReviewScrapingFailure('Could not find date.', self)
        (date,) = match.groups()
        return date

    def _get_text(self):
        """Return the text of the review."""
        pat = re.compile(r"""<span[ ]class="description">
                          \s*
                          (.*?)
                          \s*
                          </span>""", re.VERBOSE)
        match = pat.search(self.html)
        if not match:
            raise ReviewScrapingFailure('Could not find review text.', self)
        (text,) = match.groups()
        return text

    def _get_star_rating(self):
        """Return the reviewer's star rating of the product."""
        pat = re.compile(r'(\d).\d out of 5 stars')
        match = pat.search(self.html)
        if not match:
            raise ReviewScrapingFailure('Could not find star rating.', self)
        stars = match.groups()[0]
        return int(stars)

    def _get_title(self):
        """Return the review's title."""
        pat = re.compile(r"""<span[ ]class="summary">
                          \s*
                          (.*?)
                          \s*
                          </span>
                          """, re.VERBOSE)
        match = pat.search(self.html)
        if not match:
            raise ReviewScrapingFailure('Could not find the title.', self)
        return match.groups()[0]

    def _get_helpfulness(self):
        """Return the helpfulness rating of the review.
       
        The first item of the tuple is the number of people who found the
        review to be helpful. The second is the total number of people
        who rated the review's helpfulness.
        """
        pat = re.compile(r'(\d+) of (\d+) people found the following '
                          'review helpful')
        match = pat.search(self.html)
        if not match:
            return 0, 0
            #TODO: See if there's any indication in the HTML that there have
            # been 0 helpfulness ratings. Raise an exception if there have 
            # been and match is None.

        pair = match.groups()
        helpful = int(pair[0])
        total = int(pair[1])
        return helpful, total

    def _get_reviewer(self):
        """Return the reviewer's Amazon ID."""
        # beautifulsoup would be cleaner here.
        name_pat = re.compile(r"<title>Amazon.com: (.*?)'s? review of", re.UNICODE)
        match = name_pat.search(self.html)
        if not match:
            raise ReviewScrapingFailure('Could not find reviewer name.', self)
        group = match.groups()
        return group[0]

    def _get_product_name(self):
        """Return the name of the product."""
        pat = re.compile(r"""This[ ]review[ ]is[ ]from:[ ]
                          </span>
                          (.*?)
                          \(.*?\)
                          </b>""", re.VERBOSE)
        match = pat.search(self.html)
        if not match:
            raise ReviewScrapingFailure('Could not find product name.', self)
        name = match.groups()[0]
        return name.strip()

    #
    # Output methods
    #
    def __str__(self):
        """Return the field-value pairs for the review."""
        fields = self._make_fields_dict()
        strings = []
        for attr, value in fields.items():
            strings.append(attr.title().rjust(20, '*') + '*' * 10)
            strings.append('\n'.join(textwrap.wrap(unicode(value), 70)))
            strings.append('')  # For extra newline between fields.
        return '\n'.join(strings).encode('utf-8')

    def to_json(self):
        """Return a json string made from a dict of the review fields."""
        return json.dumps(self._make_fields_dict(), indent=3)

    def _make_fields_dict(self):
        """Return a dictionary from the review's attributes to their values."""
        return dict(url=self.url, text=self.text, date=self.date, 
                    reviewer=self.reviewer, title=self.title, 
                    star_rating=self.star_rating, 
                    product_name=self.product_name)


class Product(object):

    """Primarily a container for Review objects.

    `reviews` is a list of Reviews.
    `scrape_reviews  is called in __init__ and populates `reviews`.
    """

    def __init__(self, url):
        """Scrape the reviews for the product at `url` and store results.
       
        `url` needs to be the URL of the main page of a product on Amazon. 
        """
        self.product_url = url
        self.reviews = self.scrape_reviews()

    @staticmethod
    def _fetch_html(url):
        """Return the HTML at `url`."""
        return urlopen(url).read().decode('iso-8859-1')

    def scrape_reviews(self):
        'Scrape the reviews for product at `url` and return a list of Reviews.'
        reviews = []
        urls = self._get_review_urls()
        count = len(urls)
        for i, url in enumerate(urls):
            print >> sys.stderr, "Scraping review %d of %d." % (i + 1, count)
            reviews.append(Review(url))
        return reviews

    @staticmethod
    def _scrape_permalinks(html):
        """Return all the permalinks to reviews on this page."""
        pat = re.compile(r'<a href="(.*?)" >Permalink</a>')
        permalinks = pat.findall(html)
        return permalinks

    @staticmethod
    def _get_link_to_next(html):
        'Return url of link to the next page of reviews or None if on last.'
        next_pat = re.compile('<a href="(((?!\|).)*)" >Next &rsaquo;</a>')
        match = next_pat.search(html)
        if match:
            return match.groups()[0]
        else:
            return None

    def _get_review_urls(self):
        """Returns the URLs of each review of the product."""
        main_page_html = self._fetch_html(self.product_url)
        pat = re.compile(r'<a href="(.*?)" >'
                          'See all \d+ customer reviews...</a>')
        match = pat.search(main_page_html)
        url = match.groups()[0]

        permalinks = []
        i = 1
        while url:
            print >> sys.stderr, 'Getting permalinks from review page %d.' % i 
            i += 1
            html = self._fetch_html(url)
            new_permalinks = self._scrape_permalinks(html)
            permalinks += new_permalinks
            url = self._get_link_to_next(html)
        return permalinks 

    def __str__(self):
        """Return each Review as a string, separated by a newline."""
        return '\n'.join([str(rev) for rev in self.reviews])

    def to_json(self):
        """Return a json string representing all the Reviews in a list."""
        reviews = [str(rev) for rev in self.reviews]
        return json.dumps(reviews, indent=3)


class ScrapingFailure(Exception): 
    """Base failure for failed attempts to scrape something from a page."""
    pass

class ReviewScrapingFailure(ScrapingFailure):
    def __init__(self, msg, review_obj):
        self.msg = msg
        self.title = review_obj.title
        self.url = review_obj.url

    def __str__(self):
        return "%s (Review title = '%s' and url = '%s')" \
                % (self.msg, self.title, self.url)

# Not used yet-- not making sure URL is right
#class ScrapeError(Exception): pass
#class NotReviewURLError(ScrapeError): pass
#class NotProductURLError(ScrapeError): pass


def main(argv=None):
    """This program can be used to scrape data from Amazon product
    reviews. The default behavior is to process the command line 
    arguments as URLs of Amazon products. In this case, the script
    scrapes each of the reviews for the product. If the -r (--review) 
    option is used, the arguments are treated as URLs of individual 
    reviews."""
    if argv is None:
        argv = sys.argv[1:]

    parser = OptionParser(description=re.sub('\s+', ' ', main.__doc__))
    parser.add_option('-r', '--review', dest='is_review', default=False,
                      action='store_true',
                      help='The arguments passed in are treated as URLs '
                      'of individual reviews rather than products.')

    parser.add_option('-o', '--outfile', action='store', default='-',
                      metavar='<FILENAME>',
                      help='Filename of output. Defaults to stdout (-).')

    parser.add_option('-f', '--format', action='store', default='string',
                      metavar='<FORMAT>', dest='the_format',
                      help='Format of output. Either "string" or "json". '
                      'Default is string.')
    options, args = parser.parse_args(argv)

    if options.the_format not in ('string', 'json'):
        parser.error("Argument of option --format must be 'string' or 'json'")

    if options.outfile == '-':
        out = sys.stdout
    else:
        out = open(options.outfile, 'w')

    # Process arguments either as Reviews or Products.
    results = []
    if options.is_review:
        for url in args:
            results.append(Review(url))
    else:
        for url in args:
            results.append(Product(url))

    # Print out scraped information formatted as json or as default string.
    for result in results:
        if options.the_format == 'string':
            print >> out, result
        elif options.the_format == 'json':
            print >> out, result.to_json()

    return 0


if __name__ == '__main__':
    exit(main())

