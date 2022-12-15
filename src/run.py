from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from flask_login import LoginManager, logout_user, login_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse

from forms import SignupForm, PostForm, LoginForm, EditForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:example@172.17.0.2/flask' #'postgresql://postgres:mysecretpassword@172.17.0.2:5432/postgres'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)

from models import User, SensorData, TaskData

@app.route("/", methods=['GET', 'POST'])
def index():
    #db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    form2 = SignupForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('admin')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('admin')
            return redirect(next_page)
    
    error = None
    if form2.validate_on_submit():
        name = form2.name.data
        country = form2.country.data
        city = form2.city.data
        phone = form2.phone.data
        cargo = form2.cargo.data
        email = form2.email.data
        password = form2.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = User.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
            # Creamos el usuario y lo guardamos
            user = User(name=name, email=email)
            user.set_password(password)
            user.country = country
            user.city = city
            user.phone = phone
            user.cargo = cargo
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    
    return render_template("Base/index.html", form=form,form2=form2)

@app.route("/dashboard")
def admin():
    #db.create_all()
    #posts = Post.get_all()
    if current_user.is_admin == 1:
        if current_user.is_anonymous:
            return redirect(url_for('index'))
        data = SensorData.get_last(current_user.id)
        data2 = SensorData.get_lastTwo(current_user.id)
        dataTask = TaskData.get_all_admin(current_user.id)
        return render_template("Admin/index.html", data=data, data2=data2, dataTask=dataTask)
    else:
        if current_user.is_anonymous:
            return redirect(url_for('index'))
        dataTask = TaskData.get_all_admin(current_user.id)
        return render_template("User/user.html", dataTask=dataTask)

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    #db.create_all()
    #posts = Post.get_all()
    
    form = EditForm()
    
    if current_user.is_anonymous:
        return redirect(url_for('index'))
    
    if form.validate_on_submit():
       user = User.get_by_id(current_user.id)
       user.email = form.email.data
       user.name = form.name.data
       user.cargo = form.cargo.data
       user.phone = form.phone.data
       user.city = form.city.data
       user.country = form.country.data
       user.save()
    return render_template("Admin/users-profile.html",form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.route('/deleteTask/<int:id>')
def delete_task(id):
    task = TaskData.query.filter_by(id=id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect("/dashboard")

@app.route('/completedTask/<int:id>')
def completed_task(id):
    task = TaskData.query.filter_by(id=id).first()
    task.status = "Completed"
    task.save()
    return redirect("/dashboard")

@app.route('/waitingTask/<int:id>')
def waiting_task(id):
    task = TaskData.query.filter_by(id=id).first()
    task.status = "Waiting"
    task.save()
    return redirect("/dashboard")

@app.route('/pendingTask/<int:id>')
def pending_task(id):
    task = TaskData.query.filter_by(id=id).first()
    task.status = "Pending"
    task.save()
    return redirect("/dashboard")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

##API REST


@app.route('/users')
def get_users():
    users = [ user.serialize() for user in User.query.all() ] 
    return jsonify({'users': users })

@app.route('/sensorData')
def get_sensorData():
    sensorDatas = [ sensorData.serialize() for sensorData in SensorData.query.all() ] 
    return jsonify({'sensorData': sensorDatas })