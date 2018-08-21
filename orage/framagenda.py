import json
import logging
import caldav
from requests.auth import HTTPBasicAuth


def from_json(json_file):
    """
    Make a vcalendar of vevents as a string from a json calendar.

    :param json_file: the input events to add to the calendar
    :return: the vacalendars as a list of strings
    """
    with open(json_file) as inputfile:
        calendar = json.load(inputfile)

    vcalendars = []

    for rdv in calendar:
        vcal = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Orage Project//Framagenda//FR\n"
        vcal += "BEGIN:VEVENT\n"
        for key in rdv.keys():
            vcal += str(key) + ":" + str(rdv[key]) + "\n"
        # Unique ID. If two vevents start at the same time, they are the same vevent, so it is just an update
        vcal += "UID:orage@{}\n".format(rdv["DTSTART"])
        vcal += "END:VEVENT\n"
        vcal += "END:VCALENDAR\n"

        vcalendars.append(vcal)

    return vcalendars


def create_vevents(person, json_file, login, password):
    """
    Create the events on the online calendar.

    :param person: the minister as a dictionary
    :param json_file: the input events to add to the calendar
    :param login: login for the remote calendar
    :param password: password for the remote calendar
    :return:
    """

    client = caldav.DAVClient("https://framagenda.org/remote.php/dav/calendars/Orage/",
                              auth=HTTPBasicAuth(login, password))
    principal = client.principal()
    calendars = principal.calendars()

    for cal in calendars:
        if person["calendar"] in str(cal.url):
            calendar = cal
            break
    else:
        logging.error("no calendar not found: {}".format(person["calendar"]))
        return

    vcalendars = from_json(json_file)
    for vcal in vcalendars:
        event = calendar.add_event(vcal)
        print("Event {} created".format(event))


if __name__ == "__main__":
    import os
    my_path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(my_path, '../data/sources.json')) as input_file:
        data = json.load(input_file)
    sources = data['sources']
    ministre = sources[0]
    create_vevents(ministre, "../data/json/Edouard_Philippe_20180821.json")
