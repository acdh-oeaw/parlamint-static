import os
import pandas as pd
import lxml.etree as ET

from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import get_xmlid
from acdh_xml_pyutils.xml import NSMAP
# from acdh_wikidata_pyutils import WikiDataPlace
# from tqdm import tqdm


# df = pd.read_csv(os.path.join("process", "places.csv"))
# places = pd.concat([df['place_of_birth'], df['place_of_death']]).dropna().unique()

# enriched_places = []
# for x in tqdm(places, total=len(places)):
#     pl_id = x.split("/")[-1]
#     item = WikiDataPlace(x).get_apis_entity()
#     item["xml_id"] = pl_id
#     enriched_places.append(item)

# df = pd.DataFrame(enriched_places)
# df.to_csv(os.path.join("process", "enriched_places.csv"), index=False)
file = os.path.join("data", "indices", "listplace.xml")
doc = TeiReader(file)
for bad in doc.any_xpath(".//tei:place[@xml:id]"):
    bad.getparent().remove(bad)

listperson = doc.any_xpath(".//tei:listPlace")[0]

df = pd.read_csv(os.path.join("process", "enriched_places.csv"))

sorted_df = df.sort_values(by="name")

for i, row in sorted_df.iterrows():
    place = ET.Element(
        "{http://www.tei-c.org/ns/1.0}place",
        attrib={"{http://www.w3.org/XML/1998/namespace}id": row["xml_id"]},
    )
    placename = ET.Element("{http://www.tei-c.org/ns/1.0}placeName")
    placename.text = row["name"]
    place.append(placename)
    loc = ET.Element("{http://www.tei-c.org/ns/1.0}location", attrib={"type": "coords"})
    geo = ET.Element("{http://www.tei-c.org/ns/1.0}geo")
    geo.text = f'{row["lat"]} {row["lng"]}'
    loc.append(geo)
    place.append(loc)
    idno = ET.Element("{http://www.tei-c.org/ns/1.0}idno", attrib={"type": "URL", "subtype": "wikidata"})
    idno.text = f"http://www.wikidata.org/entity/{row['xml_id']}"
    place.append(idno)
    listperson.append(place)

doc.tree_to_file(file)


enriched_places = pd.read_csv(os.path.join("process", "enriched_places.csv"))
persons = pd.read_csv(os.path.join("process", "places.csv"))
file = os.path.join("data", "indices", "listperson.xml")
doc = TeiReader(file)

for i, x in enumerate(doc.any_xpath(".//tei:person[@xml:id]")):
    xml_id = get_xmlid(x)
    try:
        current_person = persons[persons['xml_id'] == xml_id].iloc[0]
    except IndexError:
        print(xml_id)
        continue
    try:
        place = x.xpath(".//tei:birth/tei:placeName", namespaces=NSMAP)[0]
        try:
            place.attrib["key"] = current_person["place_of_birth"].split("/")[-1]
        except AttributeError:
            pass
    except IndexError:
        pass
    try:
        place = x.xpath(".//tei:death/tei:placeName", namespaces=NSMAP)[0]
        try:
            place.attrib["key"] = current_person["place_of_death"].split("/")[-1]
        except AttributeError:
            pass
    except IndexError:
        pass
doc.tree_to_file(file)
