from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
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