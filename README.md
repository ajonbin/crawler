

## I Can Read ##

Get list of ICanRead Level

~~~

Crawler $ source ~/.pyvenv/crawler/bin/activate

(crawler) Crawler $ scrapy startproject icanread
New Scrapy project 'icanread', using template directory '/Users//.pyvenv/crawler/lib/python3.7/site-packages/scrapy/templates/project', created in:
    /Users//Crawler/icanread

You can start your first spider with:
    cd icanread
    scrapy genspider example example.com
(crawler) Crawler $ cd icanread/
(crawler) icanread $ scrapy genspider icanread_spider icanread.com
Created spider 'icanread_spider' using template 'basic' in module:
  icanread.spiders.icanread_spider
(crawler) icanread $ 
(crawler) icanread $ scrapy crawl icanread_spider -o books.csv


~~~
