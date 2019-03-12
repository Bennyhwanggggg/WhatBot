import requests
import sys
import csv
from bs4 import BeautifulSoup

class DataExtractor:
    def __init__(self, level, course):
    	self.level = level
    	self.course = course

    def storeDetails(details):
        #generate the csv
        with open('Handbook.csv', "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(details.items())

    def extractor(self):
    	# undergraduate and comp3900 are parameters
        url = requests.get("https://www.handbook.unsw.edu.au/"+self.level+"/courses/2019/"+self.course+"/")
        htmltext = url.text

    	#read the html
        soup = BeautifulSoup(htmltext, 'lxml')

        #create a dict
        details = {}
        #store the data we need
        details["Title"] = soup.title.string
        details["Description"] = soup.find(id="readMoreIntro").div.p.string
        details["Credit"] = soup.find_all('strong')[1].string
        details["Prerequisite"] = soup.find(id="readMoreSubjectConditions").div.div.string
        details["Course Outline"] = soup.find(id="subject-outline").div.a.attrs['href']

        details["Faculty"] = soup.select('.o-attributes-table-item ')[0].a.attrs['href']
        details["School"] = soup.select('.o-attributes-table-item ')[1].a.attrs['href']
        details["Offering Terms"] = soup.select('.o-attributes-table-item ')[3].p.string
        details["Campus"] = soup.select('.o-attributes-table-item ')[4].p.string.replace(" ", "").strip()

        for value in soup.select('.p-all-1')[0].children:
            if (soup.select('.p-all-1')[0].index(value) == 3):
                details["PDF"] = value.a.attrs['href']

        details["Indicative contact hours"] = soup.select('.o-attributes-table-item ')[5].p.string
        details["Commonwealth Supported Student"] = soup.select('.a-column-sm-12')[8].p.string.strip()
        details["Domestic Student"] = soup.select('.a-column-sm-12')[10].p.string.strip()
        details["International Student"] = soup.select('.a-column-sm-12')[12].p.string.strip()


        DataExtractor.storeDetails(details)

        return soup



if __name__ == '__main__':
	data = DataExtractor(sys.argv[1], sys.argv[2])
	data.extractor()
	# data.extractor(sys.argv[1], sys.argv[2])