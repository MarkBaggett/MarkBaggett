from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey 
from sqlalchemy.orm import relationship


class Rooms(Model):
    id = Column(Integer, primary_key=True)
    number = Column(String(3), unique=True, nullable=False)
    interface = Column(String(10), unique=True, nullable=False)

    def __repr__(self):
        return self.number


class Classes(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(8), unique = True, nullable=False)
    commands = Column(String(10000), unique = True, nullable=False)

    def __repr__(self):
        return self.course

