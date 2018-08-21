import json
import orage.scraping as scrap
import orage.framagenda as fagenda

# Step 1: get te calendar from the web
my_scraper = scrap.EdouardPhilippe()
my_scraper.scrap()
json_file = my_scraper.save()

# Step 2: upload the calendar online
with open("../data/sources.json") as input_file:
    data = json.load(input_file)
sources = data['sources']
for person in sources:
    if person["id"] == my_scraper.source_id:
        minister = person
        fagenda.create_vevents(minister, json_file)
