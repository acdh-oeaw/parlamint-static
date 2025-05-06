import glob
import os

from datetime import datetime
from typesense.api_call import ObjectNotFound
from acdh_cfts_pyutils import TYPESENSE_CLIENT as client
from acdh_tei_pyutils.tei import TeiReader
from tqdm import tqdm


files = glob.glob("./data/editions/*.xml")

try:
    client.collections["parlamint"].delete()
except ObjectNotFound:
    pass

current_schema = {
    "name": "parlamint",
    "fields": [
        {"name": "id", "type": "string"},
        {"name": "rec_id", "type": "string"},
        {"name": "title", "type": "string"},
        {"name": "full_text", "type": "string"},
        {
            "name": "year",
            "type": "int32",
            "optional": True,
            "facet": True,
        },
        {"name": "persons", "type": "string[]", "facet": True, "optional": True},
        {
            "name": "legislative_period",
            "type": "string[]",
            "facet": True,
            "optional": True,
        },
        {"name":"date", "type": "int64", "facet": True, "optional": True},
    ],
}

client.collections.create(current_schema)


def get_entities(ent_type, ent_node, ent_name):
    entities = []
    # _path = f'.//tei:rs[@type="{ent_type}"]/@ref'
    e_path = ".//tei:u/@who"
    for p in body:
        ent = p.xpath(e_path, namespaces={"tei": "http://www.tei-c.org/ns/1.0"})
        ref = [ref.replace("#", "") for e in ent if len(ent) > 0 for ref in e.split()]
        for r in ref:
            p_path = f'.//tei:{ent_node}[@xml:id="{r}"]//tei:{ent_name}[1]'
            en = doc.any_xpath(p_path)
            if en:
                entity = " ".join(" ".join(en[0].xpath(".//text()")).split())
                if len(entity) != 0:
                    entities.append(entity)
                else:
                    with open("log-entities.txt", "a") as f:
                        f.write(f"{r} in {record['id']}\n")
    return [ent for ent in sorted(set(entities))]


records = []

for xml_file in tqdm(files, total=len(files)):
    doc = TeiReader(xml=xml_file)
    # make record for each document
    body = doc.any_xpath("//tei:body")
    record = {}
    record["id"] = os.path.split(xml_file)[-1]

    record["rec_id"] = os.path.split(xml_file)[-1]

    record["title"] = " ".join(
        " ".join(
            doc.any_xpath('.//tei:titleStmt/tei:title[@type="sub"][1]/text()')
        ).split()
    )

    date_str = doc.any_xpath("//tei:sourceDesc/tei:bibl/tei:date/@when")[0]

    try:
        record["year"] = int(date_str[:4])
        # Add Unix timestamp for date
        record["date"] = int(datetime.fromisoformat(date_str).timestamp())
        print(record["date"])
    except ValueError:
        pass

    if len(body) > 0:
        # get unique persons per page
        ent_type = "person"
        ent_name = "persName"
        record["persons"] = get_entities(
            ent_type=ent_type, ent_node=ent_type, ent_name=ent_name
        )

        # get legislative period
        record["legislative_period"] = doc.any_xpath(
            ".//tei:meeting[@xml:lang='de'][contains(@ana, '#parla.term')]/text()"
        )
        print(record["legislative_period"])

        record["full_text"] = "\n".join(
            " ".join("".join(p.itertext()).split()) for p in body
        )

        if len(record["full_text"]) > 0:
            records.append(record)


make_index = client.collections["parlamint"].documents.import_(records)
print(make_index)
print("done with indexing paralamint")

# make_index = CFTS_COLLECTION.documents.import_(cfts_records, {"action": "upsert"})
# print(make_index)
# print("done with cfts-index parlamint")
