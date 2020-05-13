#!/usr/bin/python
# -*- coding: utf-8 -*-
# unit test script to test faragovfirstpage_spider output file integrity and correctness
# in comparison to 'golden' file template
# test must be in the same folder as output.json file of the scrapy
# required file names:
# golden template - template.json and should contain sample structure from the test description
# scrapy output file name - output.json contains all 15 objects scraped from first fara gove Active Foreign Principals page
# Author: Nikolay Chegodaev as part of GP Application Submission Test
import unittest
import json
class fileIntegrityTest(unittest.TestCase):
	def test_returned_object_correctness(self):
		scrapyoutputfile = open("output.json", "r").read()
		templatefile = open("template.json", "r").read()		
		scrapyoutputdata = json.loads(scrapyoutputfile)
		templatedata = json.loads(templatefile)
		scrapykeys = []
		templatekeys = []
		scrapyresult = scrapyoutputdata[0] # Seems no necessity to loop over all the items as objects in result scrapy list are all similar - let's speed up test time and test only one object
		for scrapykey in scrapyresult:
			scrapykeys.append(scrapykey)
		for templatekey in templatedata:
			templatekeys.append(templatekey)
		self.assertItemsEqual(scrapykeys, templatekeys) # this function does the check if two arrays has equal element count and values of those elements are also equal
	def test_returned_object_integrity(self):
		scrapyoutputfile = open("output.json", "r").read()
		scrapyoutputdata = json.loads(scrapyoutputfile)
		scrapykeys = []
		for scrapyresult in scrapyoutputdata:
			for scrapykey in scrapyresult:
				if ((scrapykey=="state") or (scrapykey=="address")): # state may not have a value - exclude from test / address also maybe empty - for example for "Movimento de Uniao Nacional (M.U.N) Angola"
					pass
				else: 
					self.assertFalse(not(scrapyresult[scrapykey]), msg="The following key does not have a value: "+ scrapykey) # this asserting if some item in the structure does not have a value
	def test_returned_object_principal_count(self):
		goldencount = 15 # actually there are 15 principals on the page so default to this value
		scrapyoutputfile = open("output.json", "r").read()
		scrapyoutputdata = json.loads(scrapyoutputfile)
		self.assertTrue(len(scrapyoutputdata)==goldencount, msg="Actual principal count is " + str(len(scrapyoutputdata))) # assert if count of principals is 15
	def test_returned_irrelevant_value(self):		
		scrapyoutputfile = open("output.json", "r").read()
		scrapyoutputdata = json.loads(scrapyoutputfile)
		scrapykeys = []
		for scrapyresult in scrapyoutputdata:
			for scrapykey in scrapyresult:
				self.assertTrue(scrapyresult[scrapykey].find(u'\xa0'), msg="The following key: " + scrapykey + " includes xa0")
if __name__ == '__main__':
	unittest.main()
