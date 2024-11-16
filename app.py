from flask import Flask,render_template,redirect,url_for,request
from formularios.formTask import formularioTareas
from modelos.models import db,Tarea,Categorias
from flask_migrate import Migrate
import os
from datetime import datetime
from sqlalchemy import or_

app = Flask(__name__)

#clavesecreta
app.config['SECRET_KEY'] = 'clavesecreta'

#Configuracion DB
directorio = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(directorio,'modelos/tareas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
Migrate(app,db)

#fecha actual
hoy = datetime.now().date()

@app.before_request
def tarea_vencer():
    tareas_porvencer = Tarea.query.filter(Tarea.fecha == hoy, Tarea.idestado == 2).all()
    for tarea in tareas_porvencer:
        tarea.idestado = 3
        db.session.add(tarea)
    
    db.session.commit()

@app.before_request
def tarea_vencidas():
    tareas_vendecias = Tarea.query.filter(Tarea.fecha < hoy, Tarea.idestado == 2).all()
    for tarea in tareas_vendecias:
        tarea.idestado = 4
        db.session.add(tarea)
    
    db.session.commit()


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

    #Tarea sin hacer
    tareas_pendientes = Tarea.query.filter(or_(Tarea.idestado == 2 ,Tarea.idestado == 3))

    #Filtrado finalizadas
    tareas_finalizadas = Tarea.query.filter(Tarea.idestado == 1)

    #Filtrado vencidas
    tareas_vencida = Tarea.query.filter(Tarea.idestado == 4)
    


    return render_template('index.html',formularioTarea=tarea,
                           pendientes=tareas_pendientes,terminadas=tareas_finalizadas,vencidas=tareas_vencida)

#Tareas terminadas
@app.route('/terminado',methods=['POST'])
def tarea_terminada():
   tarea_id = request.form.get('id')
   tarea = db.session.get(Tarea,tarea_id)
   tarea.idestado = 1
   tarea.fecha = hoy
   db.session.commit()

   return redirect(url_for('index'))

#ejecutar funcion 
with app.app_context():
    tarea_vencer()
    tarea_vencidas()




if __name__== '__main__':
    app.run(debug=True)