import os
import pandas as pd
from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import get_xmlid
from acdh_xml_pyutils.xml import NSMAP
from acdh_wikidata_pyutils import WikiDataPerson
from tqdm import tqdm


file = os.path.join("data", "indices", "listperson.xml")
doc = TeiReader(file)
failed = []
entities = []
items = doc.any_xpath(".//tei:person[./tei:idno[@subtype='wikidata']]")
for x in tqdm(items, total=len(items)):
    xml_id = get_xmlid(x)
    wikidata = x.xpath("./tei:idno[@subtype='wikidata']", namespaces=NSMAP)[0].text
    try:
        wd_item = WikiDataPerson(wikidata)
    except Exception as e:
        failed.append[[xml_id, e]]
        continue
    ent_dict = wd_item.get_apis_entity()
    ent_dict["place_of_birth"] = wd_item.place_of_birth
    ent_dict["place_of_death"] = wd_item.place_of_death
    ent_dict["xml_id"] = xml_id
    entities.append(ent_dict)

df = pd.DataFrame(entities)
df.to_csv(os.path.join("process", "places.csv"), index=False)

