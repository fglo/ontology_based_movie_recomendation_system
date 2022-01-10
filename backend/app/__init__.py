from shutil import copyfile
from owlready2 import *

owlready2.JAVA_EXE = "C:\\Program Files\\java\\bin\\java.exe"

onto = get_ontology("../../data/System rekomendacji v0.6.1.owl").load()

with onto:
    sync_reasoner_pellet(onto, infer_property_values = True)
    onto.save(file = "../../data/system_rekomendacji_v06_extra.owl", format = "rdfxml")
    copyfile("../../data/system_rekomendacji_v06_extra.owl", "../../data/system_rekomendacji_extra.owl")