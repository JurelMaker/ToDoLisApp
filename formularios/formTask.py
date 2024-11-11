#Formulario de registro de tareas
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

#Registro de tareas
class formularioTareas(FlaskForm):
    titulo = StringField('Titulo',validators=[DataRequired()],
                         render_kw={"class":"form-control","placeholder":"Ingresa el titulo de la tarea"})
    
    fecha = DateField('Fecha',format='%Y-%m-%d',validators=[DataRequired()],
                      render_kw={"class":"form-control"})

    categoria = SelectField('Categoría', choices=[], coerce=str,validators=[DataRequired()], render_kw={"class":"form-select"})

    boton = SubmitField('Registrar',render_kw={"class":"btn btn-primary"})