from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, Date, func
from sqlalchemy.orm import sessionmaker, declarative_base
import uuid
import data
import csv

Base = declarative_base()
class Fish(Base):
    __tablename__ = "fish"
    id = Column("id", String, primary_key=True)
    type = Column("type", String)
    date = Column("date", String)
    value = Column("value", Integer)
    itemid = Column(String, ForeignKey("item.id"))
    siteid = Column(String, ForeignKey("site.id"))

    def __init__(self, type, date, value, itemid, siteid):
        self.id = str(uuid.uuid4())
        self.type = type
        self.date = date
        self.value = value
        self.itemid = itemid
        self.siteid = siteid

class Item(Base):
    __tablename__ = "item"
    id = Column("id", String, primary_key=True)
    type = Column("type", String)

    def __init__(self, id, type):
        self.id = id
        self.type = type

class Site(Base):
    __tablename__ = "site"
    id = Column("id", String, primary_key=True)
    type = Column("type", String)

    def __init__(self, id, type):
        self.id = id
        self.type = type

def connect():
    engine = create_engine("sqlite:///fishdb.db", echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    site_exist = session.query(Site).count() == len(data.DISTRICTS)
    if not site_exist:
        print("Site table incomplete or missing, creating new one")
        session.query(Site).delete()
        __create_site_objects(session)
    items_exist = session.query(Item).count() == len(data.FISH)
    if not items_exist:
        print("Items table incomplete or missing, creating new one")
        session.query(Item).delete()
        __create_item_objects(session)
    return session

def __create_site_objects(session):
    districts = data.DISTRICTS
    for id, district in enumerate(districts):
        site = Site(id, district)
        session.add(site)
    session.commit()

def __create_item_objects(session):
    fish = data.FISH
    for id, f in enumerate(fish):
        item = Item(id, f)
        session.add(item)
    session.commit()

def add_observed_data(session, file_path, type_description, item_id, site_id):
    fish_exist = session.query(Fish).count() != 0
    if not fish_exist:
        print("Adding observed data")
        with open(file_path, newline="") as f:
            csv_it = csv.reader(f, delimiter=',')
            for row in csv_it:
                fish = Fish(type_description, row[0], row[1], item_id, site_id)
                session.add(fish)
            print("Number of data objects added to database: ", csv_it.line_num)
            session.commit()
