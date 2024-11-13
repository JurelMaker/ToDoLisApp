from flask import Flask,render_template,redirect,url_for,request
from formularios.formTask import formularioTareas
from modelos.models import db,Tarea,Categorias
from flask_migrate import Migrate
import os
from datetime import datetime

app = Flask(__name__)

#clavesecreta
app.config['SECRET_KEY'] = 'clavesecreta'

#Configuracion DB
directorio = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(directorio,'modelos/tareas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
Migrate(app,db)

#Vista principal
@app.route('/',methods=['GET','POST'])
def index():

    #Ingresar tarea
    tarea = formularioTareas()
    tarea.categoria.choices = [(c.id_categorias,c.nombre) for c in Categorias.query.all()]
    if tarea.validate_on_submit():
        task = Tarea(titulo=tarea.titulo.data,fecha=tarea.fecha.data,idcategoria=tarea.categoria.data,idestado=2)
        db.session.add(task)
        db.session.commit()

        return redirect(url_for('index'))
    
    #fecha actual
    hoy = datetime.now().date()

    #Recuperar datos
    todas_tareas = Tarea.query.all()
    #Logica de las tareas por vencer
    for t in todas_tareas:
        if hoy == t.fecha and t.idestado == 2:
            t.idestado = 3
            db.session.add(t)
            db.session.commit()
        elif hoy > t.fecha and t.idestado == 2: 
            t.idestado = 4
            db.session.add(t)
            db.session.commit()


    return render_template('index.html',formularioTarea=tarea,todas=todas_tareas)

#Tareas terminadas
@app.route('/terminado',methods=['POST'])
def tarea_terminada():
   tarea_id = request.form.get('id')
   tarea = db.session.get(Tarea,tarea_id)
   tarea.idestado = 1
   db.session.commit()

   return redirect(url_for('index'))




if __name__== '__main__':
    app.run(debug=True)