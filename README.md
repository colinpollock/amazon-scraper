Amazon Scraper
==============

About
-----
scrape.py can be used to scrape data from Amazon product reviews. It's extremely
brittle since it uses regular expressions to search the HTML of product and
review pages. If Amazon were to make small changes to how they render pages then
this script would probably break. Also, I wouldn't be surprised if Amazon
discouraged scraping their reviews. There are a few APIs out there that I didn't
know about when I first wrote this.


Usage
-----
The default behavior is to process the command line arguments as URLs of Amazon 
products. In this case, the script scrapes each of the reviews for the product. 
If the -r (--review) option is used, the arguments are treated as URLs of 
individual reviews. 

The scraped information from each review can be rendered as text or json.

Scraped information for each review includes:
* Reviewer's Amazon ID
* Review title
* Text of review
* Product name
* Star rating
* Date of review
* Helpfulness of the review, which is a pair (# voted helpful, total votes)


TODO
----
* Make Python3 branch.
* Add setup.py.
* Download Amazon pages to use as test data instead of relying on web pages.
