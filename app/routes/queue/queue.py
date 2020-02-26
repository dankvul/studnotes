from flask import render_template
from flask_login import login_required, current_user
from flask import request, jsonify
from werkzeug.exceptions import BadRequest

from app import db
from app.models.users import Queue, QueueMember, User
from app.routes.queue import bp


@bp.route('/queues', methods=['GET'])
@login_required
def queue_list():
    queues = Queue.query.filter_by(group_id=current_user.group_id).all()
    return render_template('queue_list.html', queues=queues)


@bp.route('/queues/<int:queue_id>', methods=['GET'])
@login_required
def queue_menu(queue_id):
    current_queue = Queue.query.filter_by(id=queue_id).first()
    temp = QueueMember.query.filter_by(queue_id=queue_id).all()
    queue_members = []
    for i in temp:
        queue_members.append(User.query.filter_by(id=i.user_id).first())
    return render_template('queue_menu.html', queue_members=queue_members, current_queue=current_queue)


@bp.route('/queues/enter', methods=['POST'])
@login_required
def enter_to_queue():
    user_id = request.form['user_id']
    queue_id = request.form['queue_id']
    check_unique = QueueMember.query.filter_by(user_id=user_id, queue_id=queue_id).all()
    if len(check_unique) >= 1:
        return jsonify({'message': 'You are already in queue'})
    new_member = QueueMember(user_id=user_id, queue_id=queue_id)
    db.session.add(new_member)
    db.session.commit()
    return jsonify({'message': 'You have been successfully added'})


@bp.route('/queues/add', methods=['POST'])
@login_required
def create_queue():
    new_queue_name = request.form['name']
    if Queue.query.filter_by(queue_name=new_queue_name).first():
        raise BadRequest()
    queue_new = Queue(queue_name=new_queue_name, group_id=current_user.group_id)
    db.session.add(queue_new)
    db.session.commit()
    return jsonify({'id': queue_new.id,
                    'group_id': queue_new.group_id,
                    'name': queue_new.queue_name,
                    'size': queue_new.get_size()})



