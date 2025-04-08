import os
import pandas as pd
from acdh_wikidata_pyutils import WikiDataPlace
from tqdm import tqdm


df = pd.read_csv(os.path.join("process", "places.csv"))
places = pd.concat([df['place_of_birth'], df['place_of_death']]).dropna().unique()

enriched_places = []
for x in tqdm(places, total=len(places)):
    pl_id = x.split("/")[-1]
    item = WikiDataPlace(x).get_apis_entity()
    item["xml_id"] = pl_id
    enriched_places.append(item)
df.to_csv(os.path.join("process", "enriched_places.csv"), index=False)
