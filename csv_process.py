import pandas as pd
import argparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class CSVProcessor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def _count_rows(self, df):
        """Count the number of rows in the DataFrame"""
        return len(df.index)

    def process_csv(self):
        """Process the CSV file"""
        try:
            df = pd.read_csv(self.input_file, on_bad_lines='skip')
            total_rows = self._count_rows(df)
            logging.info(f"Total rows in input file: {total_rows}")

            df['Download Link'] = df['Link/DOI'].apply(self._generate_download_link)
            df.drop('Abstract', axis=1, inplace=True)
            df.to_csv(self.output_file, index=False)
            logging.info(f"Processed CSV saved to: {self.output_file}")
        except Exception as e:
            logging.error(f"Error processing CSV file: {e}")

    def _generate_download_link(self, link):
        """Generate download link based on the DOI or link"""
        link = link.replace('https://doi.org/', '')
        if '10.31234/osf.io' in link:
            return f'https://osf.io/{link.split("/")[-1]}/download/'
        elif '10.26434/chemrxiv' in link:
            return f'https://osf.io/{link.split("-")[-1]}/download/'
        elif '10.1101' in link:
            return f'https://www.medrxiv.org/content/{link}v3.full.pdf'
        else:
            return f'https://www.biorxiv.org/content/{link}v1.full.pdf'


if __name__ == '__main__':
    # Use argparse to parse command line arguments
    parser = argparse.ArgumentParser(description="Process a CSV file to generate download links.")
    parser.add_argument('input_file', type=str, help="Path to the input CSV file.")
    parser.add_argument('output_file', type=str, help="Path to the output CSV file.")

    args = parser.parse_args()

    processor = CSVProcessor(args.input_file, args.output_file)
    processor.process_csv()

