from owlready2 import *
from . import config

instance = None

def init_onto():
    global instance
    
    owlready2.JAVA_EXE = config.java_path
    instance = get_ontology("data/system_rekomendacji_extra.owl").load()


def get():
    global instance
    if instance is None:
        init_onto()
    return instance