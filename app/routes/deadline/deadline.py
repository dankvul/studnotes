from flask import render_template, flash
from flask_login import current_user, login_required

from app.models.users import *
from app import Config
from app.routes.deadline import bp
from flask import request, jsonify
from sqlalchemy import desc
import datetime


class upgraded_deadline:
    def __init__(self, id, group_id, exp_date, body, state, color):
        self.id = id
        self.group_id = group_id
        self.exp_date = exp_date
        self.body = body
        self.state = state  # hard == true, soft == false
        self.color = color


@bp.route('/deadlines', methods=['GET', 'POST'])
@login_required
def deadline_page():
    if current_user.group_id is None:
        flash('Your group is NULL, please, send message to vk.com/jodyk')
        return render_template('deadlines.html', title='Deadline', admins=Config.admins)

    deadlines_query = Deadline.query.filter_by(group_id=current_user.group_id).order_by(desc(Deadline.exp_date)).all()
    deadlines = []
    for i in deadlines_query:
        deadlines.append(upgraded_deadline(i.id, i.group_id, i.exp_date, i.body, i.state, color='white'))
    for i in deadlines:
        i.exp_date = i.exp_date.strftime("%d.%m.%Y")
    return render_template('deadlines.html', title='Deadline', admins=Config.admins, deadlines=deadlines)


@bp.route('/deadline_add', methods=['POST'])
@login_required
def deadline_add():
    date = request.form['date']
    new_d = datetime.date(int(date[0] + date[1]+date[2]+date[3]), int(date[5]+date[6]), int(date[8] + date[9]))
    new_dl = Deadline(group_id=int(current_user.group_id), body=request.form['body'], state=bool(request.form['state']),
                      exp_date=new_d)
    db.session.add(new_dl)
    db.session.commit()

    return jsonify({'id': str(new_dl.id),
                    'group_id': str(new_dl.group_id),
                    'exp_date': new_dl.exp_date.strftime("%d.%m.%Y"),
                    'body': str(new_dl.body),
                    'state': str(new_dl.state)
                    })