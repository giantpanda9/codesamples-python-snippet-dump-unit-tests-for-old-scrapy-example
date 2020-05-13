#!/usr/bin/python
# -*- coding: utf-8 -*-
# Scrapy spider/scrapper to fetch and parse the first page available by this link - https://efile.fara.gov/pls/apex/f?p=185:130:0::NO:RP,130:P130_DATERANGE:N
# As per my instructions only first 15 participants, available on the aforementioned page are requried
# Author: Nikolay Chegodaev as part of GP Application Submission Test
import scrapy
import datetime
from urlparse import urljoin
from hashlib import md5
import urllib2
from cookielib import CookieJar
from scrapy.http import HtmlResponse

class FaragovfirstpageSpiderSpider(scrapy.Spider):
	name = 'faragovfirstpage_spider'
	allowed_domains = ['efile.fara.gov']
	start_urls = ['https://efile.fara.gov/pls/apex/f?p=185:130:0::NO:RP,130:P130_DATERANGE:N']

	def parse(self, response):
		per_page_countries_counter = 1
		scrapypath = scrapy.Selector(response)
		selectedclass = scrapypath.xpath('//td[@headers="FP_NAME BREAK_COUNTRY_NAME_1"]/text()').extract()
		baseurl = "https://efile.fara.gov/pls/apex/"
		country_structure = scrapypath.xpath("//*[contains(@id, 'BREAK_COUNTRY_NAME_')]//span[@class='apex_break_headers']/text()").extract();
		for country in country_structure:			
			state_array = [e.xpath('string()').extract()[0] for e in scrapypath.xpath("//td[@headers='STATE BREAK_COUNTRY_NAME_" + str(per_page_countries_counter) + "']")]
			reg_num_array = [e.xpath('string()').extract()[0] for e in scrapypath.xpath("//td[@headers='REG_NUMBER BREAK_COUNTRY_NAME_" + str(per_page_countries_counter) + "']")]
			address_array = [e.xpath('string()').extract()[0] for e in scrapypath.xpath("//td[@headers='ADDRESS_1 BREAK_COUNTRY_NAME_" + str(per_page_countries_counter) + "']")]
			foreign_principal_array = [e.xpath('string()').extract()[0] for e in scrapypath.xpath("//td[@headers='FP_NAME BREAK_COUNTRY_NAME_" + str(per_page_countries_counter) + "']")]
			date_array = [e.xpath('string()').extract()[0] for e in scrapypath.xpath("//td[@headers='FP_REG_DATE BREAK_COUNTRY_NAME_" + str(per_page_countries_counter) + "']")]
			registrant_array = [e.xpath('string()').extract()[0] for e in scrapypath.xpath("//td[@headers='REGISTRANT_NAME BREAK_COUNTRY_NAME_" + str(per_page_countries_counter) + "']")]
			#creating links structure would be a little trickier
			links_structure = scrapypath.xpath("//td[@headers='LINK BREAK_COUNTRY_NAME_" + str(per_page_countries_counter) + "']/a")
			links_array = []			
			for link in links_structure:
				singleurl = link.css('a ::attr("href")').extract()[0]
				links_array.append(singleurl)
			pdflinks = self.parse_pdf(baseurl, links_array) # Need scrapy to get the links and return them back in synchronous way to avoid data sctructure damage
			per_country_principal_counter = 0
			for foreign_principal in foreign_principal_array:
				singlelink = links_array[per_country_principal_counter]
				urlmark = md5(str(urljoin(baseurl, singlelink))).hexdigest()
				pdflink = pdflinks[urlmark]
				returned_object = {}
				returned_object["url"] = urljoin(baseurl, singlelink)
				returned_object["country"] = country
				try: #State can be empty therefore use EAFP way - as far as i heard the most popular in Python
					returned_object["state"] = state_array[per_country_principal_counter]
				except:
					returned_object["state"] = "null"
				returned_object["reg_num"] = reg_num_array[per_country_principal_counter]
				returned_object["address"] = address_array[per_country_principal_counter].replace(u'\xa0', u' ')
				returned_object["foreign_principal"] = foreign_principal
				date_item = date_array[per_country_principal_counter]				
				mm,dd,yy = date_item.split("/")
				date_item = datetime.datetime(day=int(dd), month=int(mm), year=int(yy))
				date_item = str(date_item)
				date_item = date_item.replace(" ", "T")
				returned_object["date"] = date_item
				returned_object["registrant"] = registrant_array[per_country_principal_counter]
				returned_object["exhibit_url"] = pdflink
				yield returned_object
				per_country_principal_counter += 1
			per_page_countries_counter += 1	

	def parse_pdf(self, baseurl, pdfurls):
		#this sub will be called and then scrapy would wait for it to finish otherwise data structure may not be correct
		returned = {}
		for link in pdfurls:
			try:
				# since technical task does not openly advise that all the requests should be build using scrapy,
				# one synchronous request was built using urllib2 and CookieJar 
				# for sake of data structure correctness(mostly), maintability of the code and full automation of the scrapper
				# no scrapping speed loss detected from my end
				# as there are not too much exhibit urls on the pages
				# at least i see the solution this way as i came from WWW::Mechanize
				openlink = urljoin(baseurl,link)
				cookies = CookieJar()
				builtrequest = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
				request = builtrequest.open(openlink)
				response = HtmlResponse(url=openlink, body=request.read())
				pdfpath = scrapy.Selector(response)# Scrapy will still parse the response and scrap the data
				pdf_links_structure = pdfpath.xpath("//td[@headers='DOCLINK']/a")
				pdflinks_data = {}
				singlepdfurl = "No Documents Found."				
				if (len(pdf_links_structure) > 0):
					singlepdfurl = pdf_links_structure[0].css('a ::attr("href")').extract()[0]
				else:
					singlepdfurl = "No Documents Found."
			except:
				singlepdfurl = "No Documents Found." # Connection error => No Documents Found.
			urlmark = md5(str(openlink)).hexdigest()
			returned[urlmark] = singlepdfurl
		return returned
