# -*- coding": "utf-8 -*-
import scrapy
import time
from marriott.items import MarriottItem
from selenium import webdriver
from scrapy.selector import Selector

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MarriottSpiderSpider(scrapy.Spider):
    name = 'marriott_spider'
    allowed_domains = ['marriott.com']
    start_urls = ['http://marriott.com']

    search_url = 'https://www.marriott.com/search/submitSearch.mi'
    
    query_data = {
        "roomTypeCode": "",
        "recordsPerPage": "20",
        "autoSuggestItemType": "",
        "destinationAddress.types": "locality,political",
        "destinationAddress.latitude": "31.230416",
        "propertyCode": "",
        "destinationAddress.stateProvinceShort": "",
        "isInternalSearch": "true",
        "destinationAddress.cityPopulation": "",
        "vsInitialRequest": "false",
        "searchType": "InCity",
        "destinationAddress.locality": "",
        "showAddressPin": "",
        "destinationAddress.stateProvinceDisplayName": "",
        "destinationAddress.destinationPageDestinationAddress": "",
        "countryName": "China",
        "destinationAddress.stateProvince": "Shanghai",
        "searchRadius": "80467.2",
        "singleSearchAutoSuggest": "Unmatched",
        "destinationAddress.placeId": "ChIJMzz1sUBwsjURoWTDI5QSlQI",
        "airportName": "",
        "for-hotels-nearme": "Near",
        "suggestionsPropertyCode": "",
        "destinationAddress.country": "CN",
        "destinationAddress.name": "",
        "poiCity": "",
        "destinationAddress.countryShort": "",
        "poiName": "",
        "destinationAddress.address": "Shanghai, China",
        "search-countryRegion": "",
        "collapseAccordian": "is-hidden",
        "singleSearch": "true",
        "destinationAddress.cityPopulationDensity": "",
        "destinationAddress.secondaryText": "China",
        "destinationAddress.postalCode": "",
        "destinationAddress.city": "Shanghai",
        "destinationAddress.mainText": "Shanghai",
        "airportCode": "",
        "isTransient": "true",
        "destinationAddress.longitude": "121.473701",
        "initialRequest": "true",
        "destinationAddress.website": "https://maps.google.com/?q=Shanghai,+China&ftid=0x35b27040b1f53c33:0x295129423c364a1",
        "search-locality": "",
        "roomTypeCode": "",
        "propertyCode": "",
        "flexibleDateSearchRateDisplay": "false",
        "propertyName": "",
        "isSearch": "true",
        "marriottRewardsNumber": "",
        "isRateCalendar": "false",
        "incentiveType_Number": "",
        "incentiveType": "",
        "flexibleDateLowestRateMonth": "",
        "flexibleDateLowestRateDate": "",
        "isMultiRateSearch": "",
        "multiRateMaxCount": "",
        "multiRateCorpCodes": "",
        "useMultiRateRewardsPoints": "",
        "multiRateClusterCodes": "",
        "multiRateCorpCodesEntered": "",
        "lowestRegularRate": "",
        "js-location-nearme-values": "",
        "destinationAddress.destination": "Shanghai, China",
        "fromToDate": "",
        "fromToDate_submit": "11/11/2019",
        "fromDate": "11/10/2019",
        "toDate": "11/11/2019",
        "toDateDefaultFormat": "11/11/2019",
        "fromDateDefaultFormat": "11/10/2019",
        "flexibleDateSearch": "false",
        "t-start": "2019-11-10",
        "t-end": "2019-11-11",
        "lengthOfStay": "1",
        "roomCountBox": "1 Room",
        "roomCount": "1",
        "guestCountBox": "1 Adult Per Room",
        "numAdultsPerRoom": "1",
        "childrenCountBox": "0 Children Per Room",
        "childrenCount": "0",
        "childrenAges": "",
        "clusterCode": "",
        "corporateCode": "", 
    }
    
    def __init__(self):
        self.webdriver = webdriver.Chrome("../chromedriver")
        #self.webdriver = webdriver.Firefox("../geckodriver")

    def start_requests(self):
        yield scrapy.FormRequest(url=self.search_url, method='GET', formdata=self.query_data, callback=self.parse)

    def parse(self, response):
        # url is generated in scrapy.FromRequest
        # use selenium to re-scrap it
        self.webdriver.get(response.url)

        time.sleep(30)

        WebDriverWait(self.webdriver, 120).until(
            EC.presence_of_element_located((By.XPATH, '//span[@class="l-property-name"]'))
        )

        sel = Selector(text=self.webdriver.page_source)
        sel_hotels = sel.xpath('//div[contains(@class,"property-record-item")]')

        for hotel in sel_hotels:
            hotel_item = MarriottItem()
            hotel_item['name'] = hotel.xpath('.//span[@class="l-property-name"]/text()').extract_first()
            hotel_item['price'] = hotel.xpath('.//span[@class="t-price  m-display-block"]/text()').extract_first()
            
            yield hotel_item

    def closed(self, reason):
        self.webdriver.close()
