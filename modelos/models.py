#Modelo de la base de datos
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#tabla Categorias
class Categorias(db.Model):
    __tablename__='Cat_categorias'
    id_categorias = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.Text)
    tarea = db.relationship('Tareas',backref='tarea',lazy='dynamic')

class Estado(db.Model):
    __tablename__='Cat_estado'
    id_estado = db.Column(db.Integer,primary_key=True)
    estado = db.Column(db.Text)
    tarea = db.relationship('Tareas',backref='tarea',lazy='dynamic')

class Tarea(db.Model):
    __tablename__='Tareas'
    id = db.Column(db.Integer,primary_key=True)
    titulo = db.Column(db.Text)
    fecha = db.Column(db.Date)
    idcategoria = db.Column(db.Integer,db.ForeignKey('Cat_categorias.id_categorias'),name='fk_categorias_tarea')
    idestado = db.Column(db.Integer,db.ForeignKey('Cat_estado.id_estado'),name='fk_estado_tarea')