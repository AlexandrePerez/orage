# TODO Documentation
import os

import abc
import json
from collections import defaultdict
import logging
import requests
from bs4 import BeautifulSoup
import datetime
import dateparser


class Scraper:
    __metaclass__ = abc.ABCMeta
    _url = ''
    _vevents = []
    _first_name = ""
    _last_name = ""

    @abc.abstractmethod
    def scrap(self):
        """
        Get the calendar from the website.

        Save it in self._vevents as a dictionary with the ICalendar format.
        :return:
        """
        return

    def save(self):
        """
        Save the calendar into a JSON file.
        :return:
        """
        my_path = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(my_path, '../data/json/' + str(self._first_name) + "_" + str(self._last_name) + "_" +
                                        datetime.datetime.now().strftime("%Y%m%d") + '.json'), 'w') as outfile:
            json.dump(self._vevents, outfile, ensure_ascii=True)
        return outfile.name


class EdouardPhilippe(Scraper):
    """
    The scraper for Edouard Philppe, 1er ministre.
    """
    def __init__(self):
        self.source_id = 0  # mandatory

        # get info from the sources file
        my_path = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(my_path, '../data/sources.json')) as input_file:
            data = json.load(input_file)
            sources = data['sources']
            for idx in range(len(sources)):
                if sources[idx]['id'] == self.source_id:
                    self._url = data['sources'][idx]['url']
                    self._last_name = data['sources'][idx]['person']['last_name']
                    self._first_name = data['sources'][idx]['person']['first_name']
                    break
            else:
                # raise ValueError("id {} not found in sources.".format(self._source_id))
                logging.error("source id: {} not found in sources.json".format(self.source_id))

    def scrap(self):
        if not self._url:
            logging.error("No URL specified for this source.")
            return

        print("scraping {}...".format(self._url))

        req = requests.get(self._url)

        soup = BeautifulSoup(req.text, 'html.parser')
        agenda = soup.find_all(class_='agenda-jour')
        for jour in agenda:
            for child in jour.children:
                try:
                    if str(child).find('agenda-jour-titre') != -1:
                        date = dateparser.parse(child.text).date()
                    else:
                        for event in child.children:
                            rendez_vous = defaultdict()
                            # print("event : {}".format(event))
                            for info in event.children:
                                if str(info).find('agenda-evenement-heure') != -1:
                                    time = dateparser.parse(info.text).time()
                                    rendez_vous['DTSTART'] = str(date).replace('-', '') + 'T' + \
                                                             str(time).replace(':', '') + 'Z'
                                elif str(info).find('agenda-evenement-titre') != -1:
                                    rendez_vous['SUMMARY'] = info.text
                                elif str(info).find('agenda-evenement-lieu') != -1:
                                    rendez_vous['LOCATION'] = info.text
                                else:
                                    logging.warning('WARNING unknown field : {}'.format(info))
                            self._vevents.append(rendez_vous)
                except AttributeError:  # case "Agenda non disponible"
                            continue


if __name__ == '__main__':
    my_scraper = EdouardPhilippe()
    my_scraper.scrap()
    my_scraper.save()
