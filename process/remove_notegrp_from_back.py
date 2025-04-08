import glob
from acdh_tei_pyutils.tei import TeiReader
from tqdm import tqdm

print("removes mentions list (.//tei:back//tei:noteGrp) from back elements")

files = glob.glob("./data/*/*xml")

faulty = []
for x in tqdm(files):
    doc = TeiReader(x)
    for bad in doc.any_xpath(".//tei:back//tei:noteGrp"):
        bad.getparent().remove(bad)
    doc.tree_to_file(x)
