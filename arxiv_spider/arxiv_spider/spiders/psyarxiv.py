import scrapy
import json
import csv
import logging
from datetime import datetime, timedelta
from tqdm import tqdm


class PsyarxivSpider(scrapy.Spider):
    name = 'psyarxiv'
    allowed_domains = ['osf.io']
    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }

    # Get today's date in the format YYYY-MM-DD
    today = datetime.now().date().isoformat()

    # Get the date 1 month ago in the format YYYY-MM-DD
    # one_month_ago = (datetime.now() - timedelta(days=30)).date().isoformat()
    # Set the start date to a very early date to get all records
    earliest_date = '1900-01-01'

    def __init__(self, start_date=earliest_date, end_date=today, *args, **kwargs):
        """
        Initialize the spider with start and end dates for filtering the preprints.

        Args:
            start_date (str): The start date for filtering preprints.
            end_date (str): The end date for filtering preprints.
        """
        super(PsyarxivSpider, self).__init__(*args, **kwargs)
        self.logger.setLevel(logging.DEBUG)
        self.start_date = start_date
        self.end_date = end_date
        self.file = open(f'results/psyarxiv_results.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['Link/DOI', 'Publication Date', 'Title', 'Authors', 'Abstract'])
        self.headers = {
            'Accept': 'application/json',  # Indicates a preference for JSON
        }
        self.total_preprints = 0  # Total number of preprints to process
        self.pbar = None  # Progress bar

    def start_requests(self):
        """
        Start the initial request to fetch preprints from the API.
        """
        url = f'https://api.osf.io/v2/preprints/?filter[provider]=psyarxiv&filter[date_published][gte]={self.start_date}&filter[date_published][lte]={self.end_date}'
        yield scrapy.Request(url=url, headers=self.headers, method='GET', callback=self.parse)

    def parse(self, response):
        """
        Parse the response from the API to extract preprint information.

        Args:
            response (scrapy.http.Response): The response object from the API request.
        """
        try:
            data = json.loads(response.text)
            preprints = data.get('data', [])
            print("preprints:", preprints)
            # Initialize the progress bar if not already initialized
            if self.pbar is None:
                self.total_preprints = data.get('meta', {}).get('total', len(preprints))
                self.pbar = tqdm(total=self.total_preprints, desc="Processing preprints")

            for preprint in preprints:
                attributes = preprint.get('attributes', {})
                title = attributes.get('title', '').replace('\n', ' ')
                abstract = attributes.get('description', '').replace('\n', ' ')
                doi_link = preprint.get('links', {}).get('preprint_doi', 'N/A')
                publication_date = attributes.get('date_published', 'N/A').split('T')[0]
                authors_link = preprint.get('relationships', {}).get('contributors', {}).get('links', {}).get('related',{}).get('href', '')

                # Initially, authors are not fetched; set as a placeholder
                authors_str = "To be fetched"

                if doi_link != 'N/A':
                    self.writer.writerow([
                        doi_link,
                        publication_date,
                        title,
                        authors_str,
                        abstract
                    ])

                if authors_link:
                    # Yield a new request to fetch authors, passing current preprint info as meta
                    yield scrapy.Request(url=authors_link, headers=self.headers, method='GET',
                                         callback=self.parse_authors, meta={
                            'doi_link': doi_link,
                            'publication_date': publication_date,
                            'title': title,
                            'abstract': abstract
                        })

                # Update the progress bar
                self.pbar.update(1)

            # Handling pagination
            next_url = data.get('links', {}).get('next', None)
            if next_url:
                yield scrapy.Request(url=next_url, headers=self.headers, callback=self.parse)
        except json.JSONDecodeError:
            self.logger.error(
                f'Failed to decode JSON from response. Status: {response.status}, URL: {response.url}, Body: {response.text[:500]}')
            return

    def parse_authors(self, response):
        """
        Parse the response to extract author information and update the CSV file.
        Args:
                    response (scrapy.http.Response): The response object from the API request for authors.
                """
        data = json.loads(response.text)
        authors = data.get('data', [])
        authors_str = ', '.join(
            [author.get('embeds', {}).get('users', {}).get('data', {}).get('attributes', {}).get('full_name', 'N/A') for
             author in authors])

        # Append authors to the existing CSV row. This is a simplified approach;
        # for a more accurate handling, you might need to update the existing row or handle this data differently.
        self.writer.writerow([
            response.meta['doi_link'],
            response.meta['publication_date'],
            response.meta['title'],
            authors_str,
            response.meta['abstract']
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