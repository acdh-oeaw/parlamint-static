import os
from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import get_xmlid
from acdh_xml_pyutils.xml import NSMAP

doc = TeiReader(os.path.join("data", "indices", "listorg.xml"))

lookup_dict = {}

for x in doc.any_xpath(".//tei:org[@xml:id]"):
    xmlid = f"#{get_xmlid(x)}"
    try:
        name = x.xpath(".//tei:orgName[@full='abb']", namespaces=NSMAP)[0].text
    except IndexError:
        name = x.xpath(".//tei:orgName[@full='yes'][1]", namespaces=NSMAP)[0].text
    lookup_dict[xmlid] = name

file = os.path.join("data", "indices", "listperson.xml")

doc = TeiReader(file)
print("parsed file")

for x in doc.any_xpath(".//tei:person[@xml:id]/tei:affiliation[@ref]"):
    ref = x.attrib["ref"]
    name = lookup_dict[ref]
    x.attrib["n"] = name

doc.tree_to_file(file)
print("done")
