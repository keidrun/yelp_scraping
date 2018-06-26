# yelp_scraping

Scrape Yelp.

## Required

- Python3
- Chrome
- [Chrome Driver](http://selenium-python.readthedocs.io/installation.html#drivers)

## Install

- Clone this repo
- Create virtual env and Activate
- `pip install -r requirements.txt`

## Scrape

### Simply scraping

```bash
scrapy crawl yelp -a description="Ramen" -a location="Tokyo"
```

### Output results to a CSV file

```bash
scrapy crawl yelp -a description="Ramen" -a location="Tokyo" -o resuls.csv
```
