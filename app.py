from flask import Flask,render_template,redirect,url_for
from formularios.formTask import formularioTareas
from modelos.models import db,Tarea,Categorias
from flask_migrate import Migrate
import os

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
        task = Tarea(titulo=tarea.titulo.data,fecha=tarea.fecha.data,idcategoria=tarea.categoria.data,idestado=1)
        db.session.add(task)
        db.session.commit()

        return redirect(url_for('index'))
    
    #Recuperar datos
    todas_tareas = Tarea.query.all()

    return render_template('index.html',formularioTarea=tarea,todas=todas_tareas)




if __name__== '__main__':
    app.run(debug=True)