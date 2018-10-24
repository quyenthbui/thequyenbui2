from mongoengine import*

class User(Document):
    fullname = StringField()
    email = StringField()
    username = StringField()
    password = StringField()
    contributed = IntField()
class Song(Document):
    happy = IntField()
    name = StringField()
    author = StringField()
    link = StringField()
    link_img = StringField()
    user_id = ReferenceField(User)
class Book(Document):
    happy = IntField()
    name = StringField()
    author = StringField()
    link = StringField()
    link_img = StringField()
    user_id = ReferenceField(User)
class Video(Document):
    happy = IntField()
    name = StringField()
    author = StringField()
    link = StringField()
    link_img = StringField()
    user_id = ReferenceField(User)
class Place(Document):
    happy = IntField()
    name = StringField()
    describe = StringField()
    link = StringField()
    user_id = ReferenceField(User)
class Contribution(Document):
    happy = IntField()
    song = ReferenceField(Song)
    book = ReferenceField(Book)
    video = ReferenceField(Video)
    place = ReferenceField(Place)
    user_id = ReferenceField(User)
    approved = BooleanField()
