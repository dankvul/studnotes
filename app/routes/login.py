from app import app
from flask import render_template, flash, redirect, url_for
from app.forms.auth import AuthForm, RegForm, NewGroupForm
from flask_login import login_user, logout_user, current_user, login_required
from app.models.users import *

admins = set(['jodyk', 'debdodebug', 'Jake'])


@app.route('/index', methods=['GET'])
def main_page():
    return render_template('index.html', title='Main page', admins=admins)



@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    form = AuthForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login_page'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main_page'))
    return render_template('login.html', title='LoginPage', form=form, admins=admins)


@app.route('/reg', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    form = RegForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        user.set_group_id(form.token.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main_page'))
    return render_template('reg.html', title='RegPage', form=form, admins=admins)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))


@app.route('/create_group', methods=['POST', 'GET'])
@login_required
def new_group():
    if current_user.username not in admins:
        return redirect(url_for('main_page'))
    form = NewGroupForm()

    if form.validate_on_submit():
        group = Group(name=form.name.data)
        group.set_token()
        db.session.add(group)
        db.session.commit()
        return redirect(url_for('group_view'))
    return render_template('new_group.html', title='CreateGroup', form=form, admins=admins)


@app.route('/group_view')
@login_required
def group_view():
    if current_user.username not in admins:
        return redirect(url_for('main_page'))
    form = Group.query.all()
    members = []
    for i in form:
        members.append(User.query.filter_by(group_id=i.id))
    return render_template('group_list.html', title='All groups', group=form, members=members, admins=admins)

