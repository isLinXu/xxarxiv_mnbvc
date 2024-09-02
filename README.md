# xxarxiv_mnbvc

# usage

## install

```
pip install -r requirements.txt
```



```
cd arxiv_spider
```

```
scrapy crawl psyarxiv
scrapy crawl chemrxiv
scrapy crawl biorxiv
scrapy crawl medrxiv
```




# transfer data

```shell
python process_csv.py /path/to/input_file.csv /path/to/output_file.csv
```

```shell
python process_csv.py ./results/psyarxiv_results.csv ./download/medrxiv_download.csv
```

```shell
python process_csv.py ./results/biorxiv_results.csv ./download/biorxiv_download.csv
```

```shell
python process_csv.py ./results/chemrxiv_results.csv ./download/chemrxiv_download.csv
```

```shell
python process_csv.py ./results/psyarxiv_results.csv ./download/psyarxiv_download.csv
```



# download data

```
python xxarxiv_download.py ./arxiv_download/medrxiv_download.csv medrxiv
```

```
python xxarxiv_download.py ./arxiv_download/biorxiv_download.csv biorxiv
```

```
python xxarxiv_download.py ./arxiv_download/chemrxiv_download.csv chemrxiv
```

```
python xxarxiv_download.py ./arxiv_download/psyarxiv_download.csv psyarxiv
```

