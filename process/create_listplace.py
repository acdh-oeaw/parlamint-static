import os
import pandas as pd
import lxml.etree as ET

from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import get_xmlid
from acdh_xml_pyutils.xml import NSMAP

from collections import defaultdict

# Initialize a dictionary to store people associated with each place
place_to_people = defaultdict(lambda: {"birth": [], "death": []})

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
place_file = os.path.join("data", "indices", "listplace.xml")
place_doc = TeiReader(place_file)
for bad in place_doc.any_xpath(".//tei:place[@xml:id]"):
    bad.getparent().remove(bad)

listplace = place_doc.any_xpath(".//tei:listPlace")[0]

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
    listplace.append(place)
 

enriched_places = pd.read_csv(os.path.join("process", "enriched_places.csv"))
persons = pd.read_csv(os.path.join("process", "places.csv"))
person_file = os.path.join("data", "indices", "listperson.xml")
person_doc = TeiReader(person_file)

for i, x in enumerate(person_doc.any_xpath(".//tei:person[@xml:id]")):
    xml_id = get_xmlid(x)
    try:
        current_person = persons[persons['xml_id'] == xml_id].iloc[0]
    except IndexError:
        continue
    try:
        place = x.xpath(".//tei:birth/tei:placeName", namespaces=NSMAP)[0]
        try:
            place_id = current_person["place_of_birth"].split("/")[-1]
            place.attrib["key"] = place_id
            # Locate the corresponding place in listplace.xml
            listplace_place = place_doc.any_xpath(f".//tei:place[@xml:id='{place_id}']")[0]
            note_grp = listplace_place.find("{http://www.tei-c.org/ns/1.0}noteGrp")
            if note_grp is None:
                note_grp = ET.Element("{http://www.tei-c.org/ns/1.0}noteGrp")
                listplace_place.append(note_grp)
            note = ET.Element("{http://www.tei-c.org/ns/1.0}note",attrib={"type": "births", "target": f"#{xml_id}"})
            note.text = f"{current_person['name']}, {current_person['first_name']}"
            note_grp.append(note)
        except AttributeError:
            pass
    except IndexError:
        pass
    try:
        place = x.xpath(".//tei:death/tei:placeName", namespaces=NSMAP)[0]
        try:
            place_id = current_person["place_of_death"].split("/")[-1]
            place.attrib["key"] = place_id
             # Locate the corresponding place in listplace.xml
            listplace_place = place_doc.any_xpath(f".//tei:place[@xml:id='{place_id}']")[0]
            note_grp = listplace_place.find("{http://www.tei-c.org/ns/1.0}noteGrp")
            if note_grp is None:
                note_grp = ET.Element("{http://www.tei-c.org/ns/1.0}noteGrp")
                listplace_place.append(note_grp)
            note = ET.Element("{http://www.tei-c.org/ns/1.0}note",attrib={"type": "deaths", "target": f"#{xml_id}"})
            note.text = f"{current_person['name']}, {current_person['first_name']}"
            note_grp.append(note)
        except AttributeError:
            pass
    except IndexError:
        pass

place_doc.tree_to_file(place_file)
person_doc.tree_to_file(person_file)
