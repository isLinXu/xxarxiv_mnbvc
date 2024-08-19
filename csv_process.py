# import csv
# from tqdm import tqdm
#
# class CSVProcessor:
#     def __init__(self, input_file, output_file):
#         self.input_file = input_file
#         self.output_file = output_file
#
#     def _count_rows(self):
#         with open(self.input_file, 'r') as csvfile:
#             reader = csv.reader(csvfile)
#             return sum(1 for _ in reader) - 1
#
#     def process_csv(self):
#         with open(self.input_file, 'r') as csvfile:
#             reader = csv.DictReader(csvfile)
#             fieldnames = reader.fieldnames
#             fieldnames.remove('Abstract')
#             fieldnames.append('Download Link')
#
#             # with open(self.output_file, 'w') as output_csvfile:
#             #     writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
#             #     writer.writeheader()
#             #
#             #     total_rows = self._count_rows()
#             #     for row in tqdm(reader, total=total_rows, desc="Processing rows"):
#             #         link = row['Link/DOI'].replace('https://doi.org/', 'https://osf.io/')
#             #         download_link = f'{link}download/'
#             #         row['Download Link'] = download_link
#             #         row.pop('Abstract', None)
#             #         writer.writerow(row)
#             with open(self.output_file, 'w') as output_csvfile:
#                 writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
#                 writer.writeheader()
#
#                 total_rows = self._count_rows()
#                 for row in tqdm(reader, total=total_rows, desc="Processing rows"):
#                     link = row['Link/DOI'].replace('https://doi.org/', '')
#                     download_link = f'https://osf.io/{link}/download/'
#                     row['Download Link'] = download_link
#                     row.pop('Abstract', None)
#                     writer.writerow(row)

# class CSVProcessor:
#     def __init__(self, input_file, output_file):
#         self.input_file = input_file
#         self.output_file = output_file
#
#     def _count_rows(self):
#         with open(self.input_file, 'r') as csvfile:
#             reader = csv.reader(csvfile)
#             return sum(1 for _ in reader) - 1
#
#     def process_csv(self):
#         with open(self.input_file, 'r') as csvfile:
#             reader = csv.DictReader(csvfile)
#             fieldnames = reader.fieldnames
#             fieldnames.remove('Abstract')
#             fieldnames.append('Download Link')
#
#             with open(self.output_file, 'w') as output_csvfile:
#                 writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
#                 writer.writeheader()
#
#                 total_rows = self._count_rows()
#                 for row in tqdm(reader, total=total_rows, desc="Processing rows"):
#                     link = row['Link/DOI'].replace('https://doi.org/', 'https://osf.io/')
#                     download_link = f'{link}download/'
#                     row['Download Link'] = download_link
#                     del row['Abstract']
#                     writer.writerow(row)


# import csv
# from tqdm import tqdm
#
# class CSVProcessor:
#     def __init__(self, input_file, output_file):
#         self.input_file = input_file
#         self.output_file = output_file
#
#     def _count_rows(self):
#         with open(self.input_file, 'r') as csvfile:
#             reader = csv.reader(csvfile)
#             return sum(1 for _ in reader) - 1
#
#     def process_csv(self):
#         with open(self.input_file, 'r') as csvfile:
#             reader = csv.DictReader(csvfile)
#             fieldnames = reader.fieldnames
#             fieldnames.remove('Abstract')
#             fieldnames.append('Download Link')
#
#             with open(self.output_file, 'w') as output_csvfile:
#                 writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
#                 writer.writeheader()
#
#                 total_rows = self._count_rows()
#                 for row in tqdm(reader, total=total_rows, desc="Processing rows"):
#                     link = row['Link/DOI'].split('/')[-1]
#                     download_link = f'https://osf.io/{link}/download/'
#                     row['Download Link'] = download_link
#                     row.pop('Abstract', None)
#                     writer.writerow(row)

import csv
from tqdm import tqdm
# class CSVProcessor:
#     def __init__(self, input_file, output_file):
#         self.input_file = input_file
#         self.output_file = output_file
#
#     def _count_rows(self):
#         with open(self.input_file, 'r') as csvfile:
#             reader = csv.reader(csvfile)
#             return sum(1 for _ in reader) - 1
#
#     def process_csv(self):
#         with open(self.input_file, 'r') as csvfile:
#             reader = csv.DictReader(csvfile)
#             fieldnames = reader.fieldnames
#             fieldnames.remove('Abstract')
#             fieldnames.append('Download Link')
#
#             with open(self.output_file, 'w') as output_csvfile:
#                 writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
#                 writer.writeheader()
#
#                 total_rows = self._count_rows()
#                 for row in tqdm(reader, total=total_rows, desc="Processing rows"):
#                     link = row['Link/DOI'].replace('https://doi.org/', '')
#                     if '10.31234/osf.io' in link:
#                         download_link = f'https://osf.io/{link.split("/")[-1]}/download/'
#                     else:
#                         download_link = f'https://www.biorxiv.org/content/{link}v1.full.pdf'
#                     row['Download Link'] = download_link
#                     row.pop('Abstract', None)
#                     writer.writerow(row)
#

# class CSVProcessor:
#     def __init__(self, input_file, output_file):
#         self.input_file = input_file
#         self.output_file = output_file
#
#     def _count_rows(self):
#         with open(self.input_file, 'r', errors='ignore') as csvfile:
#             reader = csv.reader(csvfile)
#             return sum(1 for _ in reader) - 1
#
#     def process_csv(self):
#         with open(self.input_file, 'r', errors='ignore') as csvfile:
#             reader = csv.DictReader(csvfile)
#             fieldnames = reader.fieldnames
#             fieldnames.remove('Abstract')
#             fieldnames.append('Download Link')
#
#             with open(self.output_file, 'w') as output_csvfile:
#                 writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
#                 writer.writeheader()
#
#                 total_rows = self._count_rows()
#                 for row in tqdm(reader, total=total_rows, desc="Processing rows"):
#                     link = row['Link/DOI'].replace('https://doi.org/', '')
#                     if '10.31234/osf.io' in link:
#                         download_link = f'https://osf.io/{link.split("/")[-1]}/download/'
#                     elif '10.26434/chemrxiv' in link:
#                         download_link = f'https://osf.io/{link.split("-")[-1]}/download/'
#                     else:
#                         download_link = f'https://www.biorxiv.org/content/{link}v1.full.pdf'
#                     row['Download Link'] = download_link
#                     row.pop('Abstract', None)
#                     writer.writerow(row)

# class CSVProcessor:
#     def __init__(self, input_file, output_file):
#         self.input_file = input_file
#         self.output_file = output_file
#
#     def _count_rows(self):
#         with open(self.input_file, 'r') as csvfile:
#             reader = csv.reader(csvfile)
#             return sum(1 for _ in reader) - 1
#
#     def process_csv(self):
#         with open(self.input_file, 'r') as csvfile:
#             reader = csv.DictReader(csvfile)
#             fieldnames = reader.fieldnames
#             fieldnames.remove('Abstract')
#             fieldnames.append('Download Link')
#
#             with open(self.output_file, 'w') as output_csvfile:
#                 writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
#                 writer.writeheader()
#
#                 total_rows = self._count_rows()
#                 for row in tqdm(reader, total=total_rows, desc="Processing rows"):
#                     link = row['Link/DOI'].replace('https://doi.org/', '')
#                     if '10.31234/osf.io' in link:
#                         download_link = f'https://osf.io/{link.split("/")[-1]}/download/'
#                     elif '10.26434/chemrxiv' in link:
#                         download_link = f'https://osf.io/{link.split("-")[-1]}/download/'
#                     else:
#                         download_link = f'https://www.biorxiv.org/content/{link}v1.full.pdf'
#                     row['Download Link'] = download_link
#                     row.pop('Abstract', None)
#                     writer.writerow(row)

# import csv
# from tqdm import tqdm
#
# class CSVProcessor:
#     def __init__(self, input_file, output_file):
#         self.input_file = input_file
#         self.output_file = output_file
#
#     def _count_rows(self):
#         with open(self.input_file, 'rb') as csvfile:
#             reader = csv.reader((line.decode('utf-8', 'ignore') for line in csvfile))
#             return sum(1 for _ in reader) - 1
#
#     def process_csv(self):
#         with open(self.input_file, 'rb') as csvfile:
#             reader = csv.DictReader((line.decode('utf-8', 'ignore') for line in csvfile))
#             fieldnames = reader.fieldnames
#             fieldnames.remove('Abstract')
#             fieldnames.append('Download Link')
#
#             with open(self.output_file, 'w') as output_csvfile:
#                 writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
#                 writer.writeheader()
#
#                 total_rows = self._count_rows()
#                 for row in tqdm(reader, total=total_rows, desc="Processing rows"):
#                     link = row['Link/DOI'].replace('https://doi.org/', '')
#                     if '10.31234/osf.io' in link:
#                         download_link = f'https://osf.io/{link.split("/")[-1]}/download/'
#                     elif '10.26434/chemrxiv' in link:
#                         download_link = f'https://osf.io/{link.split("-")[-1]}/download/'
#                     else:
#                         download_link = f'https://www.biorxiv.org/content/{link}v1.full.pdf'
#                     row['Download Link'] = download_link
#                     row.pop('Abstract', None)
#                     writer.writerow(row)



# import pandas as pd
# from tqdm import tqdm
#
# class CSVProcessor:
#     def __init__(self, input_file, output_file):
#         self.input_file = input_file
#         self.output_file = output_file
#
#     def _count_rows(self, df):
#         return len(df.index)
#
#     def process_csv(self):
#         df = pd.read_csv(self.input_file, error_bad_lines=False)
#         total_rows = self._count_rows(df)
#
#         df['Download Link'] = df['Link/DOI'].apply(self._generate_download_link)
#         df.drop('Abstract', axis=1, inplace=True)
#         df.to_csv(self.output_file, index=False)
#
#     def _generate_download_link(self, link):
#         link = link.replace('https://doi.org/', '')
#         if '10.31234/osf.io' in link:
#             return f'https://osf.io/{link.split("/")[-1]}/download/'
#         elif '10.26434/chemrxiv' in link:
#             return f'https://osf.io/{link.split("-")[-1]}/download/'
#         else:
#             return f'https://www.biorxiv.org/content/{link}v1.full.pdf'
#

# import pandas as pd
# from tqdm import tqdm
#
# class CSVProcessor:
#     def __init__(self, input_file, output_file):
#         self.input_file = input_file
#         self.output_file = output_file
#
#     def _count_rows(self, df):
#         return len(df.index)
#
#     def process_csv(self):
#         df = pd.read_csv(self.input_file, on_bad_lines='skip')
#         total_rows = self._count_rows(df)
#
#         df['Download Link'] = df['Link/DOI'].apply(self._generate_download_link)
#         df.drop('Abstract', axis=1, inplace=True)
#         df.to_csv(self.output_file, index=False)
#
#     def _generate_download_link(self, link):
#         link = link.replace('https://doi.org/', '')
#         if '10.31234/osf.io' in link:
#             return f'https://osf.io/{link.split("/")[-1]}/download/'
#         elif '10.26434/chemrxiv' in link:
#             return f'https://osf.io/{link.split("-")[-1]}/download/'
#         else:
#             return f'https://www.biorxiv.org/content/{link}v1.full.pdf'


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
# https://osf.io/jrm9e/download/
# https://osf.io/jrm9e/download/
processor = CSVProcessor(input_file, output_file)
processor.process_csv()