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

class ChemrxivSpider(scrapy.Spider):
    name = 'chemrxiv'
    allowed_domains = ['chemrxiv.org']
    # Get today's date in the format YYYY-MM-DD
    today = datetime.now().date().isoformat()
    # Set the start date to a very early date to get all records
    earliest_date = '1900-01-01'

    def __init__(self, server='chemrxiv', start_date=earliest_date, end_date=today, *args, **kwargs):
        super(ChemrxivSpider, self).__init__(*args, **kwargs)
        self.logger.setLevel(logging.INFO)
        (logging.DEBUG)
        self.server = server
        self.limit = 50
        self.skip = 0
        self.searchDateFrom = start_date
        self.searchDateTo = end_date
        self.file = open(f'results/{server}_results.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['Link/DOI', 'Publication Date', 'Title', 'Authors', 'Abstract'])
        self.total_preprints = 0  # Total number of preprints to process
        self.pbar = None  # Progress bar

    def start_requests(self):
        url = f'https://chemrxiv.org/engage/chemrxiv/public-api/v1/items?limit={self.limit}&searchDateFrom={self.searchDateFrom}&searchDateTo={self.searchDateTo}'
        yield scrapy.Request(url=url, method='GET', callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        itemHits = data.get('itemHits')

        # Initialize the progress bar if not already initialized
        if self.pbar is None:
            self.total_preprints = data.get('totalCount', len(itemHits))
            self.pbar = tqdm(total=self.total_preprints, desc="Processing preprints")

        if itemHits:
            for item in itemHits:
                article = item.get('item')
                loader = ItemLoader(item=PreprintItem(), selector=article)
                loader.default_output_processor = TakeFirst()

                authors = article.get('authors')
                authors_str = ', '.join([f"{author.get('firstName')} {author.get('lastName')}" for author in authors])

                loader.add_value('title', article.get('title', '').replace('\n', ' ').lower())
                loader.add_value('abstract', article.get('abstract', '').replace('\n', ' ').lower())
                loader.add_value('doi_link', "https://doi.org/" + article.get('doi', 'N/A'))
                loader.add_value('publication_date', article.get('publishedDate', '').split('T')[0])
                loader.add_value('authors', authors_str)

                item = loader.load_item()
                self.save_item(item)

                # Update the progress bar
                self.pbar.update(1)

        # Handling pagination
        self.skip += self.limit
        if self.skip < data.get('totalCount'):
            next_url = f'https://chemrxiv.org/engage/chemrxiv/public-api/v1/items?limit={self.limit}&searchDateFrom={self.searchDateFrom}&searchDateTo={self.searchDateTo}&skip={self.skip}'
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