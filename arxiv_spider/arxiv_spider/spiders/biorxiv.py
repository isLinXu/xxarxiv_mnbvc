import scrapy
import json
import csv
import logging
from datetime import datetime, timedelta
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join
from tqdm import tqdm


class PreprintItem(scrapy.Item):
    doi_link = scrapy.Field()
    publication_date = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    abstract = scrapy.Field()


class BiorxivSpider(scrapy.Spider):
    name = 'biorxiv'
    allowed_domains = ['api.biorxiv.org']
    # Get today's date in the format YYYY-MM-DD
    today = datetime.now().date().isoformat()
    # Get the date 3 months ago in the format YYYY-MM-DD
    three_months_ago = (datetime.now() - timedelta(days=90)).date().isoformat()
    # Set the start date to a very early date to get all records
    earliest_date = '1900-01-01'

    def __init__(self, server='biorxiv', start_date=earliest_date, end_date=today, *args, **kwargs):
        super(BiorxivSpider, self).__init__(*args, **kwargs)
        self.logger.setLevel(logging.DEBUG)
        self.server = server
        self.interval = f'{start_date}/{end_date}'
        self.cursor = 0
        self.file = open(f'results/{server}_results.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['Link/DOI', 'Publication Date', 'Title', 'Authors', 'Abstract'])
        self.total_preprints = 0  # Total number of preprints to process
        self.pbar = None  # Progress bar

    def start_requests(self):
        url = f'https://api.biorxiv.org/pubs/{self.server}/{self.interval}/{self.cursor}'
        yield scrapy.Request(url=url, method='GET', callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        articles = data.get('collection', [])

        # Initialize the progress bar if not already initialized
        if self.pbar is None:
            self.total_preprints = len(articles)
            self.pbar = tqdm(total=self.total_preprints, desc="Processing preprints")

        for article in articles:
            loader = ItemLoader(item=PreprintItem(), selector=article)
            loader.default_output_processor = TakeFirst()

            authors = article.get('preprint_authors', [])
            authors_str = ', '.join(authors)

            loader.add_value('title', article.get('preprint_title', '').replace('\n', ' ').lower())
            loader.add_value('abstract', article.get('preprint_abstract', '').replace('\n', ' ').lower())
            loader.add_value('doi_link', "https://doi.org/" + article.get('preprint_doi', 'N/A'))
            loader.add_value('publication_date', article.get('published_date', ''))
            loader.add_value('authors', authors_str)

            item = loader.load_item()
            self.save_item(item)

            # Update the progress bar
            self.pbar.update(1)

        # Handling pagination
        messages = data.get('messages', [])
        if messages:
            message = messages[0]
            count = message.get('count', 0)
            next_cursor = message.get('cursor', None)

            if next_cursor is not None:
                self.cursor = int(next_cursor) + count  # Ensure cursor is updated based on API response
                next_url = f'https://api.biorxiv.org/pubs/{self.server}/{self.interval}/{self.cursor}'
                yield scrapy.Request(url=next_url, callback=self.parse)

    def save_item(self, item):
        """
        Save the item to the CSV file.

        Args:
            item (PreprintItem): The item to save.
        """
        self.writer.writerow([
            item.get('doi_link', 'N/A'),
            item.get('publication_date', 'N/A'),
            item.get('title', 'N/A'),
            item.get('authors', 'N/A'),
            item.get('abstract', 'N/A')
        ])

    def close_spider(self, spider):
        """
        Close the CSV file and the progress bar when the spider is closed.

        Args:
            spider (scrapy.Spider): The spider instance that is being closed.
        """
        self.file.close()
        if self.pbar:
            self.pbar.close()