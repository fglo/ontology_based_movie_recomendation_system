from owlready2 import *

owlready2.JAVA_EXE = "C:\\Program Files\\java\\bin\\java.exe"

onto = get_ontology("System rekomendacji v0.9.owl").load()

with onto:
    sync_reasoner_pellet(infer_property_values = True)
    onto.save(file = "system_rekomendacji_extra.owl", format = "rdfxml")