# codesamples-python-unit-tests-for-old-scrapy-example
Unit tests for https://github.com/giantpanda9/codesample-python-scrapy-old-example
# Disclaimer
Old code to show the ability to work with Unit Testing in Python 2.7 related to aforementioned project
# Purpose
1. Mostly needed to display abilties to use Unit Testing in Python as tests are quite simple in structure
2. Not sure if this test still relevant for the corresponding site
3. The code will be archieved as only to be used as proof of ability to do Python Unit Testing
# Dependencies
1. Modules:
  unittest
  json
2. Files from corresponding other archieved project:
  1. output.json — my scraper output file as it must be in the same fodler with the
  fara_gov_first_page/unittests/output_file_integrity_test.py unit test
  2. template.json — the example structure from the GovPredict Interview, Scraping Foreign
  Principals Google Doc file to compare with
  Without the both two files mentioned above /unittests/output_file_integrity_test.py will not work properly
# Description
1. /unittests/output_file_integrity_test.py
This actually a kit of tests that seem to have the common purpose to me:
def test_returned_object_correctness(self): - tests if output.json file has the same number of keys
and the same values of keys as per Techincal Requirements, described in GovPredict Interview,
Scraping Foreign Principals Google Doc file
def test_returned_object_integrity(self): asserts if values of the output.json structure are not empty
with exception for state and address keys, which actually could be empty
def test_returned_object_principal_count(self): i was advised and so understood/comprehend the
advise that i need to scrape the first page of Active Foreign Principal only, which are only 15. I was
also advised and so understood/comprehend the advise that i need only one entry for each
Foreign Principal therefore there could be only 15 items in the returned structure — that i assert in
this test
def test_returned_irrelevant_value(self): there lots of irrelevant values in address line that look
like \xa0 the test is asserting this values presence and fails if so
2. /unittests/fetch_pdf_sub_correctness_test.py contains only one unit test -
def test_pdf_data_correctness(self):, which asserts the case if parse_pdf function of the spider
created is fetching the most recent url, based on static page where the links should not change
I created the aforementioned unit tests based on my assumption what critical parts of the scrapy
spider/scraper required closer attention. I actually tested my scraper output and parse_pdf function
using them and found and fixed a few mistakes in code with the help of those unit tests.
