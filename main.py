import json
import xml.etree.ElementTree as et
from dataclasses import dataclass, asdict


@dataclass
class Song:
    song_id: str
    title: str
    artist: str

    def use_product(self, product):
        product.start_object("song", self.song_id)
        product.add_property("title", self.title)
        product.add_property("artist", self.artist)

@dataclass
class Movie:
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
    creator = SerializerCreator()
    my_product = creator.get_serializer(data_format)
    object_to_serialize.use_product(my_product)
    print(creator)
    return str(my_product)

# creator
class SerializerCreator:
    def __init__(self):
        self.data_format = None

    def get_serializer(self, data_format):
        self.data_format = data_format
        if data_format == "JSON":
            return _JSONSerializer()
        elif data_format == "XML":
            return _XMLSerializer()
        else:
            raise ValueError(data_format)
        
    def __repr__(self):
        return f"SerializerCreator(data_format={self.data_format})"
    
    def __str__(self):
        return f"""Here is your item in {self.data_format} format:"""
    
# products

class _JSONSerializer:
    def __init__(self):
        self._current_object = None

    def start_object(self, object_name, object_id):
        self._current_object = {"id": object_id}

    def add_property(self, name, value):
        self._current_object[name] = value

    def __str__(self):
        return json.dumps(self._current_object)

class _XMLSerializer:
    def __init__(self):
        self._item = None

    def start_object(self, object_name, object_id):
        self._item = et.Element(object_name, attrib={"id": object_id})
        
    def add_property(self, name, value):
        prop = et.SubElement(self._item, name)
        prop.text = value
    
    def __str__(self):
        return et.tostring(self._item, encoding="unicode")
    
# try it out

# song
my_song = Song("1", "Hammer", "Lorde")
print(serialize(my_song, "XML"))
print(serialize(my_song, "JSON"))

# movie
my_movie = Movie("2", "Dune 2", "Denis Villeneuve", 166)
print(serialize(my_movie, "XML"))
print(serialize(my_movie, "JSON"))
