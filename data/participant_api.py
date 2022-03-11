import flask
from flask import jsonify, request, make_response

from . import db_session
from .promotion import Promotions
from .participant import Participants

blueprint = flask.Blueprint(
    'participant_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/promo/<int:promo_id>/participant', methods=['POST'])
def create_participant(promo_id):
    try:
        if not request.json:
            return make_response(jsonify({'error': 'Empty request'}), 400)
        elif not all(key in request.json for key in ['name']):
            return make_response(jsonify({'error': 'Bad request'}), 400)
        db_sess = db_session.create_session()
        promo = db_sess.query(Promotions).get(promo_id)
        if not promo:
            return make_response(jsonify({'error': 'Not found'}), 404)
        part = Participants(
            name=request.json.get('name'),
            promotion=promo
        )
        db_sess.add(part)
        db_sess.commit()
        return jsonify({'success': 'OK', 'id': part.id})
    except BaseException as e:
        print(e)
        return make_response(jsonify({'error': 'Bad request'}), 400)


@blueprint.route('/promo/<int:promo_id>/participant/<int:participant_id>', methods=['DELETE'])
def delete_participant(promo_id, participant_id):
    db_sess = db_session.create_session()
    promo = db_sess.query(Promotions).get(promo_id)
    if not promo:
        return make_response(jsonify({'error': 'Not found'}), 404)
    part = db_sess.query(Participants).get(participant_id)
    if not part or part.promotion != promo:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(part)
    db_sess.commit()
    return jsonify({'success': 'OK'})
