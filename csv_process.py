
import pandas as pd

class CSVProcessor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def _count_rows(self, df):
        return len(df.index)

    def process_csv(self):
        df = pd.read_csv(self.input_file, on_bad_lines='skip')
        total_rows = self._count_rows(df)

        df['Download Link'] = df['Link/DOI'].apply(self._generate_download_link)
        df.drop('Abstract', axis=1, inplace=True)
        df.to_csv(self.output_file, index=False)

    def _generate_download_link(self, link):
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

    input_file = '/Users/gatilin/PycharmProjects/chinaarxiv_mnbvc/myproject/results/medrxiv_results.csv'
    output_file = '/Users/gatilin/PycharmProjects/chinaarxiv_mnbvc/download/medrxiv_download.csv'
    processor = CSVProcessor(input_file, output_file)
    processor.process_csv()

    # input_file = '/Users/gatilin/PycharmProjects/chinaarxiv_mnbvc/myproject/results/psyarxiv_results.csv'
    # output_file = '/Users/gatilin/PycharmProjects/chinaarxiv_mnbvc/download/psyarxiv_download.csv'

    # 128606
    # input_file = '/Users/gatilin/PycharmProjects/chinaarxiv_mnbvc/myproject/results/biorxiv_results.csv'
    # output_file = '/Users/gatilin/PycharmProjects/chinaarxiv_mnbvc/download/biorxiv_download.csv'

    input_file = '/Users/gatilin/PycharmProjects/chinaarxiv_mnbvc/myproject/results/chemrxiv_results.csv'
    output_file = '/Users/gatilin/PycharmProjects/chinaarxiv_mnbvc/download/chemrxiv_download.csv'
    processor = CSVProcessor(input_file, output_file)
    processor.process_csv()