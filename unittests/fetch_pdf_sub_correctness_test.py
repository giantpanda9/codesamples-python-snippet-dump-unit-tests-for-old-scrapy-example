#!/usr/bin/python
# -*- coding: utf-8 -*-
# This test asserts the parse_pdf function of the scrapy spider and checks that the sub takes the correct pdf document
# by passing a golden page downloaded from the far.gov site and checking if returned url is equal to "http://www.fara.gov/docs/6549-Exhibit-AB-20180601-23.pdf"
#(name: "Tourism Northern Territory") as document is the most recent document on static downloaded page and dated as 06/01/2018
# This unit test should be in one folder with the scrapy spider
# Author: Nikolay Chegodaev as part of GP Application Submission Test
import faragovfirstpage_spider as spider
import unittest
import os
from hashlib import md5
from urlparse import urljoin
class subCorrectnessTest(unittest.TestCase):
	def test_pdf_data_correctness(self): # This test calls parse_pdf function from spider 
		baseurl = "file://" # we need to reconstruct the logic that was used in fara.gov spider to get the pdf url
		links_array = []
		searchpath = os.path.abspath(os.curdir)
		htmlpath = searchpath + "/testtemplate/Documents.html"#test template (just a downloaded document page - included) should be in one folder with the unit test script
		links_array.append(htmlpath)
		spiderclass = spider.FaragovfirstpageSpiderSpider()
		pdflinks = spiderclass.parse_pdf(baseurl, links_array)
		comparisonlink = "http://www.fara.gov/docs/6549-Exhibit-AB-20180601-23.pdf"
		urlmark = md5(str(urljoin(baseurl, htmlpath))).hexdigest()
		testcase = pdflinks[urlmark]
		self.assertEqual(testcase, comparisonlink)

if __name__ == '__main__':
	unittest.main()


