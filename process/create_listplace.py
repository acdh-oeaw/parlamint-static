import os
import pandas as pd
from lxml import etree as ET
from slugify import slugify
from acdh_tei_pyutils.tei import TeiReader

dummy = """
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
      <fileDesc>
         <titleStmt>
            <title type="main">Register der Orte</title>
            <title type="sub">Österreichisches Parlamentskorpus ParlaMint-AT [ParlaMint]</title>
         </titleStmt>
         <publicationStmt>
            <p>Publication Information</p>
         </publicationStmt>
         <sourceDesc>
            <p>Information about the source</p>
         </sourceDesc>
      </fileDesc>
  </teiHeader>
  <text>
      <body>
         <listPlace></listPlace>
      </body>
  </text>
</TEI>
"""

file = os.path.join("data", "indices", "listperson.xml")
doc = TeiReader(file)

data = {}
for x in doc.any_xpath(".//tei:placeName"):
    key = f"place-{slugify(x.text)}"
    x.attrib["key"] = key
    data[key] = x.text
doc.tree_to_file(file)

doc = TeiReader(dummy)
list_place = doc.any_xpath(".//tei:listPlace")[0]
for bad in doc.any_xpath(".//tei:place[@xml:id]"):
    bad.getparent().remove(bad)

for key, value in data.items():
    pl = ET.Element("{http://www.tei-c.org/ns/1.0}place")
    pl.attrib["{http://www.w3.org/XML/1998/namespace}id"] = key
    name = ET.Element("{http://www.tei-c.org/ns/1.0}placeName")
    name.text = value
    pl.append(name)
    list_place.append(pl)

for key, value in data.items:
    new_name = value.split(" (")[0]
doc.tree_to_file(os.path.join("data", "indices", "listplace.xml"))
df = pd.DataFrame.from_dict(data.items())
df.columns = ['id', 'name']
df.to_csv(os.path.join("process", "places.csv"), index=False)
