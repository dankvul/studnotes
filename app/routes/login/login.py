from flask import render_template, flash, redirect, url_for
from app.forms.auth import AuthForm, RegForm, NewGroupForm
from flask_login import login_user, logout_user, current_user, login_required
from app.models.users import *
from app import Config
from app.routes.login import bp


@bp.route('/index', methods=['GET'])
def main_page():
    return render_template('index.html', title='Main page')


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/login', methods=['GET', 'POST'])
def login_page():
    admin = User.query.filter_by(username='jodyk').first()
    if not admin:
        new_admin = User(username='jodyk')
        new_admin.set_password(Config.ADMIN_PASS)
        db.session.add(new_admin)
        db.session.commit()
    if current_user.is_authenticated:
        return redirect(url_for('login.main_page'))
    form = AuthForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login.login_page'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('login.main_page'))
    return render_template('login.html', title='LoginPage', form=form, admins=Config.admins)


@bp.route('/reg', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login.main_page'))
    form = RegForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        user.set_group_id(form.token.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('login.main_page'))
    return render_template('reg.html', title='RegPage', form=form, admins=Config.admins)


@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login_page'))


@bp.route('/create_group', methods=['POST', 'GET'])
@login_required
def new_group():
    if current_user.username not in Config.admins:
        return redirect(url_for('login.main_page'))
    form = NewGroupForm()

    if form.validate_on_submit():
        group = Group(name=form.name.data)
        group.set_token()
        db.session.add(group)
        db.session.commit()
        return redirect(url_for('login.group_view'))
    return render_template('new_group.html', title='CreateGroup', form=form, admins=Config.admins)


@bp.route('/group_view')
@login_required
def group_view():
    if current_user.username not in Config.admins:
        return redirect(url_for('login.main_page'))
    form = Group.query.all()
    members = []
    for i in form:
        members.append(User.query.filter_by(group_id=i.id))
    return render_template('group_list.html', title='All groups', group=form, members=members, admins=Config.admins)

