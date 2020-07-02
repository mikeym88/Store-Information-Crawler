# Store Info Web Crawler

This crawler fetches data from the websites of various chains in order to get information about their store locations.
Information such as store name, phone number, operating hours, etc.

This crawler was **last run successfully in June 2020**. The crawler would need to be tested and changed on a regular 
interval to make sure it still works.

See the `results` folder for the crawler output.

## Notes

* Either crawler 1 or 2 was not working because the `robots.txt` was being misread. While the website's `robots.txt` 
  allowed the specific URL to be accessed by crawlers, `scapy` did not read that correctly.
    * Workaround: set `ROBOTSTXT_OBEY` to `False` in `settings.py`
    * Further investigation needed. 

## Running the crawlers

Use the following commands to run the crawlers.

### Crawler 1:

Output as JSON file:
```
scrapy crawl towncaredental -o results/towncaredental.json
```

Output as CSV file:
```
scrapy crawl towncaredental -o results/towncaredental.csv -t csv
```

### Crawler 2

Output as JSON file:
```
scrapy crawl rickysalldaygrillcanada -o results/rickysalldaygrillcanada.json
```

Output as CSV file:
```
scrapy crawl rickysalldaygrillcanada -o results/rickysalldaygrillcanada.csv -t csv
```

### Crawler 3

Output as JSON file:
```
scrapy crawl jockey -o results/jockey.json
```

Output as CSV file:
```
scrapy crawl jockey -o results/jockey.csv -t csv
```


### Crawler 4

Output as JSON file:
```
scrapy crawl rentking -o results/rentking.json
```

Output as CSV file:
```
scrapy crawl rentking -o results/rentking.csv -t csv
```

### Crawler 5

* This crawler was created specifically to answer the StackOverflow.com question
"[Crawl table data without 'next button' with Scrapy](https://stackoverflow.com/questions/62669269/crawl-table-data-without-next-button-with-scrapy)".
* For help, I used the StackOverflow.com answer to the question 
"[Crawling through pages with PostBack data javascript Python Scrapy](https://stackoverflow.com/a/28976674/6288413)".

Output as JSON file:
```
scrapy crawl uae_free -o results/uae_free.json
```

Output as CSV file:
```
scrapy crawl uae_free -o results/uae_free.csv -t csv
```

## Resources

1.	ScraPy module for Python: <https://docs.scrapy.org/en/latest/>. Quick start-to-finish example: <https://www.codementor.io/andy995/writing-a-simple-web-scraper-using-scrapy-myb7vrmgx>
2.	XPath syntax: <https://devhints.io/xpath>. Use Google Chrome Inspector (Dev tools) to test XPath to access HTML nodes of a website; example: <https://yizeng.me/2014/03/23/evaluate-and-validate-xpath-css-selectors-in-chrome-developer-tools/>
3.	Network Log details/demo: <https://developers.google.com/web/tools/chrome-devtools/network/>
