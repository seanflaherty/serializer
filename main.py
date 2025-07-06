import json
import xml.etree.ElementTree as et
import yaml
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod

class ClientBluePrint(ABC):
    @abstractmethod
    def use_product(self):
        pass
@dataclass
class Song(ClientBluePrint):
    song_id: str
    title: str
    artist: str

    def use_product(self, product):
        product.start_object("song", self.song_id)
        product.add_property("title", self.title)
        product.add_property("artist", self.artist)

@dataclass
class Movie(ClientBluePrint):
    movie_id: str
    title: str
    director: str
    running_time: int = 0  # in minutes

    def use_product(self, product):
        product.start_object("movie", self.movie_id)
        product.add_property("title", self.title)
        product.add_property("director", self.director)
        product.add_property("running_time", str(self.running_time))

def serialize(object_to_serialize, data_format):
    my_product = creator.factory_method(data_format)
    object_to_serialize.use_product(my_product)
    print(creator)
    return str(my_product)

# creator

class CreatorBluePrint(ABC):
    @abstractmethod
    def factory_method(self):
        pass
    @abstractmethod
    def register_format(self):
        pass
class SerializationBluePrint(ABC):

    @abstractmethod
    def start_object(self):
        pass

    @abstractmethod
    def add_property(self):
        pass

class SerializerCreator(CreatorBluePrint):
    def __init__(self):
        self._products = dict()
        self.data_format = None

    def register_format(self, data_format, product):
        self._products[data_format] = product

    def factory_method(self, data_format):
        self.data_format = data_format
        product = self._products.get(data_format)
        if not product:
            raise ValueError(f"Unsupported data format: {data_format}")
        return product()
        
    def __repr__(self):
        return f"SerializerCreator(data_format={self.data_format})"
    
    def __str__(self):
        return f"""Here is your item in {self.data_format} format:"""
    
# products

class _JSONSerializer(SerializationBluePrint):
    def __init__(self):
        self._current_object = None

    def start_object(self, object_name, object_id):
        self._current_object = {"id": object_id}

    def add_property(self, name, value):
        self._current_object[name] = value

    def __str__(self):
        return json.dumps(self._current_object)

class _XMLSerializer(SerializationBluePrint):
    def __init__(self):
        self._item = None

    def start_object(self, object_name, object_id):
        self._item = et.Element(object_name, attrib={"id": object_id})
        
    def add_property(self, name, value):
        prop = et.SubElement(self._item, name)
        prop.text = value
    
    def __str__(self):
        return et.tostring(self._item, encoding="unicode")
    
class _YAMLSerializer(_JSONSerializer):
    def __str__(self):
        return yaml.dump(self._current_object)
# register
creator = SerializerCreator()
creator.register_format("JSON", _JSONSerializer)
creator.register_format("XML", _XMLSerializer)
creator.register_format("YAML", _YAMLSerializer)

# try it out
# song
my_song = Song("1", "Hammer", "Lorde")
print(serialize(my_song, "XML"))
print(serialize(my_song, "JSON"))
print(serialize(my_song, "YAML"))

# movie
my_movie = Movie("2", "Dune 2", "Denis Villeneuve", 166)
print(serialize(my_movie, "XML"))
print(serialize(my_movie, "JSON"))
print(serialize(my_movie, "YAML"))
