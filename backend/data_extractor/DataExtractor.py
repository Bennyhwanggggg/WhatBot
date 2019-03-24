import requests
import sys
from bs4 import BeautifulSoup
from database.DataBaseManager import DataBaseManager


class DataExtractor:
    def __init__(self, study_level='postgraduate', course='COMP9900'):
        self.study_level = study_level
        self.course = course
        self.details = dict()
        self.data_base_manager = DataBaseManager()

    def extract(self):
        # undergraduate and comp3900 are parameters
        url = "https://www.handbook.unsw.edu.au/{}/courses/2019/{}/".format(self.study_level, self.course)
        url = requests.get(url)
        htmltext = url.text

        #read the html
        soup = BeautifulSoup(htmltext, 'html.parser')

        #store the data we need
        # self.details["Title"] = soup.title.string
        # self.details["Description"] = soup.find(id="readMoreIntro").div.p.string
        # self.details["Credit"] = soup.find_all('strong')[1].string
        # self.details["Prerequisite"] = soup.find(id="readMoreSubjectConditions").div.div.string
        # self.details["Course Outline"] = soup.find(id="subject-outline").div.a.attrs['href']
        # self.details["Faculty"] = soup.select('.o-attributes-table-item ')[0].a.attrs['href']
        # self.details["School"] = soup.select('.o-attributes-table-item ')[1].a.attrs['href']
        # self.details["Offering Terms"] = soup.select('.o-attributes-table-item ')[3].p.string
        # self.details["Campus"] = soup.select('.o-attributes-table-item ')[4].p.string.replace(" ", "").strip()
        #
        # for value in soup.select('.p-all-1')[0].children:
        #     if soup.select('.p-all-1')[0].index(value) == 3:
        #         self.details["PDF"] = value.a.attrs['href']
        #
        # self.details["Indicative contact hours"] = soup.select('.o-attributes-table-item ')[5].p.string
        # self.details["Commonwealth Supported Student"] = soup.select('.a-column-sm-12')[8].p.string.strip()
        # self.details["Domestic Student"] = soup.select('.a-column-sm-12')[10].p.string.strip()
        # self.details["International Student"] = soup.select('.a-column-sm-12')[12].p.string.strip()

        if soup.title.string:
            self.details["Title"] = soup.title.string
        else:
            self.details["Title"] = ""
        if soup.find(id="readMoreIntro").div.p:
            self.details["Description"] = soup.find(id="readMoreIntro").div.p.string
        else:
            self.details["Description"] = ""
        if soup.find_all('strong')[1]:
            self.details["Credit"] = soup.find_all('strong')[1].string
        else:
            self.details["Credit"] = ""
        if soup.find(id="readMoreSubjectConditions"):
            self.details["Prerequisite"] = soup.find(id="readMoreSubjectConditions").div.div.string
        else:
            self.details["Prerequisite"] = ""
        if soup.find(id="subject-outline"):
            self.details["Course Outline"] = soup.find(id="subject-outline").div.a.attrs['href']
        else:
            self.details["Course Outline"] = ""
        if soup.select('.o-attributes-table-item ')[0].a:
            self.details["Faculty"] = soup.select('.o-attributes-table-item ')[0].a.attrs['href']
        else:
            self.details["Faculty"] = ""
        if soup.select('.o-attributes-table-item ')[1].a:
            self.details["School"] = soup.select('.o-attributes-table-item ')[1].a.attrs['href']
        else:
            self.details["School"] = ""
        if soup.select('.o-attributes-table-item ')[3].p:
            self.details["Offering Terms"] = soup.select('.o-attributes-table-item ')[3].p.string
        else:
            self.details["Offering Terms"] = ""
        if soup.select('.o-attributes-table-item ')[4].p:
            self.details["Campus"] = soup.select('.o-attributes-table-item ')[4].p.string.replace(" ", "").strip()
        else:
            self.details["Campus"] = ""

        if soup.select('.p-all-1')[0]:
            for value in soup.select('.p-all-1')[0].children:
                if (soup.select('.p-all-1')[0].index(value) == 3):
                    self.details["PDF"] = value.a.attrs['href']
        else:
            self.details["PDF"] = ""

        if soup.select('.o-attributes-table-item ')[5].p:
            self.details["Indicative contact hours"] = soup.select('.o-attributes-table-item ')[5].p.string
        else:
            self.details["Indicative contact hours"] = ""
        if soup.select('.a-column-sm-12')[8].p:
            self.details["Commonwealth Supported Student"] = soup.select('.a-column-sm-12')[8].p.string.strip()
        else:
            self.details["Commonwealth Supported Student"] = ""
        if soup.select('.a-column-sm-12')[10].p:
            self.details["Domestic Student"] = soup.select('.a-column-sm-12')[10].p.string.strip()
        else:
            self.details["Domestic Student"] = ""
        if soup.select('.a-column-sm-12')[12].p:
            self.details["International Student"] = soup.select('.a-column-sm-12')[12].p.string.strip()
        else:
            self.details["International Student"] = ""

    def save(self):
        # print(self.course)
        # print(self.details["Title"])
        # print(self.details["Credit"])
        # print(self.details["Prerequisite"])
        # print(self.details["Course Outline"])
        # print(self.details["Faculty"])
        # print(self.details["School"])
        # print(self.details["Offering Terms"])
        # print(self.details["Campus"])
        # print(self.details["Description"])
        # print(self.details["PDF"])
        # print(self.details["Indicative contact hours"])
        # print(self.details["Commonwealth Supported Student"])
        # print(self.details["Domestic Student"])
        # print(self.details["International Student"])
        self.data_base_manager.add_handbook_entry(self.course, self.details["Title"], self.details["Credit"],
                                                  self.details["Prerequisite"],self.details["Course Outline"],
                                                  self.details["Faculty"],
                                                  self.details["School"], self.details["Offering Terms"],
                                                  self.details["Campus"], self.details["Description"], self.details["PDF"],
                                                  self.details["Indicative contact hours"],
                                                  self.details["Commonwealth Supported Student"],
                                                  self.details["Domestic Student"],
                                                  self.details["International Student"])

        #




if __name__ == '__main__':
    if len(sys.argv) > 1:
        data_extractor = DataExtractor(sys.argv[1], sys.argv[2])
    else:
        data_extractor = DataExtractor()
    data_extractor.extract()
    data_extractor.save()