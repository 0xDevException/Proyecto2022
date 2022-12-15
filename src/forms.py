from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    country = StringField('Pais', validators=[DataRequired(), Length(max=64)])
    city = StringField('Ciudad', validators=[DataRequired(), Length(max=64)])
    phone = StringField('Telefono', validators=[DataRequired(), Length(max=64)])
    cargo = StringField('Cargo', validators=[DataRequired(), Length(max=64)])
    submit = SubmitField('Registrar')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar Sesión')


class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    content = TextAreaField('Contenido')
    submit = SubmitField('Enviar')

class EditForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    country = StringField('Pais', validators=[DataRequired(), Length(max=64)])
    city = StringField('Ciudad', validators=[DataRequired(), Length(max=64)])
    phone = StringField('Telefono', validators=[DataRequired(), Length(max=64)])
    cargo = StringField('Cargo', validators=[DataRequired(), Length(max=64)])
    submit = SubmitField('Guardar Cambios')

class EditTaskForm(FlaskForm):
    personal = StringField('Personal', validators=[DataRequired(), Length(max=128)])
    task = StringField('Tarea', validators=[DataRequired(), Length(max=128)])
    status = StringField('Estado', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Guardar Cambios')

class AddTaskForm(FlaskForm):
    personal = StringField('Personal', validators=[DataRequired(), Length(max=128)])
    task = StringField('Tarea', validators=[DataRequired(), Length(max=128)])
    status = StringField('Estado', validators=[DataRequired(), Length(max=128)])
    userid = IntegerField('User ID', validators=[DataRequired()])
    adminid = IntegerField('Admin ID', validators=[DataRequired()])
    submit = SubmitField('Guardar Cambios')