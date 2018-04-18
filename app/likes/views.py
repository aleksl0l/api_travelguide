from flask import Blueprint, request, jsonify
from app.likes.models import Likes
from app.app import session
from app.baseviews import token_required
from sqlalchemy import exc

likes = Blueprint('likes', __name__)


@likes.route('/api_v1.0/add_like', methods=['GET', 'POST'])
@token_required
def api_add_like(current_user):
    try:
        id_sight = request.args['id_sight']
        new_like = Likes(id_user=current_user.id_user, id_sight=id_sight, value=1)
        session.add(new_like)
        session.commit()
        return jsonify({'message': None, 'data': None, 'status': 'success'})
    except exc.IntegrityError:
        session.rollback()
        return jsonify({'message': 'Duplicate', 'data': None, 'status': 'error'})
    except Exception as e:
        session.rollback()
        return jsonify({'message': 'Unexpected error', 'data': None, 'status': 'error'})


@likes.route('/api_v1.0/del_like', methods=['GET', 'POST'])
@token_required
def api_del_like(current_user):
    try:
        id_sight = request.args['id_sight']
        del_like = session.query(Likes).filter(
                                               Likes.id_user == current_user.id_user,
                                               Likes.id_sight == id_sight
                                            ).first()
        session.delete(del_like)
        session.commit()
        return jsonify({'message': None, 'data': None, 'status': 'success'})
    except Exception as e:
        session.rollback()
        return jsonify({'message': 'Unexpected error', 'data': None, 'status': 'error'})