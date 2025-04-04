import os
import pandas as pd
from lxml import etree as ET
from acdh_tei_pyutils.tei import TeiReader
from acdh_xml_pyutils.xml import NSMAP

file = os.path.join("data", "indices", "listperson.xml")
doc = TeiReader(file)
for bad in doc.any_xpath(".//tei:idno[@subtype='wikidata']"):
    bad.getparent().remove(bad)

df = pd.read_csv(os.path.join("process", "wikidata_ids.csv"))

for x in doc.any_xpath(".//tei:person[@xml:id and ./tei:idno[@subtype='parliament']]"):
    parla_id = x.xpath("./tei:idno[@subtype='parliament']", namespaces=NSMAP)[0].text
    pad_id = ''.join(filter(str.isdigit, parla_id))
    matching_row = df[df['p2280'] == int(pad_id)]
    if not matching_row.empty:
        wiki_id = matching_row.iloc[0]['entity']
        idno = ET.Element("{http://www.tei-c.org/ns/1.0}idno", attrib={'type': 'URI', 'subtype': 'wikidata'})
        idno.text = wiki_id
        x.append(idno)
doc.tree_to_file(file)
