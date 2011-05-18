#!/usr/bin/env python

"""Tests for Review and Product in scrape

TODO:
  Add tests for Product with no reviews.
  Add test for review with anonymous author.

  Make a mock set of .html files with Amazon links replaced with links to
  local files.

"""

import os
from os import path
import unittest

import scrape

class TestGoodReview(unittest.TestCase):
    """Test NLTK review with all information present."""

    def setUp(self):
        """Create Review for test_data/nltk_review_sara_kazemia.html."""
        #TODO: use path.join; better way to open local files using urllib?
        cwd = os.getcwd()
        the_path = 'file://' + cwd + '/test_data/nltk_review_sara_kazemi.html'
        self.review = scrape.Review(the_path)


    def test_title(self):
        correct = 'A great resource for computational linguistics and NLP'
        self.assertEqual(self.review.title, correct)

    def test_product_name(self):
        correct = 'Natural Language Processing with Python'
        self.assertEqual(self.review.product_name, correct)

    def test_star_rating(self):
        correct = 4
        self.assertEqual(self.review.star_rating, correct)

    def test_date(self):
        correct = 'February 8, 2010'
        self.assertEqual(self.review.date, correct)

    def test_reviewer(self):
        correct = 'Sara Kazemi "Sarie"'
        self.assertEqual(self.review.reviewer, correct)

    def test_helpfulness(self):
        correct = (1, 2)
        self.assertEqual(self.review.helpfulness, correct)

    def test_text(self):
        correct = """If you already know how to program in Python and are doing NLP projects, this book is very helpful. If you are looking to learn Python so that you can do NLP projects, you will need to first learn Python elsewhere before this resource will become useful. Example code is abundant and is well explained."""
        self.assertEqual(self.review.text, correct)


class TestProduct(unittest.TestCase):

    """Test the main method of Product. Uses rest of helper methods.
        
    TODO
    This test needs to be reworked later. Currently a Product object is created
    using information scraped from the web. The "url" passed to Product
    contains links to real Amazon pages. So, I need to replace all the URLs on
    the pages with links to local files. 
    
    The test is currently very slow since it scrapes the real web so I'm only
    running one test so that the slow __init__ isn't run repeatedly.
    """

    def setUp(self):
        cwd = os.getcwd()
        the_path = 'file://' + cwd + '/test_data/nltk_main.html'
        self.product = scrape.Product(the_path)

    def test_number(self):
        self.assertEqual(len(self.product.reviews), 13)


class TestProductStatics(unittest.TestCase):
    def setUp(self):
        cwd = os.getcwd()
        main_path = path.join(cwd, 'test_data', 'nltk_main.html')
        with open(main_path, 'r') as f:
            self.main_html = f.read()

        page1_path = path.join(cwd, 'test_data', 'nltk_reviews_page_1.html')
        with open(page1_path, 'r') as f:
            self.page1_html = f.read()

        page2_path = path.join(cwd, 'test_data', 'nltk_reviews_page_2.html')
        with open(page2_path, 'r') as f:
            self.page2_html = f.read()

    def test__scrape_permalinks(self):
        found = scrape.Product._scrape_permalinks(self.page1_html)
        correct = ["""http://www.amazon.com/review/R1HV36NPN7MCIS/ref=cm_cr_pr_perm?ie=UTF8&ASIN=0596516495&nodeID=&tag=&linkCode=""", 
                   """http://www.amazon.com/review/R1HAP7CV5AP8ZN/ref=cm_cr_pr_perm?ie=UTF8&ASIN=0596516495&nodeID=&tag=&linkCode=""", 
                   """http://www.amazon.com/review/R8QHGZ36Q8D50/ref=cm_cr_pr_perm?ie=UTF8&ASIN=0596516495&nodeID=&tag=&linkCode=""", 
                   """http://www.amazon.com/review/R38V0H4A79LEQ0/ref=cm_cr_pr_perm?ie=UTF8&ASIN=0596516495&nodeID=&tag=&linkCode=""", 
                   """http://www.amazon.com/review/R10B3M673LVF1F/ref=cm_cr_pr_perm?ie=UTF8&ASIN=0596516495&nodeID=&tag=&linkCode=""", 
                   """http://www.amazon.com/review/R3INYYU0KNUX1G/ref=cm_cr_pr_perm?ie=UTF8&ASIN=0596516495&nodeID=&tag=&linkCode=""",
                    """http://www.amazon.com/review/R3B6C3CENXKX4C/ref=cm_cr_pr_perm?ie=UTF8&ASIN=0596516495&nodeID=&tag=&linkCode=""",
                    """http://www.amazon.com/review/RHTF63JU9QV0O/ref=cm_cr_pr_perm?ie=UTF8&ASIN=0596516495&nodeID=&tag=&linkCode=""",
                    """http://www.amazon.com/review/R2M01NA001Q57U/ref=cm_cr_pr_perm?ie=UTF8&ASIN=0596516495&nodeID=&tag=&linkCode=""",
                    """http://www.amazon.com/review/RWUN3MGC1ZIPB/ref=cm_cr_pr_perm?ie=UTF8&ASIN=0596516495&nodeID=&tag=&linkCode="""]
        self.assertEqual(found, correct)
        
    def test__get_link_to_next(self):
        found = scrape.Product._get_link_to_next(self.page1_html)
        correct = "http://www.amazon.com/Natural-Language-Processing-Python-"                     "Steven/product-reviews/0596516495"

        # `correct` doesn't include the ref information in the URL, so only
        # match the beginning of `found`.
        self.assertTrue(found.startswith(correct))

    def test__get_link_to_next_None(self):
        found = scrape.Product._get_link_to_next(self.page2_html)
        correct = None
        self.assertEqual(found, correct)

    

if __name__ == '__main__':
    unittest.main()

