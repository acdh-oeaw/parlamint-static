import os
import lxml.etree as ET

from acdh_tei_pyutils.tei import TeiReader
from acdh_wikidata_pyutils import fetch_image
from acdh_xml_pyutils.xml import NSMAP
from tqdm import tqdm

file = os.path.join("data", "indices", "listperson.xml")
doc = TeiReader(file)

for bad in doc.any_xpath(".//tei:figure"):
    bad.getparent().remove(bad)


for x in tqdm(doc.any_xpath(".//tei:person[@xml:id][./tei:idno[@subtype='wikidata']]")):
    wikidata_url = x.xpath("./tei:idno[@subtype='wikidata']/text()", namespaces=NSMAP)[
        0
    ]
    img_url = fetch_image(wikidata_url)
    if img_url:
        fig = ET.Element("{http://www.tei-c.org/ns/1.0}figure")
        graphic = ET.Element(
            "{http://www.tei-c.org/ns/1.0}graphic", attrib={"url": img_url}
        )
        fig.append(graphic)
        x.append(fig)

doc.tree_to_file(file)
