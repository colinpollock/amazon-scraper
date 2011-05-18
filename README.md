README 
======
scrape.py can be used to scrape data from Amazon product reviews. The default
behavior is to process the command line arguments as URLs of Amazon products. In
this case, the script scrapes each of the reviews for the product. If the -r 
(--review) option is used, the arguments are treated as URLs of individual
reviews. 

The scraped information from each review can be rendered as text or json.

Scraped information for each review includes:
* Reviewer's Amazon ID
* Review title
* Text of review
* Product name
* Star rating
* Date of review
* Helpfulness of the review, which is a pair (# voted helpful, total votes)
