from flask import Flask,render_template
from formularios.formTask import formularioTareas
from modelos.models import db,Tarea
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
    tarea = formularioTareas()
    

    return render_template('index.html',formularioTarea=tarea)




if __name__== '__main__':
    app.run(debug=True)