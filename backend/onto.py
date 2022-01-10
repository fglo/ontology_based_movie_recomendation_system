from owlready2 import *
from . import config

instance = None

def init_onto():
    global instance
    owlready2.JAVA_EXE = config.java_path
    instance = get_ontology("data/system_rekomendacji_extra.owl").load()
    sync()


def get():
    global instance
    if instance is None:
        init_onto()
    return instance

def sync():
    global instance
    if instance is None:
        init_onto()
    sync_reasoner(instance, infer_property_values = True)
    
def add_user(username):
    global instance
    if instance is None:
        init_onto()
    instance.Uzytkownik(username)
        
def get_users():
    global instance
    if instance is None:
        init_onto()
    return list(instance.get_instances_of(instance["Uzytkownik"]))
    
def get_actors():
    global instance
    if instance is None:
        init_onto()
    return list(instance.get_instances_of(instance["Aktor"]))
    
def get_series():
    global instance
    if instance is None:
        init_onto()
    return list(instance.get_instances_of(instance["Seria"]))
    
def get_movies():
    global instance
    if instance is None:
        init_onto()
    return list(instance.get_instances_of(instance["Film"]))
    
def get_categories():
    global instance
    if instance is None:
        init_onto()
    return list(instance.get_instances_of(instance["Kategoria"]))
    
def get_tags():
    global instance
    if instance is None:
        init_onto()
    return list(instance.get_instances_of(instance["Tag"]))